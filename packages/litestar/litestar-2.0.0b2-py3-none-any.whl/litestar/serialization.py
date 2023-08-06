from __future__ import annotations

from collections import deque
from decimal import Decimal
from functools import partial
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from pathlib import Path, PurePath
from re import Pattern
from typing import TYPE_CHECKING, Any, Callable, Mapping, TypeVar, overload

import msgspec
from pydantic import (
    BaseModel,
    ByteSize,
    ConstrainedBytes,
    ConstrainedDate,
    NameEmail,
    SecretField,
    StrictBool,
)
from pydantic.color import Color
from pydantic.json import decimal_encoder

from litestar.enums import MediaType
from litestar.exceptions import SerializationException
from litestar.types import Empty, Serializer

if TYPE_CHECKING:
    from litestar.types import TypeEncodersMap

__all__ = (
    "dec_hook",
    "decode_json",
    "decode_media_type",
    "decode_msgpack",
    "default_serializer",
    "encode_json",
    "encode_msgpack",
    "get_serializer",
)

T = TypeVar("T")


def _enc_base_model(model: BaseModel) -> Any:
    return model.dict()


def _enc_byte_size(bytes_: ByteSize) -> int:
    return bytes_.real


def _enc_constrained_bytes(bytes_: ConstrainedBytes) -> str:
    return bytes_.decode("utf-8")


def _enc_constrained_date(date: ConstrainedDate) -> str:
    return date.isoformat()


def _enc_pattern(pattern: Pattern) -> Any:
    return pattern.pattern


DEFAULT_TYPE_ENCODERS: TypeEncodersMap = {
    Path: str,
    PurePath: str,
    # pydantic specific types
    BaseModel: _enc_base_model,
    ByteSize: _enc_byte_size,
    NameEmail: str,
    Color: str,
    SecretField: str,
    ConstrainedBytes: _enc_constrained_bytes,
    ConstrainedDate: _enc_constrained_date,
    IPv4Address: str,
    IPv4Interface: str,
    IPv4Network: str,
    IPv6Address: str,
    IPv6Interface: str,
    IPv6Network: str,
    # pydantic compatibility
    deque: list,
    Decimal: decimal_encoder,
    StrictBool: int,
    Pattern: _enc_pattern,
    # support subclasses of stdlib types, If no previous type matched, these will be
    # the last type in the mro, so we use this to (attempt to) convert a subclass into
    # its base class. # see https://github.com/jcrist/msgspec/issues/248
    # and https://github.com/litestar-org/litestar/issues/1003
    str: str,
    int: int,
    float: float,
    set: set,
    frozenset: frozenset,
}


def default_serializer(value: Any, type_encoders: Mapping[Any, Callable[[Any], Any]] | None = None) -> Any:
    """Transform values non-natively supported by ``msgspec``

    Args:
        value: A value to serialized
        type_encoders: Mapping of types to callables to transforming types
    Returns:
        A serialized value
    Raises:
        TypeError: if value is not supported
    """
    if type_encoders is None:
        type_encoders = DEFAULT_TYPE_ENCODERS
    for base in value.__class__.__mro__[:-1]:
        try:
            encoder = type_encoders[base]
        except KeyError:
            continue
        return encoder(value)
    raise TypeError(f"Unsupported type: {type(value)!r}")


def dec_hook(type_: Any, value: Any) -> Any:  # pragma: no cover
    """Transform values non-natively supported by ``msgspec``

    Args:
        type_: Encountered type
        value: Value to coerce

    Returns:
        A ``msgspec``-supported type
    """
    if issubclass(type_, BaseModel):
        return type_.parse_obj(value)
    if issubclass(type_, (Path, PurePath)):
        return type_(value)
    raise TypeError(f"Unsupported type: {type(value)!r}")


_msgspec_json_encoder = msgspec.json.Encoder(enc_hook=default_serializer)
_msgspec_json_decoder = msgspec.json.Decoder(dec_hook=dec_hook)
_msgspec_msgpack_encoder = msgspec.msgpack.Encoder(enc_hook=default_serializer)
_msgspec_msgpack_decoder = msgspec.msgpack.Decoder(dec_hook=dec_hook)


