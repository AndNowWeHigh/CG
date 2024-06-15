import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode, ChatAction
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton

from aiogram.filters.command import Command

BOT_TOKEN = "6545180866:AAFhWbANjh72C1MJLt0Aujq-jHriTdiGWn4"

dp = Dispatcher()
router_output_doc = Router()

# --------------------------------
folder_document_path_in_method1 = "C:\\Users\ACER\Desktop\НН ФТІ\Com. graf\Project\media_users\document_in\method1"
folder_document_path_in_method2 = "C:\\Users\ACER\Desktop\НН ФТІ\Com. graf\Project\media_users\document_in\method2"

folder_document_path_out_method1 = "C:\\Users\ACER\Desktop\НН ФТІ\Com. graf\Project\media_users\document_out\method1"
folder_document_path_out_method2 = "C:\\Users\ACER\Desktop\НН ФТІ\Com. graf\Project\media_users\document_out\method2"
# --------------------------------
button_1m = KeyboardButton(text='Метод 1')
button_2m = KeyboardButton(text='Метод 2')

button_row_1 = [button_1m, button_2m]
markup = ReplyKeyboardMarkup(keyboard=[button_row_1])


# --------------------------------
@dp.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(f"Привіт\\. *{message.from_user.full_name}*\n"
                         f"Надсилай свій zip\\-файл, який містить набір зображень, який ти хочеш обробити\n",
                         parse_mode=ParseMode.MARKDOWN_V2)

# --------------------------------
@dp.message(F.document)
async def download_document(message: Message):
    Type_document = message.document.mime_type.split('/')  # список можливих типів файлу
    await message.bot.download(message.document,
                               destination=f'{folder_document_path_in_method1}/{message.document.file_id}_{message.chat.id}.{Type_document[-1]}')
    await message.bot.download(message.document,
                               destination=f'{folder_document_path_in_method2}/{message.document.file_id}_{message.chat.id}.{Type_document[-1]}')

    await message.answer(f'Бот завантажив <i>{message.document.file_name}</i>\n'
                         f"Тепер обери метод, яким ти бажаєш щоб обробити твої файли",
                         parse_mode=ParseMode.HTML,
                         reply_markup=markup)





# --------------------------------
@router_output_doc.message(F.text == 'Метод 1')
async def output_document(message: Message):
    await message.bot.send_chat_action(chat_id=message.chat.id,
                                       action=ChatAction.UPLOAD_DOCUMENT)
    while True:
        await asyncio.sleep(5)  # Чекаємо 5 секунд перед перевіркою каталогу
        files = os.listdir(folder_document_path_out_method1)
        if files:
            document_path = os.path.join(folder_document_path_out_method1, files[-1])
            documents = FSInputFile(document_path, filename=f"Your_ZipFile_Method1.zip")
            await message.bot.send_document(chat_id=message.chat.id,
                                            document=documents)
            break

@router_output_doc.message(F.text == 'Метод 2')
async def output_document(message: Message):
    await message.bot.send_chat_action(chat_id=message.chat.id,
                                       action=ChatAction.UPLOAD_DOCUMENT)
    while True:
        await asyncio.sleep(5)  # Чекаємо 5 секунд перед перевіркою каталогу
        files = os.listdir(folder_document_path_out_method2)
        if files:
            document_path = os.path.join(folder_document_path_out_method2, files[-1])
            documents = FSInputFile(document_path, filename="Your_ZipFile_Method2.zip")
            await message.bot.send_document(chat_id=message.chat.id,
                                            document=documents)
            break


# --------------------------------

async def main():
    dp.include_router(router_output_doc)
    bot = Bot(token=BOT_TOKEN)
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



