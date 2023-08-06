from __future__ import annotations as _annotations

import typing as t
from inspect import Parameter
from inspect import signature

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import create_model
from pydantic.v1.decorator import ALT_V_ARGS
from pydantic.v1.decorator import ALT_V_KWARGS
from pydantic.v1.decorator import V_DUPLICATE_KWARGS
from pydantic.v1.decorator import V_POSITIONAL_ONLY_NAME
from pydantic.v1.decorator import validate_arguments
from pydantic.v1.errors import ConfigError
from pydantic.v1.typing import get_all_type_hints
from pydantic.v1.utils import to_camel
from pydantic_settings import BaseSettings


def _build_field_definitions(function: t.Callable[..., t.Any]):
    # `pydantic.v1.decorator.ValidatedFunction.__init__`
    parameters: t.Mapping[str, Parameter] = signature(function).parameters

    if parameters.keys() & {
        ALT_V_ARGS,
        ALT_V_KWARGS,
        V_POSITIONAL_ONLY_NAME,
        V_DUPLICATE_KWARGS,
    }:
        raise ConfigError(
            f'"{ALT_V_ARGS}", "{ALT_V_KWARGS}", "{V_POSITIONAL_ONLY_NAME}" and "{V_DUPLICATE_KWARGS}" '
            f'are not permitted as argument names when using the "{validate_arguments.__name__}" decorator'
        )

    v_args_name = 'args'
    v_kwargs_name = 'kwargs'

    type_hints = get_all_type_hints(function)
    takes_args = False
    takes_kwargs = False
    fields: t.Dict[str, t.Tuple[t.Any, t.Any]] = {}
    for i, (name, p) in enumerate(parameters.items()):
        if p.annotation is p.empty:
            annotation = t.Any
        else:
            annotation = type_hints[name]

        default = ... if p.default is p.empty else p.default
        if p.kind == Parameter.POSITIONAL_ONLY:
            fields[name] = annotation, default
            # ! ignore:
            # fields[V_POSITIONAL_ONLY_NAME] = t.List[str], None
        elif p.kind == Parameter.POSITIONAL_OR_KEYWORD:
            fields[name] = annotation, default
            # ! ignore:
            # fields[V_DUPLICATE_KWARGS] = t.List[str], None
        elif p.kind == Parameter.KEYWORD_ONLY:
            fields[name] = annotation, default
        elif p.kind == Parameter.VAR_POSITIONAL:
            v_args_name = name
            fields[name] = t.Tuple[annotation, ...], None
            takes_args = True
        else:
            assert p.kind == Parameter.VAR_KEYWORD, p.kind
            v_kwargs_name = name
            fields[name] = t.Dict[str, annotation], None  # type: ignore
            takes_kwargs = True

    # these checks avoid a clash between "args" and a field with that name
    if not takes_args and v_args_name in fields:
        v_args_name = ALT_V_ARGS

    # same with "kwargs"
    if not takes_kwargs and v_kwargs_name in fields:
        v_kwargs_name = ALT_V_KWARGS

    if not takes_args:
        # we add the field so validation below can raise the correct exception
        # ! ignore:
        # fields[v_args_name] = t.List[t.Any], None
        ...

    if not takes_kwargs:
        # same with kwargs
        # ! ignore:
        # fields[v_kwargs_name] = t.Dict[t.Any, t.Any], None
        ...
    return fields


def create_settings(
    function: t.Callable[..., t.Any],
    *,
    config: t.Optional[ConfigDict] = None,
    base: type[BaseModel] = BaseSettings,
    module=__name__,
    validators: t.Optional[dict[str, classmethod[t.Any, t.Any, t.Any]]] = None,
):
    _field_definitions = _build_field_definitions(function)
    return create_model(
        to_camel(function.__name__) + 'Signature' + base.__name__.replace('Base', ''),
        __config__=config,
        __base__=base,
        __module__=module,
        __validators__=validators,
        **_field_definitions,
    )
