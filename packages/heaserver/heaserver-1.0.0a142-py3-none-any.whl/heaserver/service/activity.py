from types import TracebackType
from typing import Type
from heaobject.activity import DesktopObjectAction, Status
from heaobject.user import NONE_USER
from heaobject.root import ShareImpl, Permission
from heaserver.service.oidcclaimhdrs import SUB
from aiohttp.web import Request, Application
from mypy_boto3_s3 import S3Client
from .messagebroker import publish_desktop_object
from .appproperty import HEA_DB
from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from collections.abc import Iterable, Callable, Coroutine
from contextlib import AbstractAsyncContextManager


T = TypeVar('T')

def default_shares(request: Request) -> tuple[ShareImpl]:
    """
    Default shares are NONE_USER and VIEWER permission.
    """
    share = ShareImpl()
    share.user = request.headers.get(SUB, NONE_USER)
    share.permissions = [Permission.VIEWER]
    return (share,)


class DesktopObjectActionLifecycle(AbstractAsyncContextManager[T], Generic[T], ABC):
    def __init__(self, request: Request,
                 code: str,
                 description: str,
                 volume_id: str,
                 owner: str = NONE_USER,
                 shares: Iterable[str] | None = None,
                 activity_cb: Callable[[Application, DesktopObjectAction], Coroutine[None, None, None]] | None = None) -> None:
        if request is None:
            raise ValueError('Request cannot be None')
        if code is None:
            raise ValueError('code cannot be None')
        if description is None:
            raise ValueError('description cannot be None')
        if volume_id is None:
            raise ValueError('volume_id cannot be None')
        if not isinstance(request, Request):
            raise TypeError(f'request must be a Request but was a {type(request)}')
        if owner is None:
            raise ValueError('owner cannot be None')
        self.__request = request
        self.__code = str(code)
        self.__description = str(description)
        self.__volume_id = str(volume_id)
        self.__activity: DesktopObjectAction | None = None
        self.__owner = str(owner) if owner is not None else NONE_USER
        self.__shares = list(shares) if shares is not None else list(default_shares(request))
        self.__activity_cb: Callable[[Application, DesktopObjectAction], Coroutine[None, None, None]] | None = activity_cb


    async def __aenter__(self) -> tuple[T, DesktopObjectAction]:
        if self.__activity_cb:
            self.__activity = DesktopObjectAction()
            self.__activity.generate_application_id()
            self.__activity.code = self.__code
            self.__activity.owner = self.__owner
            self.__activity.shares = self.__shares
            self.__activity.user_id = self.__activity.owner
            self.__activity.description = self.__description
            await self.__activity_cb(self.__request.app, self.__activity)

            self.__activity.status = Status.IN_PROGRESS
            await self.__activity_cb(self.__request.app, self.__activity)

        return await self.connection, self.__activity

    async def __aexit__(self, exc_type: Type[BaseException] | None,
                        exc_value: BaseException | None,
                        traceback: TracebackType | None) -> None:
        if self.__activity_cb:
            if exc_type is None:
                self.__activity.status = Status.SUCCEEDED
            else:
                self.__activity.status = Status.FAILED
            await publish_desktop_object(self.__request.app, self.__activity)
        return True  # Suppress the exception.

    @property
    @abstractmethod
    async def connection(self) -> T:
        """Returns the database connection."""
        pass

    @property
    def request(self) -> Request:
        return self.__request

    @property
    def volume_id(self) -> str:
        return self.__volume_id


class S3ClientDesktopObjectActionLifecycle(DesktopObjectActionLifecycle[S3Client]): # Go into db package?
    def __init__(self, request: Request,
                 code: str,
                 description: str,
                 volume_id: str,
                 connection: S3Client | None = None,
                 activity_cb: Callable[[Application, DesktopObjectAction], Coroutine[None, None, None]] | None = None) -> None:
        super().__init__(request, code, description, volume_id, activity_cb=activity_cb)
        if connection is not None and not isinstance(connection, S3Client):
            raise ValueError(f'Connection {connection} must be an S3Client')
        self.__connection = connection

    @property
    async def connection(self) -> S3Client:
        if self.__connection is None:
            self.__connection = await self.request.app[HEA_DB].get_client(self.request, 's3', self.volume_id)
        return self.__connection

