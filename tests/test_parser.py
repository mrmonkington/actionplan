"""Fairly high level parser tests
"""

# import pytest
from actionplan import parse
# import logging

import string

def norm_compare(s1, s2):
    """Compare two strings ignoring whitespace
    """
    remove = string.whitespace
    return s1.translate(None, remove) == s2.translate(None, remove)


def test_parse_example_1_ast():
    """Bit of a dumb test - compares the AST of a parsed file with the
    AST from a previous run that looks *ok*
    """
    with open('tests/model_example_1.ap', 'r') as f:

        r = parse.parse(f, "meetingowner")
        print(r)

        # mdt = f.read()
        # pr = marko.Markdown(parser=marko.Parser, renderer=ASTRenderer)
        # p = pr.parse(mdt)
        # ast = pr.render(p)
