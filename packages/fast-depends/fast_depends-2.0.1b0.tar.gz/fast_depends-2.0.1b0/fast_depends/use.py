from contextlib import AsyncExitStack, ExitStack
from functools import wraps
from typing import Any, Awaitable, Callable, Optional, Union

from typing_extensions import ParamSpec, TypeVar

from fast_depends.core import CallModel, build_call_model
from fast_depends.dependencies import dependency_provider, model

P = ParamSpec("P")
T = TypeVar("T")


def Depends(
    dependency: Union[Callable[P, T], Callable[P, Awaitable[T]]],
    *,
    use_cache: bool = True,
    cast: bool = True,
) -> Any:  # noqa: N802
    return model.Depends(call=dependency, use_cache=use_cache, cast=cast)


def inject(
    func: Optional[Union[Callable[P, T], Callable[P, Awaitable[T]]]] = None,
    *,
    dependency_overrides_provider: Optional[Any] = dependency_provider,
    wrap_dependant: Callable[[CallModel], CallModel] = lambda x: x,
) -> Union[Callable[P, T], Callable[P, Awaitable[T]]]:
    decorator = _wrap_inject(
        dependency_overrides_provider=dependency_overrides_provider,
        wrap_dependant=wrap_dependant,
    )

    if func is None:
        return decorator

    else:
        return decorator(func)


def _wrap_inject(
    dependency_overrides_provider: Optional[Any],
    wrap_dependant: Callable[[CallModel], CallModel],
) -> Callable[
    [Union[Callable[P, T], Callable[P, Awaitable[T]]]],
    Union[Callable[P, T], Callable[P, Awaitable[T]]],
]:
    if (
        dependency_overrides_provider
        and getattr(dependency_overrides_provider, "dependency_overrides", None)
        is not None
    ):
        overrides = dependency_overrides_provider.dependency_overrides
    else:
        overrides = None

    def func_wrapper(
        func: Union[Callable[P, T], Callable[P, Awaitable[T]]]
    ) -> Union[Callable[P, T], Callable[P, Awaitable[T]]]:
        model = wrap_dependant(build_call_model(func))

        if model.is_async:

            @wraps(func)
            async def injected_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                async with AsyncExitStack() as stack:
                    return await model.asolve(
                        *args,
                        stack=stack,
                        dependency_overrides=overrides,
                        cache_dependencies={},
                        **kwargs,
                    )

        else:

            @wraps(func)
            def injected_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                with ExitStack() as stack:
                    return model.solve(
                        *args,
                        stack=stack,
                        dependency_overrides=overrides,
                        cache_dependencies={},
                        **kwargs,
                    )

        return wraps(func)(injected_wrapper)

    return func_wrapper
