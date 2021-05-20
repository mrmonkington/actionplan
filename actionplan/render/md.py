"""Markdown renderer
"""

def render_projects(projects):
    """Render all projects and items into a string
    """
    ret = ""
    for project in projects:
        probject = project[0]
        ret += "**Project: %s (owner: %s)**\n" \
               % (probject['note'], ", ".join(probject['owner'])) + "\n"
        ret += render_items(probject['items'])
        ret += "\n"
    return ret

def render_items(items):
    """Render all items within a project into a string
    """
    ret = ""
    for i in items:
        if i['ap'] == 'todo':
            ret += "%s - [ ] %s [%s]\n" % (i['level'] * "  ", i['note'], ", ".join(i['owner']))
        elif i['ap'] == 'done':
            ret += "%s - [x] ~~%s~~ [%s]\n" \
                   % (i['level'] * "  ", i['note'].strip(), ", ".join(i['owner']))
        else:
            ret += "%s - %s\n" % (i['level'] * "  ", i['note'])
        if 'items' in i:
            ret += render_items(i['items'])
    return ret

def render_titles(projects):
    """Summarise just project names into a string
    """
    ret = ""
    for project in projects:
        probject = project[0]
        ret += "**Project: %s (owner: %s)**\n" % (probject['note'], ", ".join(probject['owner']))
    return ret
