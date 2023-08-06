from src.pymolecule_parser import parse
import pytest


def test_parser():
    testcases = {
        "H2O": {"H": 2, "O": 1},
        "C6H12O6": {"C": 6, "H": 12, "O": 6},
        "3H2O": {"H": 6, "O": 3},
        "[Co(NH3)6]Cl3": {"Co": 1, "N": 6, "H": 18, "Cl": 3},
        "XyzA4": {"Xyz": 1, "A": 4},
        "H3C-OH": {"C": 1, "H": 4, "O": 1},
        "C6H5C≡N": {"C": 7, "H": 5, "N": 1},
    }
    for key, value in testcases.items():
        assert parse(key) == value


def test_parser_strict():
    testcases = {
        "H2O": {"H": 2, "O": 1},
        "C6H12O6": {"C": 6, "H": 12, "O": 6},
        "3H2O": {"H": 6, "O": 3},
        "[Co(NH3)6]Cl3": {"Co": 1, "N": 6, "H": 18, "Cl": 3},
        "H3C-OH": {"C": 1, "H": 4, "O": 1},
        "C6H5C≡N": {"C": 7, "H": 5, "N": 1},
    }
    for key, value in testcases.items():
        assert parse(key, strict_mode=True) == value


def test_parser_strict_invalid():
    testcases = {
        # Expect to raise ValueError
        "XyzA4": ValueError()
    }
    for key, value in testcases.items():
        with pytest.raises(ValueError) as e:
            parse(key, strict_mode=True)

        exception_raised = e.value
        assert isinstance(exception_raised, type(value))
