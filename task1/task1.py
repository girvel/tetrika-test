import functools
import inspect
from typing import Any, Callable


def strict(func: Callable[..., Any]):
    """Validates parameter types in runtime according to annotations.

    Allowed types: bool, int, float, str
    """

    # inspect is better than annotations: it resolves "" expressions
    annotations = inspect.get_annotations(func, eval_str=True)
    if 'return' in annotations:
        del annotations['return']

    assert all(
        t in (bool, int, float, str) for t in annotations.values()
    ), "Unsupported type in annotation"

    sig = inspect.signature(func)
    assert not any(
        param.kind in (param.VAR_KEYWORD, param.VAR_POSITIONAL)
        for param in sig.parameters.values()
    ), "@strict function must not have *args and **kwargs"

    assert len(sig.parameters) == len(annotations), "All parameters should be annotated"

    @functools.wraps(func)
    def result(*args, **kwargs):
        wrong_args = []
        for i, (arg_name, arg_type) in enumerate(annotations.items()):
            if i < len(args):
                value = args[i]
            else:
                value = kwargs[arg_name]

            if not isinstance(value, arg_type):
                wrong_args.append((arg_name, type(value)))

        if len(wrong_args) > 0:
            wrong_args = "; ".join(
                f"{name} expected to be {annotations[name]}, got {type_} instead"
                for name, type_ in wrong_args
            )
            raise TypeError(f"Mismatching types for arguments: {wrong_args}")

        return func(*args, **kwargs)

    return result
