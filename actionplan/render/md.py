def render_projects(projects):
    ret = ""
    for project in projects:
        p = project[0]
        ret += "**Project: %s (owner: %s)**\n" % (p['note'], ", ".join(p['owner']) ) + "\n"
        ret += render_items(p['items'])
        ret += "\n"
    return ret

def render_items(items):
    ret = ""
    for i in items:
        if i['ap'] == 'todo':
            ret += "%s + [ ] %s [%s]\n" % (i['level'] * "  ", i['note'], ", ".join(i['owner']) )
        elif i['ap'] == 'done':
            ret += "%s + [x] %s [%s]\n" % (i['level'] * "  ", i['note'], ", ".join(i['owner']) )
        else:
            ret += "%s - %s\n" % (i['level'] * "  ", i['note'] )
        if 'items' in i:
            ret += render_items(i['items'])
    return ret

def render_titles(projects):
    ret = ""
    for project in projects:
        p = project[0]
        ret += "**Project: %s (owner: %s)**\n" % (p['note'], ", ".join(p['owner']) )
    return ret

