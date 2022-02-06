from main import Type, parse_type

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
    assert str(tt1)=='La:(p->q).(a b:p)'


if __name__ == '__main__':
    test_Type()
    test_TypedTerm()
