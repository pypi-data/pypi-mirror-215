import inspect
from typing import Any, Callable, Optional

from typing_extensions import Annotated, assert_never, get_args, get_origin

from fast_depends._compat import create_model
from fast_depends.core.model import CallModel
from fast_depends.dependencies import Depends
from fast_depends.library import CustomField
from fast_depends.utils import get_typed_signature, is_coroutine_callable

CUSTOM_ANNOTATIONS = (Depends, CustomField)


def build_call_model(
    call: Callable[..., Any],
    *,
    cast: bool = True,
    use_cache: bool = True,
    is_sync: Optional[bool] = None,
) -> CallModel:
    name = getattr(call, "__name__", type(call).__name__)

    is_call_async = is_coroutine_callable(call)
    if is_sync is None:
        is_sync = not is_call_async
    else:
        assert not (
            is_sync and is_call_async
        ), f"You cannot use async dependency `{name}` at sync main"

    typed_params, return_annotation = get_typed_signature(call)

    class_fields = {}
    dependencies = {}
    custom_fields = {}
    for param in typed_params:
        dep: Optional[Depends] = None
        custom: Optional[CustomField] = None

        if param.annotation is inspect._empty:
            annotation = Any

        elif get_origin(param.annotation) is Annotated:
            annotated_args = get_args(param.annotation)
            type_annotation = annotated_args[0]
            custom_annotations = [
                arg for arg in annotated_args[1:] if isinstance(arg, CUSTOM_ANNOTATIONS)
            ]

            assert (
                len(custom_annotations) <= 1
            ), f"Cannot specify multiple `Annotated` Custom arguments for `{param.name}`!"

            next_custom = next(iter(custom_annotations), None)
            if next_custom is not None:
                if isinstance(next_custom, Depends):
                    dep = next_custom
                elif isinstance(next_custom, CustomField):
                    custom = next_custom
                else:  # pragma: no cover
                    assert_never()

                annotation = type_annotation
            else:
                annotation = param.annotation
        else:
            annotation = param.annotation

        default = param.default
        if dep or isinstance(default, Depends):
            dep = dep or default

            dependencies[param.name] = build_call_model(
                dep.call,
                cast=dep.cast,
                use_cache=dep.use_cache,
                is_sync=is_sync,
            )

            if dep.cast is True:
                class_fields[param.name] = (annotation, ...)

        elif custom or isinstance(default, CustomField):
            custom = custom or default
            assert not (
                is_sync and is_coroutine_callable(custom.use)
            ), f"You cannot use async custom field `{type(custom).__name__}` at sync `{name}`"

            custom.set_param_name(param.name)
            custom_fields[param.name] = custom

            if custom.cast is False:
                annotation = Any

            if custom.required:
                class_fields[param.name] = (annotation, ...)
            else:
                class_fields[param.name] = (Optional[annotation], None)

        elif default is inspect._empty:
            class_fields[param.name] = (annotation, ...)

        else:
            class_fields[param.name] = (annotation, default)

    if cast and return_annotation is not inspect._empty:
        response_model = create_model(
            "ResponseModel", response=(return_annotation, ...)
        )
    else:
        response_model = None

    func_model = create_model(name, **class_fields)

    return CallModel(
        call=call,
        model=func_model,
        response_model=response_model,
        cast=cast,
        use_cache=use_cache,
        is_async=is_call_async,
        dependencies=dependencies,
        custom_fields=custom_fields,
    )
