import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

users_sending = [] # Users sending promts store here (Could be changed for security)
TOKEN = open("./resources/teletoken", "r").read() # Bot's token in file
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

# Router replaces Dispatcher
router = Router()
dp = Dispatcher()
dp.include_router(router=router)

def get_result_by_promt(promt: str):
    result = "placeholder"
    return result

# Sends start message
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Continue", callback_data=f"to_main") # Go to main message
    await message.answer(text=f"This is AI Prompt Analyzer project. Click the button to continue.", reply_markup=builder.as_markup())

# Bot menu with Analyzer and Credits buttons
@router.callback_query(F.data == "to_main")
async def menu(callback_query: types.CallbackQuery) -> None:
    if callback_query.from_user.id in users_sending:
        users_sending.remove(callback_query.from_user.id) # Remove user from array
    title_img = FSInputFile('resources/title_icon.png')
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Analyze Prompt", callback_data=f"analyze")
    builder.button(text=f"Credits", callback_data=f"to_credits")
    text = f"The AI Prompt Analyzer helps people to make good prompts for other AIs. Press \'Analyze Prompt\' for advices."
    await bot.send_photo(chat_id=callback_query.from_user.id, photo=title_img, caption=text, reply_markup=builder.as_markup())

# Bot credits. !!!TODO!!!
@router.callback_query(F.data == "to_credits")
async def credits(callback_query: types.CallbackQuery) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Back to menu", callback_data=f"to_main")
    text = f"Project by:\nMTUCI BVT2206 Group\n\nGitHub repo: TODO"
    await bot.send_message(chat_id=callback_query.from_user.id, text=text, reply_markup=builder.as_markup())

# Analyzer. Waits for user's promt
@router.callback_query(F.data == "analyze")
async def analyzer_wait(callback_query: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Back to menu", callback_data=f"to_main")
    if callback_query.from_user.id in users_sending:
        text = f"You've already started analyzer. Press \"Back to menu\" to quit." # Exeption, when user's ID is in array
    else:
        users_sending.append(callback_query.from_user.id) # User ID added in users_sending array
        text = f"Write your prompts as message. Press \"Back to menu\" to quit."
    await bot.send_message(chat_id=callback_query.from_user.id, text=text, reply_markup=builder.as_markup())

# Sends promts to AI.
@router.message()
async def promt_to_analyze(message: Message):
    if message.from_user.id in users_sending: # Works if user is in array
        users_sending.remove(message.from_user.id)
        await message.answer(text=get_result_by_promt(promt=message.text)) # TODO

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
