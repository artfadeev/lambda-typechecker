import pytest
from type_checker.types import Type, Implication, Base, Context
from type_checker.terms import TypedTerm, Variable, Application, Abstraction
from type_checker.type_checker import type_check
from type_checker.parser import Scanner, TokenType

class TestParser:
    def test_Scanner(self):
        # Check whether exceptions are raised
        Scanner('hello world').scan()
        Scanner('lambda x....y HGH -> ->->::').scan()

        tests = [
            ('x y z', 
                (TokenType.VARIABLE, TokenType.VARIABLE, TokenType.VARIABLE)),
            ('   a->b   ',
                (TokenType.VARIABLE, TokenType.ARROW, TokenType.VARIABLE)),
            ('  (.:->',
                (TokenType.BRACKET_OPEN, TokenType.DOT, TokenType.COLON,
                    TokenType.ARROW)),
        ]

        for source, expected_token_types in tests:
            tokens = Scanner(source).scan()
            assert len(tokens)==len(expected_token_types)
            for token, _type in zip(tokens, expected_token_types):
                assert token.type==_type

class TestType:
    def test_constuctors(self):
        t1 = Implication(Base('a'), Implication(Base('b'), Base('c')))
        t2 = Type.parse('a->(b->c)')
        t3 = Type.parse('(((((a))->((b)->c))))')

        assert t1 == t2
        assert t1 == t3

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
        tt1 = Abstraction('a', Type.parse('p->q'),
                Application(Variable('a'), Variable('b')))
        assert str(tt1)=='(La:(p->q).(a b))'

    def test_parse(self):
        tt1 = Abstraction('a', Type.parse('p->q'),
                Application(Variable('a'), Variable('b')))

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