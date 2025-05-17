from task1 import strict


@strict
def sum_two(a: int, b: "int") -> int:
    return a + b


def test_correctly_annotated():
    assert sum_two(1, 2) == 3
    assert sum_two(3, b=4) == 7
    try:
        sum_two(1, 2.4)
        assert False
    except TypeError:
        pass


@strict
def example(a: bool, b: int, c: float, d: str):
    return f'a={a} b={b} c={c} d={d}'


def test_all_annotation_types():
    assert example(True, 1, 2.2, "hi") == "a=True b=1 c=2.2 d=hi"


def test_unsupported_annotation_type():
    try:
        @strict
        def _(_: list):
            ...

        assert False
    except AssertionError:
        pass


def test_unsupported_args():
    try:
        @strict
        def _(*_: int):
            ...

        assert False
    except AssertionError:
        pass


def test_unsupported_kwargs():
    try:
        @strict
        def _(**_: int):
            ...

        assert False
    except AssertionError:
        pass


def test_missing_annotation():
    try:
        @strict
        def _(_):
            ...

        assert False
    except AssertionError:
        pass
