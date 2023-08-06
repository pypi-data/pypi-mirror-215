from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Sequence, TypedDict, cast

from litestar.enums import ScopeType
from litestar.exceptions import InternalServerException, ValidationException
from litestar.params import ParameterKwarg

if TYPE_CHECKING:
    from typing_extensions import NotRequired

    from litestar._signature.field import SignatureField
    from litestar.connection import ASGIConnection
    from litestar.utils.signature import ParsedSignature

__all__ = ("SignatureModel",)


class ErrorMessage(TypedDict):
    # key may not be set in some cases, like when a query param is set but
    # doesn't match the required length during `attrs` validation
    # in this case, we don't show a key at all as it will be empty
    key: NotRequired[str]
    message: str
    source: NotRequired[Literal["cookie", "body", "header", "query"]]


class SignatureModel(ABC):
    """Base model for Signature modelling."""

    dependency_name_set: ClassVar[set[str]]
    return_annotation: ClassVar[Any]
    fields: ClassVar[dict[str, SignatureField]]

    @classmethod
    def _create_exception(cls, connection: ASGIConnection, messages: list[ErrorMessage]) -> Exception:
        """Create an exception class - either a ValidationException or an InternalServerException, depending on whether
            the failure is in client provided values or injected dependencies.

        Args:
            connection: An ASGI connection instance.
            messages: A list of error messages.

        Returns:
            An Exception
        """
        method = connection.method if hasattr(connection, "method") else ScopeType.WEBSOCKET  # pyright: ignore
        if client_errors := [
            err_message
            for err_message in messages
            if ("key" in err_message and err_message["key"] not in cls.dependency_name_set) or "key" not in err_message
        ]:
            return ValidationException(detail=f"Validation failed for {method} {connection.url}", extra=client_errors)
        return InternalServerException(
            detail=f"A dependency failed validation for {method} {connection.url}", extra=messages
        )

    @classmethod
    def _build_error_message(cls, keys: Sequence[str], exc_msg: str, connection: ASGIConnection) -> ErrorMessage:
        """Build an error message.

        Args:
            keys: A list of keys.
            exc_msg: A message.
            connection: An ASGI connection instance.

        Returns:
            An ErrorMessage
        """

        message: ErrorMessage = {"message": exc_msg}

        if len(keys) > 1:
            key_start = 0

            if keys[0] == "data":
                key_start = 1
                message["source"] = "body"

            message["key"] = ".".join(keys[key_start:])
        elif keys:
            key = keys[0]
            message["key"] = key

            if key in connection.query_params:
                message["source"] = cast("Literal['cookie', 'body', 'header', 'query']", "query")

            elif key in cls.fields and isinstance(cls.fields[key].kwarg_model, ParameterKwarg):
                if cast(ParameterKwarg, cls.fields[key].kwarg_model).cookie:
                    source = "cookie"
                elif cast(ParameterKwarg, cls.fields[key].kwarg_model).header:
                    source = "header"
                else:
                    source = "query"
                message["source"] = cast("Literal['cookie', 'body', 'header', 'query']", source)

        return message

    @classmethod
    @abstractmethod
    def parse_values_from_connection_kwargs(cls, connection: ASGIConnection, **kwargs: Any) -> dict[str, Any]:
        """Extract values from the connection instance and return a dict of parsed values.

        Args:
            connection: The ASGI connection instance.
            **kwargs: A dictionary of kwargs.

        Raises:
            ValidationException: If validation failed.
            InternalServerException: If another exception has been raised.

        Returns:
            A dictionary of parsed values
        """
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Normalize access to the signature model's dictionary method, because different backends use different methods
        for this.

        Returns: A dictionary of string keyed values.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def populate_signature_fields(cls) -> None:
        """Populate the class signature fields.

        Returns:
            None.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create(
        cls,
        fn_name: str,
        fn_module: str | None,
        parsed_signature: ParsedSignature,
        dependency_names: set[str],
        type_overrides: dict[str, Any],
    ) -> type[SignatureModel]:
        """Create a SignatureModel.

        Args:
            fn_name: Name of the callable.
            fn_module: Name of the function's module, if any.
            parsed_signature: A parsed signature.
            dependency_names: A set of dependency names.
            type_overrides: A dictionary of type overrides, either will override a parameter type with a type derived
                from a plugin, or set the type to ``Any`` if validation should be skipped for the parameter.

        Returns:
            The created SignatureModel.
        """
        raise NotImplementedError
