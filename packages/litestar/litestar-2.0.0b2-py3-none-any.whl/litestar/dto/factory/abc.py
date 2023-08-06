from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from litestar.dto.interface import ConnectionContext, DTOInterface
from litestar.enums import RequestEncodingType
from litestar.typing import ParsedType

from ._backends import MsgspecDTOBackend, PydanticDTOBackend
from ._backends.abc import BackendContext
from .config import DTOConfig
from .exc import InvalidAnnotation
from .utils import (
    parse_configs_from_annotation,
    resolve_generic_wrapper_type,
    resolve_model_type,
)

if TYPE_CHECKING:
    from typing import Any, ClassVar, Collection, Generator

    from typing_extensions import Self

    from litestar._openapi.schema_generation import SchemaCreator
    from litestar.dto.interface import HandlerContext
    from litestar.dto.types import ForType
    from litestar.openapi.spec import Reference, Schema
    from litestar.types.serialization import LitestarEncodableType

    from ._backends import AbstractDTOBackend
    from .data_structures import FieldDefinition

__all__ = ("AbstractDTOFactory",)

T = TypeVar("T")


class AbstractDTOFactory(DTOInterface, Generic[T], metaclass=ABCMeta):
    """Base class for DTO types."""

    __slots__ = ("connection_context",)

    config: ClassVar[DTOConfig]
    """Config objects to define properties of the DTO."""
    model_type: ClassVar[type[Any]]
    """If ``annotation`` is an iterable, this is the inner type, otherwise will be the same as ``annotation``."""

    _type_backend_map: ClassVar[dict[tuple[ForType, ParsedType, RequestEncodingType | str | None], AbstractDTOBackend]]
    _handler_backend_map: ClassVar[dict[tuple[ForType, str], AbstractDTOBackend]]

    def __init__(self, connection_context: ConnectionContext) -> None:
        """Create an AbstractDTOFactory type.

        Args:
            connection_context: A :class:`ConnectionContext <.ConnectionContext>` instance, which provides
                information about the connection.
        """
        self.connection_context = connection_context

    def __class_getitem__(cls, annotation: Any) -> type[Self]:
        parsed_type = ParsedType(annotation)

        if (parsed_type.is_optional and len(parsed_type.args) > 2) or (
            parsed_type.is_union and not parsed_type.is_optional
        ):
            raise InvalidAnnotation(
                "Unions are currently not supported as type argument to DTO. Want this? Open an issue."
            )

        if parsed_type.is_forward_ref:
            raise InvalidAnnotation("Forward references are not supported as type argument to DTO")

        # if a configuration is not provided, and the type narrowing is a type var, we don't want to create a subclass
        configs = parse_configs_from_annotation(parsed_type)
        if parsed_type.is_type_var and not configs:
            return cls

        if configs:
            # provided config is always preferred
            config = configs[0]
        elif hasattr(cls, "config"):
            # if no config is provided, but the class has one assigned, use that
            config = cls.config
        else:
            # otherwise, create a new config
            config = DTOConfig()

        cls_dict: dict[str, Any] = {"config": config, "_type_backend_map": {}, "_handler_backend_map": {}}
        if not parsed_type.is_type_var:
            cls_dict.update(model_type=parsed_type.annotation)

        return type(f"{cls.__name__}[{annotation}]", (cls,), cls_dict)

    def builtins_to_data_type(self, builtins: Any) -> Any:
        """Coerce the unstructured data into the data type."""
        backend = self._get_backend("data", self.connection_context.handler_id)
        return backend.populate_data_from_builtins(builtins, self.connection_context)

    def bytes_to_data_type(self, raw: bytes) -> Any:
        """Return the data held by the DTO."""
        backend = self._get_backend("data", self.connection_context.handler_id)
        return backend.populate_data_from_raw(raw, self.connection_context)

    def data_to_encodable_type(self, data: T | Collection[T]) -> LitestarEncodableType:
        backend = self._get_backend("return", self.connection_context.handler_id)
        return backend.encode_data(data, self.connection_context)

    @classmethod
    @abstractmethod
    def generate_field_definitions(cls, model_type: type[Any]) -> Generator[FieldDefinition, None, None]:
        """Generate ``FieldDefinition`` instances from ``model_type``.

        Yields:
            ``FieldDefinition`` instances.
        """

    @classmethod
    @abstractmethod
    def detect_nested_field(cls, parsed_type: ParsedType) -> bool:
        """Return ``True`` if ``field_definition`` represents a nested model field.

        Args:
            parsed_type: inspect type to determine if field represents a nested model.

        Returns:
            ``True`` if ``parsed_type`` represents a nested model field.
        """

    @classmethod
    def on_registration(cls, handler_context: HandlerContext) -> None:
        """Called each time the DTO type is encountered during signature modelling.

        Args:
            handler_context: A :class:`HandlerContext <.HandlerContext>` instance. Provides information about the
                handler and application of the DTO.
        """
        parsed_type = handler_context.parsed_type
        model_type = resolve_model_type(parsed_type)
        wrapper_attribute_name: str | None = None

        if not model_type.is_subclass_of(cls.model_type):
            resolved_generic_result = resolve_generic_wrapper_type(model_type, cls.model_type)
            if resolved_generic_result is not None:
                model_type, parsed_type, wrapper_attribute_name = resolved_generic_result
            else:
                raise InvalidAnnotation(
                    f"DTO narrowed with '{cls.model_type}', handler type is '{parsed_type.annotation}'"
                )

        key = (handler_context.dto_for, parsed_type, handler_context.request_encoding_type)
        backend = cls._type_backend_map.get(key)
        if backend is None:
            backend_type: type[AbstractDTOBackend]
            if handler_context.request_encoding_type in {
                RequestEncodingType.URL_ENCODED,
                RequestEncodingType.MULTI_PART,
            }:
                backend_type = PydanticDTOBackend
            else:
                backend_type = MsgspecDTOBackend

            backend_context = BackendContext(
                dto_config=cls.config,
                dto_for=handler_context.dto_for,
                parsed_type=parsed_type,
                field_definition_generator=cls.generate_field_definitions,
                is_nested_field_predicate=cls.detect_nested_field,
                model_type=model_type.annotation,
                wrapper_attribute_name=wrapper_attribute_name,
            )
            backend = cls._type_backend_map.setdefault(key, backend_type(backend_context))
        cls._handler_backend_map[(handler_context.dto_for, handler_context.handler_id)] = backend

    @classmethod
    def create_openapi_schema(
        cls, dto_for: ForType, handler_id: str, schema_creator: SchemaCreator
    ) -> Reference | Schema:
        """Create an OpenAPI request body.

        Returns:
            OpenAPI request body.
        """
        return cls._get_backend(dto_for, handler_id).create_openapi_schema(schema_creator)

    @classmethod
    def _get_backend(cls, dto_for: ForType, handler_id: str) -> AbstractDTOBackend:
        """Return the backend for the handler/dto_for combo."""
        return cls._handler_backend_map[(dto_for, handler_id)]
