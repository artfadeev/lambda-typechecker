# Lambda type checker

This project provides type checker for System F (polymorphic lambda calculus).

## Installation and usage

```bash
# installation
git clone https://github.com/artfadeev/lambda-typechecker
cd lambda-typechecker

# running
python -m type_checker <term>
``` 

Syntax:
* types' names should contain only letters
* `(type 1) -> (type 2)` for applications
* variables' names should contain only letters (except `λ`)
* `(<term 1> <term 2>)` for applications
* `(lambda <variable name>: <variable type>. <term>)` for abstractions. (you can use `λ` symbol instead of `lambda` keyword)
* `<term> [<type>]` for type applications
* `type_lambda <variable_name>: <term>` for type abstractions

Example:
```bash
$ python -m type_checker 'lambda x: (a->b)->a. lambda y: a->a->b. x lambda z: a. y z z'
Type check successful
Term's type (((a->b)->a)->((a->(a->b))->a))
```

system f example
```bash
$ python -m type_checker 'lambda x: forall a.a.x'
Type check successful
Term's type ((forall a. a)->(forall a. a))
```

As you can see, brackets can be omitted. Note that application is left-associative and abstractions spread right as much as they can.

By default, type is checked in empty context. However you can specify context by passing comma-separated pairs `variable:type` into the `--context` parameter:

```bash
$ python -m type_checker 'x y z' --context 'x:a->b->c, y:a, z:b'
Type check successful
Term's type c
``` 

## Development

Project's structure:
```
├── dev-requirements.txt 
├── LICENSE
├── README.md
├── tests.py
└── type_checker
    ├── __main__.py         # CLI 
    ├── parser.py           # Scanner and Parser of terms and types
    ├── terms.py            # Data structures for terms
    ├── type_checker.py     # Type checker itself
    └── types.py            # Data structures for types and context
```

You can run tests:
```bash
python -m pip install -r dev-requirements.txt   # or just install pytest
pytest tests.py
```