import pytest
from main import *

class TestType:
    def test_constuctors(self):
        t1 = Type('implication', Type('base', 'a'), 
                                 Type('implication', Type('base', 'b'),
                                                     Type('base', 'c')))
        t2 = Type.implication(Type.base('a'), 
                              Type.implication(Type.base('b'),
                                               Type.base('c')))
        t3 = Type.parse('a->(b->c)')
        t4 = Type.parse('(((((a))->((b)->c))))')

        assert t1 == t2
        assert t1 == t3
        assert t1 == t4

    def test_apply(self):
        tests_valid = [
            ('a->((c->b)->c)', 'a', '((c->b)->c)'),
            ('((c->b)->c)', 'c->b', 'c'),
        ]

        for t1, t2, result in tests_valid:
            assert Type.parse(t1).apply(Type.parse(t2))==Type.parse(result)

        tests_fail = [
            ('a->b', 'c'),
            ('a', 'a'),
            ('(a->b)->c', 'a'),
            ('c', 'c->d')
        ]

        for t1, t2 in tests_fail:
            with pytest.raises(Exception):
                Type.parse(t1).apply(Type.parse(t2))

class TestTypedTerm:
    def test_constructor(self):
        tt1 = TypedTerm.abstraction(
                TypedTerm.variable('a', Type.parse('p->q')),
                TypedTerm.application(
                    TypedTerm.variable('a'),
                    TypedTerm.variable('b', Type.parse('p'))
                )
            )
        assert str(tt1)=='(La:(p->q).(a b:p))'

    def test_parse(self):
        tt1 = TypedTerm.abstraction(
                TypedTerm.variable('a', Type.parse('p->q')),
                TypedTerm.application(
                    TypedTerm.variable('a'),
                    TypedTerm.variable('b')
                )
            ) 
        assert tt1 == TypedTerm.parse('(La:(p->q).(a b))')

        tts = [
            '((Lx:p.x) y)',
            '((a b) (c d))',
            '((Lx:p.(Ly:q.(z y))) q)',
        ]

        for tt in tts:
            assert(str(TypedTerm.parse(tt))==tt)


def test_type_check():
    tests_ok = [
        ("Lx:a->b.(x y)", "y:a", "(a->b)->b"),
        ("Lx:a->(a->b).Ly:a.((x y) y)", "", "(a->(a->b))->(a->b)"),
        ("((x y) z)", "x:(a->b)->(c->d), y:a->b, z:c", "d"),
    ]

    for term, context, _type in tests_ok:
        assert type_check(TypedTerm.parse(term), 
                    Context.parse(context))==Type.parse(_type), term

    tests_fail = [
        ("y", "x:a, z:b"),
        ("x y", "x:(a->b)->c, y:a"),
        ("Lx:a->b.x y", "y:c"),
    ]

    for term, context in tests_fail:
        with pytest.raises(Exception):
            type_check(TypedTerm.parse(term), Context.parse(context))
        

if __name__ == '__main__':
    test_Type()
    test_TypedTerm()
    test_TypedTerm_parse()
    test_Type_apply()
    test_type_check()