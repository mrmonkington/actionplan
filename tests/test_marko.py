"""Debug tool for dumping Marko AST as graphviz
"""

import marko
import graphviz
from marko.ast_renderer import ASTRenderer


def interpret(element):
    """Marko AST/DOM is a bit thin - you have to use a bit of reflection
    to find out what you have
    """
    rv = {k: v for k, v in element.__dict__.items() if not k.startswith("_")}
    rv["element"] = element.__class__.__name__
    return rv


def visit(dot, nodelist, parent_key):
    """Recurse through the AST/DOM tree
    """
    try:
        for index, node in enumerate(nodelist):
            el = interpret(node)
            key = "%s.%i" % (parent_key, index)

            dot.node(key, el["element"])
            # by weighting the first children more strongly
            # we get a graph that is more 'top/left aligned'
            dot.edge(parent_key, key, weight=str((100/pow(index+1, 1))))
            if "children" in el:
                visit(dot, el["children"], key)
    except (TypeError, AttributeError):
        # this is a string leaf
        key = "%s.%i" % (parent_key, 1)
        dot.node(key, "\"%s\"" % (nodelist,), fontname="sans bold")
        dot.edge(parent_key, key)


def graphit(ast):
    """Dump this AST as graphviz dot for rendering by external tool
    e.g.
        $ python tests/test_marko.py  | dot -Tpng  | feh -
    """
    el = interpret(ast)
    assert el["element"] == 'Document'
    dot = graphviz.Digraph(comment='Parsed Document',
                           graph_attr={'rankdir': 'LR', 'ordering': 'out',
                                       'nodesep': '0.05', 'splines': 'true',
                                       'concentrate': 'true'},
                           node_attr={'shape': 'box', 'fontsize': '8',
                                      'fontname': 'mono'},
                           edge_attr={'arrowsize': '0.2', 'color': '#b0e0ff'}
                           )
    key = '1'
    if "children" in el:
        visit(dot, el["children"], key)
    print(dot.source)


if __name__ == "__main__":
    with open('tests/model_example_1.ap', 'r') as f:
        mdt = f.read()
        pr = marko.Markdown(parser=marko.Parser, renderer=ASTRenderer)
        p = pr.parse(mdt)
        # pr.render(p)
        # pprint.pprint(p)
        # pprint.pprint(pr.render(p))
        graphit(p)


