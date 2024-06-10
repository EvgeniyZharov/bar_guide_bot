from aiogram import types
from initial import bot, dp
from keyboards import create_keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from dataClient.db_mysql import DataClient

from config import FSMWorkProgram


class AuthorizationAdmin:
    def __init__(self, data_client: DataClient) -> None:
        self.data_client = data_client

    async def authorize_pa(self, msg: types.Message):
        await msg.answer("Введите: логин/пароль",
                         reply_markup=create_keyboards(list()))
        await FSMWorkProgram.authorize_pa.set()

    async def success_entrance_pa(self, msg: types.Message):
        info = msg.text.split("/")
        res = self.data_client.check_pass_log_pa(login=info[0], user_pass=info[1], user_id=str(msg.from_user.id))
        if res:
            await msg.answer("Вы успешно авторизировались.",
                             reply_markup=create_keyboards(["В главное меню"]))
            await FSMWorkProgram.success_entrance_pa.set()
        else:
            await msg.answer("Вы допустили ошибку, попробуйте еще раз.")


    def run_handler(self) -> None:
        dp.register_message_handler(self.authorize_pa,
                                    Text(equals="Авторизироваться", ignore_case=True),
                                    state=FSMWorkProgram.entrance_pa)
        dp.register_message_handler(self.success_entrance_pa,
                                    state=FSMWorkProgram.authorize_pa)


