from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject

from ..handlers.user import UserLanguageSetupHandlers


class UserLanguageMiddleware(BaseMiddleware):
    def __init__(self, handler: UserLanguageSetupHandlers) -> None:
        self.handler = handler
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Union[TelegramObject, types.Message],
        data: Dict[str, Any],
    ) -> Any:
        user = data.get('user')

        if not user:
            raise NotImplementedError(f'`{self.__class__.__name__}` requires user auth middleware')

        if not user.lang_code:
            return await self.handler._require(user.id)

        return await handler(event, data)
