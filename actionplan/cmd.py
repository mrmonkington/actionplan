#!/usr/bin/env python

import re, sys, argparse

DEFAULT_OWNER = 'nobody'

def extract_owners(owner_str):
    m = re.search("(\s*[a-zA-Z\.]+\s*(?:(?:,|/|and)\s*[a-zA-Z\.]+\s*)*)", owner_str)
    if m:
        names = re.split(",|/|and", m.group(1).replace(" ", ""))
        return names
    return []

def parse_line(line, tabstr):
    m = re.match('(\s*)(\+|\-|=)?\s*([^\[]*)(\[[^\]]+\])?', line)
    if m:
        groups = m.groups(default='')
        indent = groups[0].count(tabstr)
        owner = extract_owners(groups[3])
        if groups[1] == '+':
            ap = 'todo'
        elif groups[1] == '=':
            ap = 'done'
        else:
            ap = False
        return {
            'level': indent,
            'note': groups[2],
            'owner': owner,
            'ap': ap
        }
    else:
        raise Exception('Bad line "%s"' % line)

def parse_projects(lines):
    proj = []
    for line in lines:
        line = line.rstrip()
        if line == "":
            if len(proj):
                yield proj
                proj = []
            # skip blank lines in general
        else:
            proj.append(parse_line(line, '  '))
    if len(proj):
        yield proj

def parse(lines, default_owner):
    proj_list = []
    for proj_chunk in parse_projects(lines):
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

import render.ap
#import render.ap

def run():
    parser = argparse.ArgumentParser(description="User management tool for Google Analytics")
    parser.add_argument(help="Input file in AP format", dest="input_file", type=str, default='-')
    #parser.add_argument("--showall", "-a", dest="action", help="What output do you want", action='store_const', const='showall')
    parser.add_argument("--showtitles", "-t", dest="action", help="What output do you want", action='store_const', const='showtitles')
    parser.add_argument("--format", "-f", dest="format", help="What format do you want? Options: html, md. Default: md", type=str, default='md')
    parser.add_argument("--filterowner", "-o", dest="owner_filter", help="Filter APs for which user", type=str, default="all")
    args = parser.parse_args()

    if args.input_file == '-':
        projects = parse(sys.stdin, DEFAULT_OWNER)
    else:
        with open(args.input_file) as inp:
            projects = parse(inp, DEFAULT_OWNER)

    if 
    if args.action == 'showtitles':
        print( render_titles(projects) )
    else:
        print( render_projects(projects) )
