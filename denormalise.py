#!/usr/bin/env python

import re, sys, pprint

DEFAULT_OWNER = 'nobody'

def extract_owners(owner_str):
    m = re.search("(\s*[a-zA-Z\.]+\s*(?:(?:,|/|and)\s*[a-zA-Z\.]+\s*)*)", owner_str)
    if m:
        names = re.split(",|/|and", m.group(1).replace(" ", ""))
        return names
    return []

def make_note(line, tabstr):
    m = re.match('(\s*)(\+|\-)?\s*([^\[]*)(\[[^\]]+\])?', line)
    if m:
        groups = m.groups(default='')
        indent = groups[0].count(tabstr)
        owner = extract_owners(groups[3])
        ap = True if groups[1] == '+' else False
        return {
            'level': indent,
            'note': groups[2],
            'owner': owner,
            'ap': ap
        }
    else:
        raise Exception('Bad line "%s"' % line)

def projects(lines):
    proj = []
    for line in lines:
        line = line.rstrip()
        if line == "":
            if len(proj):
                yield proj
                proj = []
            # skip blank lines in general
        else:
            proj.append(make_note(line, '  '))
    if len(proj):
        yield proj

def parse(lines, default_owner):
    proj_list = []
    for proj_chunk in projects(lines):
        proj_list.append(build_tree(proj_chunk, 0, [default_owner]))
    return proj_list

def build_tree(items, this_level, default_owner):
    proj = []
    while len(items) > 0:
        if items[0]['level'] < this_level:
            # end of nested list
            return proj
        elif items[0]['level'] > this_level:
            if len(proj) > 0:
                proj[-1]['items'] = build_tree(items, items[0]['level'], proj[-1]['owner'])
        elif items[0]['level'] == this_level:
            # consume items as we go
            item = items.pop(0)
            if len(item['owner']) == 0:
                item['owner'] = default_owner
            proj.append(item)

    return proj


def render_project(p):
    print "Project: %s (owner: %s)" % (p['note'], ", ".join(p['owner']) )
    render_items(p['items'])

def render_items(items):
    for i in items:
        if i['ap'] == True:
            print "%s - AP: %s [%s]" % (i['level'] * "  ", i['note'], ", ".join(i['owner']) )
        else:
            print "%s - %s" % (i['level'] * "  ", i['note'] )
        if 'items' in i:
            render_items(i['items'])


if __name__=="__main__":
    projects = parse(sys.stdin, DEFAULT_OWNER)
    action = 'show'
    if action == 'show':
        for project in projects:
            render_project(project[0])
            print