# (ve) mark@pancake:actionplan $ marko -r marko.ast_renderer.ASTRenderer < tests/model_example_1.ap
# {'link_ref_defs': {}, 'children': [{'level': 1, 'children': [{'element':
# 'raw_text', 'children': 'Title [projectowner]', 'escape': True}], 'element':
# 'heading'}, {'element': 'blank_line'}, {'children': [{'element': 'raw_text',
# 'children': 'Paragraph 1.', 'escape': True}], 'element': 'paragraph'},
# {'element': 'blank_line'}, {'level': 2, 'children': [{'element': 'raw_text',
# 'children': 'Project 1 [project1owner]', 'escape': True}], 'element':
# 'heading'}, {'element': 'blank_line'}, {'bullet': '-', 'ordered': False,
# 'start': 1, 'tight': True, 'children': [{'children': [{'children': [{'element':
# 'raw_text', 'children': 'list 1', 'escape': True}], 'element': 'paragraph'}],
# 'element': 'list_item'}, {'children': [{'children': [{'element': 'raw_text',
# 'children': 'list 2 [owner1]', 'escape': True}], 'element': 'paragraph'},
# {'bullet': '+', 'ordered': False, 'start': 1, 'tight': True, 'children':
# [{'children': [{'children': [{'element': 'raw_text', 'children': 'action 2.1',
# 'escape': True}], 'element': 'paragraph'}], 'element': 'list_item'}],
# 'element': 'list'}, {'bullet': '-', 'ordered': False, 'start': 1, 'tight':
# True, 'children': [{'children': [{'children': [{'element': 'raw_text',
# 'children': 'list 2.2', 'escape': True}], 'element': 'paragraph'}], 'element':
# 'list_item'}], 'element': 'list'}], 'element': 'list_item'}, {'children':
# [{'children': [{'element': 'raw_text', 'children': 'list 3 [owner2]', 'escape':
# True}], 'element': 'paragraph'}, {'bullet': '+', 'ordered': False, 'start': 1,
# 'tight': True, 'children': [{'children': [{'children': [{'element': 'raw_text',
# 'children': 'action 3.1', 'escape': True}], 'element': 'paragraph'}],
# 'element': 'list_item'}], 'element': 'list'}, {'bullet': '-', 'ordered': False,
# 'start': 1, 'tight': True, 'children': [{'children': [{'children': [{'element':
# 'raw_text', 'children': 'list 3.2 [owner3]', 'escape': True}], 'element':
# 'paragraph'}, {'bullet': '-', 'ordered': False, 'start': 1, 'tight': True,
# 'children': [{'children': [{'children': [{'element': 'raw_text', 'children':
# 'list 3.2.1', 'escape': True}], 'element': 'paragraph'}], 'element':
# 'list_item'}], 'element': 'list'}, {'bullet': '+', 'ordered': False, 'start':
# 1, 'tight': True, 'children': [{'children': [{'children': [{'element':
# 'raw_text', 'children': 'action 3.2.2', 'escape': True}], 'element':
# 'paragraph'}], 'element': 'list_item'}, {'children': [{'children': [{'element':
# 'raw_text', 'children': 'action 3.2.3 [owner4]', 'escape': True}], 'element':
# 'paragraph'}], 'element': 'list_item'}, {'children': [{'children': [{'element':
# 'raw_text', 'children': 'action 3.2.4', 'escape': True}], 'element':
# 'paragraph'}], 'element': 'list_item'}], 'element': 'list'}], 'element':
# 'list_item'}], 'element': 'list'}], 'element': 'list_item'}], 'element':
# 'list'}, {'bullet': '+', 'ordered': False, 'start': 1, 'tight': True,
# 'children': [{'children': [{'children': [{'element': 'raw_text', 'children':
# 'action 4', 'escape': True}], 'element': 'paragraph'}], 'element':
# 'list_item'}, {'children': [{'children': [{'element': 'raw_text', 'children':
# 'action 5 [owner5]', 'escape': True}], 'element': 'paragraph'}], 'element':
# 'list_item'}, {'children': [{'children': [{'element': 'raw_text', 'children':
# 'action 6', 'escape': True}], 'element': 'paragraph'}], 'element':
# 'list_item'}], 'element': 'list'}, {'element': 'blank_line'}, {'bullet': '-',
# 'ordered': False, 'start': 1, 'tight': True, 'children': [{'children':
# [{'children': [{'element': 'raw_text', 'children': 'list a', 'escape': True}],
# 'element': 'paragraph'}], 'element': 'list_item'}, {'children': [{'children':
# [{'element': 'raw_text', 'children': 'list b', 'escape': True}], 'element':
# 'paragraph'}], 'element': 'list_item'}], 'element': 'list'}, {'element':
# 'blank_line'}, {'children': [{'element': 'raw_text', 'children': 'paragraph',
# 'escape': True}], 'element': 'paragraph'}, {'element': 'blank_line'},
# {'children': [{'element': 'raw_text', 'children': 'paragraph', 'escape':
# True}], 'element': 'paragraph'}, {'element': 'blank_line'}, {'level': 1,
# 'children': [{'element': 'raw_text', 'children': 'Project 2 [project2owner]',
# 'escape': True}], 'element': 'heading'}, {'element': 'blank_line'}, {'bullet':
# '-', 'ordered': False, 'start': 1, 'tight': True, 'children': [{'children':
# [{'children': [{'element': 'raw_text', 'children': 'list x', 'escape': True}],
# 'element': 'paragraph'}], 'element': 'list_item'}, {'children': [{'children':
# [{'element': 'raw_text', 'children': 'list y', 'escape': True}], 'element':
# 'paragraph'}, {'bullet': '-', 'ordered': False, 'start': 1, 'tight': True,
# 'children': [{'children': [{'children': [{'element': 'raw_text', 'children':
# 'list z', 'escape': True}], 'element': 'paragraph'}], 'element': 'list_item'}],
# 'element': 'list'}], 'element': 'list_item'}], 'element': 'list'}, {'element':
# 'blank_line'}, {'level': 1, 'children': [{'element': 'raw_text', 'children':
# 'Project 3', 'escape': True}], 'element': 'heading'}, {'element':
# 'blank_line'}, {'bullet': '-', 'ordered': False, 'start': 1, 'tight': True,
# 'children': [{'children': [{'children': [{'element': 'raw_text', 'children':
# 'list x', 'escape': True}], 'element': 'paragraph'}], 'element': 'list_item'},
# {'children': [{'children': [{'element': 'raw_text', 'children': 'list y',
# 'escape': True}], 'element': 'paragraph'}, {'bullet': '-', 'ordered': False,
# 'start': 1, 'tight': True, 'children': [{'children': [{'children': [{'element':
# 'raw_text', 'children': 'list z', 'escape': True}], 'element': 'paragraph'}],
# 'element': 'list_item'}], 'element': 'list'}], 'element': 'list_item'}],
# 'element': 'list'}], 'element': 'document'}
