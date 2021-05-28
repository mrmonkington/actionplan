"""Parse actionplan into a sort of AST
"""

import re
from typing import Iterable
import logging

import marko

def extract_owners(owner_str):
    """For a given line, identify 'owner' strings (wrapped in [])
    """
    match = re.search(r"(\s*[a-zA-Z\.]+\s*(?:(?:,|/|and)\s*[a-zA-Z\.]+\s*)*)",
                      owner_str)
    if match:
        names = re.split(",|/|and", match.group(1).replace(" ", ""))
        return names
    return []


def parse_line(line, tabstr):
    """Parses a line in the input stream
    """
    match = re.match(r'(\s*)(\+|\-|\*)?\s*([^\[]*)(\[[^\]]+\])?', line)
    if match:
        groups = match.groups(default='')
        indent = groups[0].count(tabstr)
        owner = extract_owners(groups[3])
        if groups[1] == '+':
            aptype = 'todo'
        elif groups[1] == '*':
            aptype = 'done'
        else:
            aptype = False
        return {
            'level': indent,
            'note': groups[2],
            'owner': owner,
            'ap': aptype
        }

    raise Exception('Bad line "%s"' % line)


def parse_projects(lines):
    """Top level tokenisation of input stream into
    project titles or project "chunks"
    """
    proj = []
    for line in lines:
        line = line.rstrip()
        if line.startswith('#'):
            yield "title", line
        elif line == "":
            if len(proj) > 0:
                yield "project", proj
                proj = []
            # skip blank lines in general
        else:
            proj.append(parse_line(line, '  '))
    if len(proj) > 0:
        yield "project", proj


def interpret_node(element):
    """Marko AST/DOM is a bit thin - you have to use a bit of reflection
    to find out what you have
    """
    rv = {k: v for k, v in element.__dict__.items() if not k.startswith("_")}
    rv["element"] = element.__class__.__name__
    return rv


def flatten_to_text(el):
    """ Extract text from a marko node
    e.g. a heading node encodes text thus:
        {
            'level': 1,
            'children': [
                {'element': 'raw_text',
                 'children': 'Project 3', 'escape': True}
            ],
            'element': 'heading'
        }
    """

    if isinstance(el, str):
        return el

    logging.debug(el)
    return "".join(flatten_to_text(child) for child in el.children)


def iterate_top_level_elements(nodelist, default_owners):
    """Walk through headings, working out owners
    """
    depth = 0
    owner_stack = [default_owners, ]
    current_owners = default_owners
    try:
        for node in nodelist:
            el = interpret_node(node)
            logging.debug(el['element'])

            # Headings act like section parents and can
            # change ownership of everything that follows.
            # 'Smaller' headings inherit from 'larger', e.g. h2 from h1
            # h1 technically set document ownership, but you can also
            # have more than one h1 if you like
            if el['element'] == 'Heading':
                logging.debug('Heading')
                text = flatten_to_text(node)
                owners = extract_owners(text)
                if len(owners):
                    current_owners = owners
                while depth < el['level']:
                    owner_stack.append(current_owners)
                    depth += 1
                while depth > el['level']:
                    owner_stack.pop()
                    depth -= 1
                owner_stack[depth] = current_owners
                node.owners = current_owners

            if el['element'] == 'List':
                logging.debug('List')
                el['owners'] = "/".join(current_owners)
                node.owners = current_owners

    except (TypeError, AttributeError):
        # this is a string leaf in root position
        # re-raise for now - can't see why this would be expected
        raise
    # not sure it's worth returning anything...
    return current_owners


def visit_node(nodelist, current_owners):
    """Recurse through the AST/DOM tree
    """
    owners = current_owners
    try:
        for node in enumerate(nodelist):
            el = interpret_node(node)

            # node_type = el["element"])
            if "children" in el:
                visit_node(el["children"], owners)
    except (TypeError, AttributeError):
        # this is a string leaf
        text = nodelist
        owners = extract_owners(text)


def parse(src: str, parser, default_owners):
    """ 
    """
    #parser = marko.Markdown(parser=marko.Parser)
    import marko
    from marko.ast_renderer import ASTRenderer
    pr = marko.Markdown(parser=marko.Parser, renderer=ASTRenderer)
    ast = pr.parse(src)
    ast = annotate(ast, default_owners)
    return ast

def annotate(ast, default_owners):
    """ Walk a Marko AST and update with action and owner info
    """
    root_element = interpret_node(ast)
    assert root_element["element"] == 'Document'
    if "children" in root_element:
        # pass 1 - serial inheritence of heading (project) owners
        owners = iterate_top_level_elements(root_element["children"],
                                            default_owners)
        # owners will now be either default or inherited from h1
        # pass 2 - recursive inheritence of list owners
        #rvisit_node(root_element["children"], owners)
    return ast
    # return old_parse(src, default_owner)

def old_parse(lines, default_owner):
    """Parse input text, splitting it into  project sized chunks
    as per titles
    """
    proj_list = []
    for chunk_type, proj_chunk in parse_projects(lines):
        if chunk_type == "title":
            proj_list.append(proj_chunk)
        if chunk_type == "project":
            proj_list.append(build_tree(proj_chunk, 0, [default_owner]))
    return proj_list


def build_tree(items, this_level, default_owner):
    """Turn tokenised text into document tree
    """
    proj = []
    while len(items) > 0:
        if items[0]['level'] < this_level:
            # end of nested list
            return proj

        if items[0]['level'] > this_level:
            if len(proj) > 0:
                proj[-1]['items'] = build_tree(items, items[0]['level'],
                                               proj[-1]['owner'])
        elif items[0]['level'] == this_level:
            # consume items as we go
            item = items.pop(0)
            if len(item['owner']) == 0:
                item['owner'] = default_owner
            proj.append(item)

    return proj
