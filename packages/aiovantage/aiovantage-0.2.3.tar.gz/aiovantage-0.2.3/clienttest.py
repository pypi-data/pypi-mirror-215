"""Async TCP connection class."""

import asyncio
from ssl import CERT_NONE, SSLContext, create_default_context
from types import TracebackType
from typing import AsyncIterator, ClassVar, Optional, Type, Union
from xml.etree import ElementTree

from typing_extensions import Self
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.parsers.handlers import XmlEventHandler
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from aiovantage.config_client.methods import Call, Method, Return


class ClientError(Exception):
    """Base exception for config client."""


class ClientConnectionError(ClientError):
    """Exception for config client connection errors."""


class ClientTimeoutError(asyncio.TimeoutError, ClientConnectionError):
    """Exception for command client connection errors caused by timeouts."""


class Connection:
    """Async TCP connection class."""

    default_port: ClassVar[int]
    default_ssl_port: ClassVar[int]
    default_conn_timeout: ClassVar[float]
    default_read_timeout: ClassVar[float]
    buffer_limit: ClassVar[int] = 2**16

    def __init__(
        self,
        host: str,
        port: Optional[int] = None,
        ssl: Union[SSLContext, bool] = True,
        conn_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None,
    ) -> None:
        """Initialize the connection."""
        self._host = host
        self._conn_timeout = conn_timeout or self.default_conn_timeout
        self._read_timeout = read_timeout or self.default_read_timeout
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None

        # Set up the SSL context
        self._ssl: Optional[SSLContext]
        if ssl is True:
            # We don't have a local issuer certificate to check against, and we'll be
            # connecting to an IP address so we can't check the hostname
            self._ssl = create_default_context()
            self._ssl.check_hostname = False
            self._ssl.verify_mode = CERT_NONE
        elif isinstance(ssl, SSLContext):
            self._ssl = ssl
        else:
            self._ssl = None

        # Set up the port
        self._port: int
        if port is None:
            self._port = self.default_ssl_port if ssl else self.default_port
        else:
            self._port = port

    async def __aenter__(self) -> Self:
        """Return context manager."""
        await self.open()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit context manager."""
        self.close()

        if exc_val:
            raise exc_val

    async def open(self) -> None:
        """Open a connection."""

        # If we're already connected, do nothing
        if self._writer is not None and not self._writer.is_closing():
            return

        # Create the connection
        try:
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(
                    self._host,
                    self._port,
                    ssl=self._ssl,
                    limit=self.buffer_limit,
                ),
                timeout=self._conn_timeout,
            )
        except asyncio.TimeoutError as exc:
            raise ClientTimeoutError(
                f"Timout connecting to {self._host}:{self._port}"
            ) from exc
        except OSError as exc:
            raise ClientConnectionError(
                f"Failed to connect to {self._host}:{self._port}"
            ) from exc

    def close(self) -> None:
        """Close the connection."""

        if self._writer is not None and not self._writer.is_closing():
            self._writer.close()
            self._writer = None

    @property
    def host(self) -> str:
        """Return the host."""
        return self._host

    @property
    def closed(self) -> bool:
        """Return whether the connection is closed."""
        return self._writer is None or self._writer.is_closing()

    async def write(self, request: str) -> None:
        """Send a plaintext message."""

        # Make sure we're connected
        if self._writer is None or self._writer.is_closing():
            raise ClientConnectionError("Client not connected, did you call open()?")

        try:
            # Send the request
            self._writer.write(request.encode())
            await self._writer.drain()

        except OSError as err:
            raise ClientConnectionError from err

    async def read(self, end_token: str = "\n") -> str:
        """Read a plaintext response, with a timeout."""

        # Make sure we're connected
        if self._reader is None or self._writer is None or self._writer.is_closing():
            raise ClientConnectionError("Client not connected, did you call open()?")

        try:
            # Read the response
            data = await self._reader.readuntil(end_token.encode())

        except (OSError, asyncio.IncompleteReadError) as err:
            raise ClientConnectionError from err

        return data.decode()

    async def read_with_timeout(self, end_token: str = "\n") -> str:
        """Read a plaintext response, with a timeout."""

        try:
            data = await asyncio.wait_for(self.read(end_token), self._read_timeout)
        except asyncio.TimeoutError as err:
            raise ClientTimeoutError from err

        return data


class ConfigConnection(Connection):
    """Connection to a Vantage ACI server."""

    default_port = 2001
    default_ssl_port = 2010
    default_conn_timeout = 5.0
    default_read_timeout = 30.0
    read_buffer = 2**20

    async def request(self, interface: str, payload: str) -> str:
        """Send a request and return the response."""

        # Send the request
        await self.write(f"<{interface}>{payload}</{interface}>")

        # Read the response
        return await self.read(f"</{interface}>")


class CommandConnection(Connection):
    """Connection to a Vantage ACI server."""

    default_port = 3001
    default_ssl_port = 3010
    default_conn_timeout = 5.0
    default_read_timeout = 5.0

    async def request(self, request: str) -> str:
        """Send a request and immediately return the response."""

        # Send the request
        await self.write(f"{request}\n")

        # Read the response
        return (await self.read()).rstrip()

    async def message_stream(self) -> AsyncIterator[str]:
        """Return an async iterator over the incoming messages."""

        while True:
            yield (await self.read()).rstrip()


class ConfigClient:
    def __init__(
        self,
        host: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        *,
        ssl: Union[SSLContext, bool] = True,
        port: Optional[int] = None,
    ) -> None:
        self._connection = ConfigConnection(host, port=port, ssl=ssl)

        self._parser = XmlParser(
            config=ParserConfig(fail_on_unknown_properties=False),
            handler=XmlEventHandler,
        )

        self._serializer = XmlSerializer(
            config=SerializerConfig(xml_declaration=False),
        )

    async def request(
        self,
        method_cls: Type[Method[Call, Return]],
        params: Optional[Call],
    ) -> Return:
        """Send a request and return the response."""

        if self._connection.closed:
            await self._connection.open()

            # TODO: Login

        raw_response = await self._connection.request(
            method_cls.interface, self._marshall_request(method_cls, params)
        )

        return self._unmarshall_response(method_cls, raw_response)

    def _marshall_request(
        self,
        method_cls: Type[Method[Call, Return]],
        params: Optional[Call],
    ) -> str:
        """Marshall a request to XML."""

        # Build the method object
        method = method_cls()
        method.call = params

        # Render the method object to XML with xsdata
        return self._serializer.render(method)

    def _unmarshall_response(
        self,
        method_cls: Type[Method[Call, Return]],
        response: str,
    ) -> Return:
        """Unmarshall a response from XML."""

        # Parse the XML doc
        tree = ElementTree.fromstring(response)

        # Extract the method element from XML doc
        method_el = tree.find(f"{method_cls.__name__}")
        if method_el is None:
            raise ValueError(
                f"Response from {method_cls.interface} did not contain a "
                f"<{method_cls.__name__}> element"
            )

        # Parse the method element with xsdata
        method = self._parser.parse(method_el, method_cls)
        if method.return_value is None or method.return_value == "":
            raise TypeError(
                f"Response from {method_cls.interface}.{method_cls.__name__}"
                f" did not contain a return value"
            )

        return method.return_value
