import config
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from docx import Document
from pypdf import PdfReader
import asyncio
from loguru import logger
import os


class Resume(StatesGroup):
    resume_sent = State()


logging_level = 'INFO'
logger.add(
    "sys.stdout",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {file}:{line} - {message}",
    colorize=True,
    level=logging_level
)


bot = Bot(token=config.TG_token , default=DefaultBotProperties(parse_mode = ParseMode.HTML)) # type: ignore
dp = Dispatcher(storage=MemoryStorage())


@dp.message(StateFilter(None), Command('resume'))
async def cmd_resume(message: Message, bot: Bot, state: FSMContext):
    await message.answer(
        text='''
        Пожалуйста, загрузите резюме в PDF или .docx формате:
        ''',
        parse_mode=None
    )
    await state.set_state(Resume.resume_sent)


@dp.message(Resume.resume_sent)
async def resume_sent(message: Message, state: FSMContext):
    if message.document:
        try:
            doc = message.document
            file_name=doc.file_name
            file_id = doc.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            this_script_path = os.path.abspath(__file__).replace('\\', '/')
            tmp_path = this_script_path[:this_script_path.find('src')]
            await bot.download_file(file_path=file_path, destination=tmp_path + 'tmp/' + file_name)
            await asyncio.sleep(0.1)
            if message.document.file_name.endswith('.docx'):
                local_doc = Document(f'tmp/{file_name}')
                iterated_doc = ''
                for paragraph in local_doc.paragraphs:
                    iterated_doc += paragraph.text + '\n'
                await message.reply(text=iterated_doc)
            elif message.document.file_name.endswith('.pdf'):
                reader = PdfReader(f"tmp/{file_name}")
                page = reader.pages[0]
                text = page.extract_text()
                await message.reply(text=text)
        except Exception as e:
            logger.error(f'Error druing processing a file: {e}')
        finally:
            state.clear()
    

@dp.message(Command('search'))
async def cmd_search(message: Message):
    inline_keyboard = InlineKeyboardBuilder()
    button1 = InlineKeyboardButton(text='Откликнуться', callback_data='text 1')
    button2 = InlineKeyboardButton(text='Пропустить', callback_data='text 2') 
    button3 = InlineKeyboardButton(text='Скрыть компанию', callback_data='text 3')
    button4 = InlineKeyboardButton(text='Ещё похожие', callback_data='text 4') 
    button5 = InlineKeyboardButton(text='Подробнее', callback_data='text 5')
    inline_keyboard.add(button1, button2, button3
    )
    inline_keyboard.row(button4, button5)
    for i in range(3):
        await message.answer(text=f'Вакансия {i + 1}',
                   reply_markup=inline_keyboard.as_markup()
                   )


'''--= Main ---'''
async def main():
    if not os.path.exists("/tmp"):  
        os.makedirs("/tmp")
    await dp.start_polling(bot)
