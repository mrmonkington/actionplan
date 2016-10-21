#!/usr/bin/env python

import re, sys

DEFAULT_OWNERS = ("nobody",)

if __name__ == "__main__":
    name_stack = [DEFAULT_OWNERS,]
    name_colors = {}
    for name in name_stack:
        name_colors[name] = ""
    last_indent = 0
    names = []

    # output string
    op = ""
    new_names = False

    for ln in sys.stdin:
        ln = ln.rstrip()
        # calc indent level
        m = re.match( "(\s*)", ln )
        indent = len(m.group(1).replace("\t", "  ")) / 2

        # lose current owner if we
        indent_change = indent - last_indent

        while indent_change < 0:
            name_stack.pop()
            indent_change += 1

        while indent_change > 0:
            # copy parent owner
            if new_names != False:
                name_stack.append(new_names)
            else:
                name_stack.append(name_stack[-1])
            indent_change -= 1

        new_names = False

        # lookup new owners 
        m = re.search("(.*)\[(\s*[a-zA-Z\.]+\s*(?:(?:\/|and)\s*[a-zA-Z\.]+\s*)*)\]\s*$", ln)
        if m:
            names = re.split("/|and", m.group(2).replace(" ", ""))
            for name in names:
                # flag name as used
                name_colors[name] = ""
            new_names = names

            ln = m.group(1)

        else:
            names = name_stack[-1]

        curr_indent = indent

        # is item?
        m = re.match( "(\s*)(\+|\-)(.*)$", ln )
        if m:
            # action point
            if m.group(2) == "+":
                # add owners
                op += m.group(1) + "+"
            else:
                op += m.group(1) + "-"
            op += m.group(3).rstrip()
            if m.group(2) == "+":
                # add owners
                op += " [" + ", ".join(names) + "]"
            op += "\n"
        elif ln.strip() != "":
            # is a project title
            op += "" + ln.strip() + " (owner: " + ", ".join(names) + ")\n"
        else:
            op += ln + "\n"

    print op


