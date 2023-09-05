import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_reader import config
from handlers import questions
from texts import texts

# Для записей с типом Secret* необходимо
# вызывать метод get_secret_value(),
# чтобы получить настоящее содержимое вместо '*******'
bot = Bot(token=config.bot_token.get_secret_value())
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Диспетчер
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Запуск процесса поллинга новых апдейтов
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_SELL_AUTO,
        callback_data="sell_auto")
    )
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_BUY_AUTO,
        callback_data="buy_auto")
    )

    await message.answer(text=texts.MESSAGE_MAIN_MENU, reply_markup=builder.as_markup())


dp.include_routers(questions.router)

if __name__ == "__main__":
    asyncio.run(main())
