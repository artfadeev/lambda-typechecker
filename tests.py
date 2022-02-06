from main import *

def test_Type():
    t1 = Type('implication', Type('base', 'a'), 
                             Type('implication', Type('base', 'b'),
                                                 Type('base', 'c')))
    t2 = Type.implication(Type.base('a'), 
                          Type.implication(Type.base('b'),
                                           Type.base('c')))
    t3 = parse_type('a->(b->c)')
    t4 = parse_type('(((((a))->((b)->c))))')

    assert t1 == t2
    assert t1 == t3
    assert t1 == t4

def test_TypedTerm():
    tt1 = TypedTerm.abstraction(
            TypedTerm.variable('a', parse_type('p->q')),
            TypedTerm.application(
                TypedTerm.variable('a'),
                TypedTerm.variable('b', parse_type('p'))
            )
        )
    assert str(tt1)=='(La:(p->q).(a b:p))'

def test_TypedTerm_parse():
    tt1 = TypedTerm.abstraction(
            TypedTerm.variable('a', parse_type('p->q')),
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
    t1 = parse_type('a->((c->b)->c)')
    t2 = parse_type('a')
    t3 = parse_type('c->b')

    assert t1.apply(t2).apply(t3)==parse_type('c')

    try:
        t3.apply(t2)
    except Exception:
        pass
    else:
        raise Exception('should have been error')

if __name__ == '__main__':
    test_Type()
    test_TypedTerm()
    test_TypedTerm_parse()
    test_Type_apply()
