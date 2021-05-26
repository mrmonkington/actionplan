"""Parse actionplan into a sort of AST
"""

import re

def extract_owners(owner_str):
    """For a given line, identify 'owner' strings (wrapped in [])
    """
    match = re.search(r"(\s*[a-zA-Z\.]+\s*(?:(?:,|/|and)\s*[a-zA-Z\.]+\s*)*)", owner_str)
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

def parse(lines, default_owner):
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
                proj[-1]['items'] = build_tree(items, items[0]['level'], proj[-1]['owner'])
        elif items[0]['level'] == this_level:
            # consume items as we go
            item = items.pop(0)
            if len(item['owner']) == 0:
                item['owner'] = default_owner
            proj.append(item)

    return proj