def encode_json(obj: Any, default: Callable[[Any], Any] | None = default_serializer) -> bytes:
    """Encode a value into JSON.

    Args:
        obj: Value to encode
        default: Optional callable to support non-natively supported types.

    Returns:
        JSON as bytes

    Raises:
        SerializationException: If error encoding ``obj``.
    """
    try:
        if default is None or default is default_serializer:
            return _msgspec_json_encoder.encode(obj)
        return msgspec.json.encode(obj, enc_hook=default)
    except (TypeError, msgspec.EncodeError) as msgspec_error:
        raise SerializationException(str(msgspec_error)) from msgspec_error


@overload
def decode_json(raw: str | bytes) -> Any:
    ...


@overload
def decode_json(raw: str | bytes, type_: type[T]) -> T:
    ...


def decode_json(raw: str | bytes, type_: Any = Empty) -> Any:
    """Decode a JSON string/bytes into an object.

    Args:
        raw: Value to decode
        type_: An optional type to decode the data into

    Returns:
        An object

    Raises:
        SerializationException: If error decoding ``raw``.
    """
    try:
        if type_ is Empty:
            return _msgspec_json_decoder.decode(raw)
        return msgspec.json.decode(raw, dec_hook=dec_hook, type=type_)
    except msgspec.DecodeError as msgspec_error:
        raise SerializationException(str(msgspec_error)) from msgspec_error


def encode_msgpack(obj: Any, enc_hook: Callable[[Any], Any] | None = default_serializer) -> bytes:
    """Encode a value into MessagePack.

    Args:
        obj: Value to encode
        enc_hook: Optional callable to support non-natively supported types

    Returns:
        MessagePack as bytes

    Raises:
        SerializationException: If error encoding ``obj``.
    """
    try:
        if enc_hook is None or enc_hook is default_serializer:
            return _msgspec_msgpack_encoder.encode(obj)
        return msgspec.msgpack.encode(obj, enc_hook=enc_hook)
    except (TypeError, msgspec.EncodeError) as msgspec_error:
        raise SerializationException(str(msgspec_error)) from msgspec_error


@overload
def decode_msgpack(raw: bytes) -> Any:
    ...


@overload
def decode_msgpack(raw: bytes, type_: type[T]) -> T:
    ...


def decode_msgpack(raw: bytes, type_: Any = Empty) -> Any:
    """Decode a MessagePack string/bytes into an object.

    Args:
        raw: Value to decode
        type_: An optional type to decode the data into

    Returns:
        An object

    Raises:
        SerializationException: If error decoding ``raw``.
    """
    try:
        if type_ is Empty:
            return _msgspec_msgpack_decoder.decode(raw)
        return msgspec.msgpack.decode(raw, dec_hook=dec_hook, type=type_)
    except msgspec.DecodeError as msgspec_error:
        raise SerializationException(str(msgspec_error)) from msgspec_error


def decode_media_type(raw: bytes, media_type: MediaType | str, type_: Any) -> Any:
    """Decode a raw value into an object.

    Args:
        raw: Value to decode
        media_type: Media type of the value
        type_: An optional type to decode the data into

    Returns:
        An object

    Raises:
        SerializationException: If error decoding ``raw`` or ``media_type`` unsupported.
    """
    if media_type == MediaType.JSON:
        return decode_json(raw, type_=type_)

    if media_type == MediaType.MESSAGEPACK:
        return decode_msgpack(raw, type_=type_)

    raise SerializationException(f"Unsupported media type: '{media_type}'")


def get_serializer(type_encoders: TypeEncodersMap | None = None) -> Serializer:
    """Get the serializer for the given type encoders."""

    if type_encoders:
        return partial(default_serializer, type_encoders={**DEFAULT_TYPE_ENCODERS, **type_encoders})

    return default_serializer
