from main import *

def test_Type():
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

def test_TypedTerm():
    tt1 = TypedTerm.abstraction(
            TypedTerm.variable('a', Type.parse('p->q')),
            TypedTerm.application(
                TypedTerm.variable('a'),
                TypedTerm.variable('b', Type.parse('p'))
            )
        )
    assert str(tt1)=='(La:(p->q).(a b:p))'

def test_TypedTerm_parse():
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

def test_Type_apply():
    t1 = Type.parse('a->((c->b)->c)')
    t2 = Type.parse('a')
    t3 = Type.parse('c->b')

    assert t1.apply(t2).apply(t3)==Type.parse('c')

    try:
        t3.apply(t2)
    except Exception:
        pass
    else:
        raise Exception('should have been error')

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
        try:
            type_check(TypedTerm.parse(term),
                    Context.parse(context))
        except Exception:
            pass
        else:
            raise Exception("should have been error")

if __name__ == '__main__':
    test_Type()
    test_TypedTerm()
    test_TypedTerm_parse()
    test_Type_apply()
    test_type_check()