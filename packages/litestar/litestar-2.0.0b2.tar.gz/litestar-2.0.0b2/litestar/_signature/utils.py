from __future__ import annotations

from inspect import getmembers, isclass
from typing import TYPE_CHECKING, Any, Literal, cast

import pydantic

from litestar._signature.models.pydantic_signature_model import PydanticSignatureModel
from litestar.constants import SKIP_VALIDATION_NAMES
from litestar.exceptions import ImproperlyConfiguredException
from litestar.params import DependencyKwarg
from litestar.types import AnyCallable, Empty
from litestar.utils.helpers import unwrap_partial
from litestar.utils.predicates import is_attrs_class

pydantic_types: tuple[Any, ...] = tuple(
    cls for _, cls in getmembers(pydantic.types, isclass) if "pydantic.types" in repr(cls)
)


if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    from litestar._signature.models.base import SignatureModel
    from litestar.utils.signature import ParsedParameter, ParsedSignature

__all__ = (
    "create_signature_model",
    "get_signature_model",
)


SignatureModelType: TypeAlias = "type[SignatureModel]"


def create_signature_model(
    dependency_name_set: set[str],
    fn: AnyCallable,
    preferred_validation_backend: Literal["pydantic", "attrs"],
    parsed_signature: ParsedSignature,
    has_data_dto: bool = False,
) -> type[SignatureModel]:
    """Create a model for a callable's signature. The model can than be used to parse and validate before passing it to
    the callable.

    Args:
        dependency_name_set: A set of dependency names
        fn: A callable.
        preferred_validation_backend: Validation/Parsing backend to prefer, if installed
        parsed_signature: A parsed signature for the handler/dependency function.
        has_data_dto: Is a data DTO defined for the handler?

    Returns:
        A signature model.
    """

    unwrapped_fn = cast("AnyCallable", unwrap_partial(fn))
    fn_name = getattr(fn, "__name__", "anonymous")
    fn_module = getattr(fn, "__module__", None)

    if fn_name == "<lambda>":
        fn_name = "anonymous"

    dependency_names = _validate_dependencies(
        dependency_name_set=dependency_name_set, fn=unwrapped_fn, parsed_signature=parsed_signature
    )

    model_class = _get_signature_model_type(
        preferred_validation_backend=preferred_validation_backend, parsed_signature=parsed_signature
    )

    type_overrides = _create_type_overrides(parsed_signature, has_data_dto)

    return model_class.create(
        fn_name=fn_name,
        fn_module=fn_module,
        parsed_signature=parsed_signature,
        dependency_names={*dependency_name_set, *dependency_names},
        type_overrides=type_overrides,
    )


def get_signature_model(value: Any) -> type[SignatureModel]:
    """Retrieve and validate the signature model from a provider or handler."""
    try:
        return cast(SignatureModelType, value.signature_model)
    except AttributeError as e:  # pragma: no cover
        raise ImproperlyConfiguredException(f"The 'signature_model' attribute for {value} is not set") from e


def _any_attrs_annotation(parsed_signature: ParsedSignature) -> bool:
    for parameter in parsed_signature.parameters.values():
        parsed_type = parameter.parsed_type
        if any(is_attrs_class(t.annotation) for t in parsed_type.inner_types) or is_attrs_class(parsed_type.annotation):
            return True
    return False


def _create_type_overrides(parsed_signature: ParsedSignature, has_data_dto: bool) -> dict[str, Any]:
    type_overrides = {}
    for parameter in parsed_signature.parameters.values():
        if _should_skip_validation(parameter):
            type_overrides[parameter.name] = Any
        if has_data_dto and "data" in parsed_signature.parameters:
            type_overrides["data"] = Any
    return type_overrides


def _get_signature_model_type(
    preferred_validation_backend: Literal["pydantic", "attrs"],
    parsed_signature: ParsedSignature,
) -> type[SignatureModel]:
    if preferred_validation_backend == "attrs" or _any_attrs_annotation(parsed_signature):
        from litestar._signature.models.attrs_signature_model import AttrsSignatureModel

        return AttrsSignatureModel
    return PydanticSignatureModel


def _should_skip_validation(parameter: ParsedParameter) -> bool:
    """Whether the parameter should skip validation.

    Returns:
        A boolean indicating whether the parameter should be validated.
    """
    return parameter.name in SKIP_VALIDATION_NAMES or (
        isinstance(parameter.default, DependencyKwarg) and parameter.default.skip_validation
    )


def _validate_dependencies(
    dependency_name_set: set[str], fn: AnyCallable, parsed_signature: ParsedSignature
) -> set[str]:
    """Validate dependencies of ``parsed_signature``.

    Args:
        dependency_name_set: A set of dependency names
        fn: A callable.
        parsed_signature: A parsed signature.

    Returns:
        A set of validated dependency names.
    """
    fn_name = getattr(fn, "__name__", "anonymous")

    dependency_names: set[str] = set()

    for parameter in parsed_signature.parameters.values():
        if isinstance(parameter.default, DependencyKwarg) and parameter.name not in dependency_name_set:
            if not parameter.parsed_type.is_optional and parameter.default.default is Empty:
                raise ImproperlyConfiguredException(
                    f"Explicit dependency '{parameter.name}' for '{fn_name}' has no default value, "
                    f"or provided dependency."
                )
            dependency_names.add(parameter.name)
    return dependency_names
