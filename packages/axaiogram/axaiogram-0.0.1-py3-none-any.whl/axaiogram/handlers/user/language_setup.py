from typing import Callable, Dict, Union

from aiogram import Bot, Dispatcher, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..base import BaseHandlersGroup
from ..base import proxy_router as _router


class UserLanguageSetupHandlers(BaseHandlersGroup):
    def __init__(
        self,
        bot: Bot,
        dp: Dispatcher,
        uowf,
        languages: Union[Dict[str, str], None] = None,
        start_handler: Union[Callable, None] = None,
    ) -> None:
        super().__init__(bot, dp, uowf)
        self.uowf = uowf

        if not languages:
            languages = {
                "en": "English",
            }

        self.languages = languages
        self.start_handler = start_handler

    async def _require(self, chat_id: int):
        builder = InlineKeyboardBuilder()

        for code, name in self.languages.items():
            builder.button(text=name, callback_data=f"chlang:{code}")

        builder.adjust(1)

        msg = await self.bot.send_message(
            chat_id=chat_id,
            text="...",
            reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True),
        )

        await msg.delete()

        await self.bot.send_message(
            chat_id=chat_id,
            text="Выберите язык/Choose a language.",
            reply_markup=builder.as_markup(),
        )

    @_router.message(F.text == "/change_lang")
    async def show_list(self, message: types.Message):
        return await self._require(message.chat.id)

    @_router.message(F.text.strip().startswith("🌍"))
    async def handle_list(self, message: types.Message):
        assert message.from_user is not None
        return await self._require(message.from_user.id)

    @_router.callback_query(F.data.startswith("chlang:"))
    async def handle_choosen(self, cq: types.CallbackQuery):
        assert cq.data is not None
        assert cq.from_user is not None

        if cq.message:
            await cq.message.delete()

        _, lang_code = cq.data.split(":")

        async with self.uowf() as uow:
            user = await uow.repo.user.get(cq.from_user.id)
            user.lang_code = lang_code

            await uow.repo.user.update(user)

        if self.start_handler is not None:
            await self.start_handler(cq.from_user.id)
