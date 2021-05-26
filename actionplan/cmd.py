"""
ActionPlan main utility
"""
#!/usr/bin/env python3

import re
import sys
import argparse
import logging

from .render import md
from . import parse
#import render.ap

DEFAULT_OWNER = 'nobody'


def main():
    """CLI entrypoint
    """
    parser = argparse.ArgumentParser(description="ActionPlan meeting notes utility")
    parser.add_argument("--input", "-i", help="Input file in AP format", type=str, default='-')
    #parser.add_argument("--showall", "-a",
    #    dest="action", help="What output do you want", action='store_const', const='showall')
    parser.add_argument("--showtitles", "-t", dest="action", help="What output do you want",
                        action='store_const', const='showtitles')
    parser.add_argument("--filterowner", "-o", help="Filter APs for which user", type=str)
    parser.add_argument("--debug", "-d", action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if args.input == '-':
        projects = parse.parse(sys.stdin, DEFAULT_OWNER)
    else:
        with open(args.input_file) as inp:
            projects = parse.parse(inp, DEFAULT_OWNER)

    if args.action == 'showtitles':
        print(md.render_titles(projects))
    else:
        print(md.render_projects(projects))

if __name__ == "__main__":
    main()
