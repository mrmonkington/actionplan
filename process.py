import re, sys

DEFAULT_OWNERS = ("nobody",)

if __name__ == "__main__":
    name_stack = [DEFAULT_OWNERS,]
    name_colors = {}
    for name in name_stack:
        name_colors[name] = ""
    last_indent = 0

    # output string
    op = ""

    for ln in sys.stdin:
        ln = ln.rstrip()
        # calc indent level
        m = re.match( "(\s*)", ln )
        indent = len(m.group(1).replace("\t", "  ")) / 2

        # lose current owner if we
        indent_change = indent - last_indent

        #if indent_change == 0:
        #    name = name_stack.pop()

        while indent_change < 0:
            name_stack.pop()
            indent_change += 1

        while indent_change > 0:
            # copy parent owner
            name_stack.append(name_stack[-1])
            indent_change -= 1

        # lookup new owners 
        m = re.search("(.*)\[(\s*[a-zA-Z\.]+\s*(?:(?:\/|and)\s*[a-zA-Z\.]+\s*)*)\]\s*$", ln)
        if m:
            names = re.split("/|and", m.group(2).replace(" ", ""))
            for name in names:
                # flag name as used
                name_colors[name] = ""
            name_stack.pop()
            name_stack.append(names)

            ln = m.group(1)

        curr_indent = indent

        # action point
        m = re.match( "(\s*)(\+|\-)(.*)$", ln )
        if m:
            op += m.group(1) + "-"
            if m.group(2) == "+":
                # add owners
                op += " **AP**" 
            op += m.group(3).rstrip()
            if m.group(2) == "+":
                # add owners
                op += " [" + ", ".join(name_stack[-1]) + "]"
            op += "\n"
        elif ln.strip() != "":
            op += "## " + ln + "\n\n"
        else:
            op += ln + "\n"

    print op


