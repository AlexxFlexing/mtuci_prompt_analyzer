import asyncio
import logging
import sys
import json
from os import getenv, listdir

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from prompt_analyzer import prompt_analyzer

users_sending = [] # Users sending promts store here (Could be changed for security)
user_languages = {}
languages = {}
TOKEN = open("resources/teletoken", "r").read() # Bot's token in file
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

# Router replaces Dispatcher
router = Router()
dp = Dispatcher()
dp.include_router(router=router)

def get_json_string(key: str, user_id: int):
    try:
        return languages[user_languages[user_id]][key]
    except:
        return languages["en"][key]

#model_path = "C:/Users/aleks/Desktop/step2/models/Llama-2-7b-Chat-AWQ" gotta fix paths



def get_result_by_propmt(prompt: str):
    result = "placeholder"
    #result = prompt_analyzer(prompt=prompt, repo=model_path)
    return result

# Sends start message
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_languages[message.from_user.id] = message.from_user.language_code
    builder = InlineKeyboardBuilder()
    builder.button(text=get_json_string("continue", message.from_user.id), callback_data=f"to_main") # Go to main message
    await message.answer(text=get_json_string("welcome", message.from_user.id), reply_markup=builder.as_markup())

# Bot menu with Analyzer and Credits buttons
@router.callback_query(F.data == "to_main")
async def menu(callback_query: types.CallbackQuery) -> None:
    title_img = FSInputFile('resources/title_icon.png')
    builder = InlineKeyboardBuilder()
    builder.button(text=get_json_string("analyze", callback_query.from_user.id), callback_data=f"analyze")
    builder.button(text=get_json_string("languages", callback_query.from_user.id), callback_data=f"to_languages")
    builder.button(text=get_json_string("credits", callback_query.from_user.id), callback_data=f"to_credits")
    await bot.send_photo(chat_id=callback_query.from_user.id, photo=title_img, caption=get_json_string("menu", callback_query.from_user.id), reply_markup=builder.as_markup())
    await callback_query.message.delete()

# Bot credits. !!!TODO!!!
@router.callback_query(F.data == "to_credits")
async def credits(callback_query: types.CallbackQuery) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_json_string("back", callback_query.from_user.id), callback_data=f"quit")
    await bot.send_message(chat_id=callback_query.from_user.id, text=get_json_string("info", callback_query.from_user.id), reply_markup=builder.as_markup())
    await callback_query.answer()

@router.callback_query(F.data == "to_languages")
async def language_menu(callback_query: types.CallbackQuery) -> None:
    builder = InlineKeyboardBuilder()
    for key in list(languages.keys()):
        builder.button(text=languages[key]["lang"], callback_data=("lang." + key))
    builder.button(text=get_json_string("back", callback_query.from_user.id), callback_data=f"to_main")
    await bot.send_message(chat_id=callback_query.from_user.id, text=get_json_string("language_menu", callback_query.from_user.id), reply_markup=builder.as_markup())
    await callback_query.answer()

@router.callback_query(F.data.contains("lang."))
async def change_language(callback_query: types.CallbackQuery) -> None:
    user_languages[callback_query.from_user.id] = callback_query.data.removeprefix("lang.")
    print(callback_query.data.removesuffix("lang."))
    await callback_query.answer(get_json_string("language_changed", callback_query.from_user.id))

@router.callback_query(F.data == "quit")
async def remove_menu(callback_query: types.CallbackQuery) -> None:
    if callback_query.from_user.id in users_sending:
        users_sending.remove(callback_query.from_user.id) # Remove user from array
    await callback_query.message.delete()

# Analyzer. Waits for user's promt
@router.callback_query(F.data == "analyze")
async def analyzer_wait(callback_query: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_json_string("back", callback_query.from_user.id), callback_data=f"quit")
    if callback_query.from_user.id in users_sending:
        text = get_json_string("analyze_ready", callback_query.from_user.id) # Exeption, when user's ID is in array
    else:
        users_sending.append(callback_query.from_user.id) # User ID added in users_sending array
        text = get_json_string("write_prompt", callback_query.from_user.id)
    await bot.send_message(chat_id=callback_query.from_user.id, text=text, reply_markup=builder.as_markup())
    await callback_query.answer()

# Sends promts to AI.
@router.message()
async def prompt_to_analyze(message: Message):
    if message.from_user.id in users_sending: # Works if user is in array
        users_sending.remove(message.from_user.id)
        await message.answer(text=get_json_string("waiting", message.from_user.id)) # TODO
        await message.answer(text=get_result_by_propmt(prompt=message.text)) # TODO

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    for file in listdir("resources/languages"):
        if file.endswith(".json"):
            languages[file.removesuffix(".json")] = json.load(open("resources/languages/" + file))
            print(file.removesuffix(".json"))
            logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
