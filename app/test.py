from typing import TypeAlias


foo = [1, 2, 3]

a = [x for x in foo if foo == 3]

_type: TypeAlias = str


def foobar(a: _type, b: _type, c: _type) -> _type:
    return a + b + c


def foobar2(a: _type, b: _type, c: _type) -> _type:
    return a + b + c
