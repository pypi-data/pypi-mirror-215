# pymolecule-parser: A parser for a molecule formula that supports nested brackets

[![pymolecule-parser-test](https://github.com/kohei-noda-qcrg/pymolecule-parser/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/kohei-noda-qcrg/pymolecule-parser/actions/workflows/test.yml)

## Installation

```bash
pip install pymolecule-parser
```

## Usage

- pymolecule_parser.parse returns a dictionary of atoms and their numbers. (type: dict[str, int])

```python
from pymolecule_parser import parse

dict_1 = parse("H2O") # {'H': 2, 'O': 1}
dict_2 = parse("3H2O") # {'H': 6, 'O': 3}
dict_3 = parse("H2O2(OH)2") # {'H': 4, 'O': 4}
dict_4 = parse("[Co(NH3)6]Cl3") # {'Co': 1, 'N': 6, 'H': 18, 'Cl': 3}
```

## Options

- strict_mode
  - If `strict_mode` is `True`, the parser expects all atoms in the argument to be from hydrogen (H) to oganeson (Og), otherwise raises an exception
  - If `strict_mode` is `False`, the parser parses arguments even if they are not existing atoms if they satisfy the rules for writing atoms (first letter is uppercase, subsequent letters are lowercase)
  - Default: `False` (non-strict mode)

If you want to use strict mode, please use the following code.

```python
from pymolecule_parser import parse

dict_1 = parse("H2O", strict_mode=True) # {'H': 2, 'O': 1}

```


## Limitations
The following notations are not supported.
- Ion notations
  - For example, `[Cu(NH3)4]2+` is not supported. Use `Cu(NH3)4` instead.
- middle dot `·`
  - For example, `CuSO4·5H2O` is not supported. Use `CuSO4(H2O)5` instead.

## License

Apache License 2.0

## Author

Kohei Noda
