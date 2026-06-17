import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8983047831:AAEmmIF0Sp902mwk5VhdSO0X_-D5jKpbk1k"

CHANNEL = "@heytomach"

CHAT_LINK = "https://t.me/+pKGgiZTD-OI2Y2Ey"
CHANNEL_LINK = "https://t.me/heytomach"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="получить ссылку", callback_data="start")]
    ])

def subscribe_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="подписка есть", callback_data="check_sub")],
        [InlineKeyboardButton(text="тг-канал", url=CHANNEL_LINK)]
    ])

async def is_subscribed(user_id: int):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "привет🐛 это бот heytoma\n\n"
        "рада поделиться с тобой ссылкой на чат для мам!",
        reply_markup=start_keyboard()
    )

@dp.callback_query(lambda c: c.data == "start")
async def start_btn(callback: types.CallbackQuery):
    await callback.message.answer(
        "подпишись на канал",
        reply_markup=subscribe_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "check_sub")
async def check_sub(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if await is_subscribed(user_id):
        await callback.message.answer(
            f"лови ссылку 💛\n\n{CHAT_LINK}"
        )
    else:
        await callback.message.answer(
            "не вижу подписку :( подпишись и попробуй снова"
        )

    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())