from aiogram import types
from initial import bot, dp
from keyboards import create_keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from dataClient.db_mysql import DataClient

from config import FSMWorkProgram


class MainMenu:
    btn_main_menu = ["Посмортеть заведение",
                     "Изменить описание",
                     "Создать анонс",
                     "Создать акцию",
                     "Посмотреть резервы",
                     "Посмотреть комментарии"]

    def __init__(self, data_client: DataClient) -> None:
        self.data_client = data_client

    async def open_main_menu(self, msg: types.Message):
        res = self.data_client.check_status_reg_pa(user_id=str(msg.from_user.id))
        if res == "1":
            await msg.answer("Выберите функцию.",
                             reply_markup=create_keyboards(self.btn_main_menu))
            await FSMWorkProgram.main_menu_pa.set()
        else:
            await msg.answer("Подождите, Ваш аккаунт пока не подтвердили.",
                             reply_markup=create_keyboards(list()))

    def run_handler(self) -> None:
        dp.register_message_handler(self.open_main_menu,
                                    Text(equals="В главное меню", ignore_case=True),
                                    state=[FSMWorkProgram.save_reg_pa, FSMWorkProgram.success_entrance_pa])



