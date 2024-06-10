from aiogram import types
from initial import bot, dp
from keyboards import create_keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from dataClient.db_mysql import DataClient

# from handlers.user.choice_place import
from config import FSMWorkProgram
# from handlers.user.choice_place import WatchPlacesProgram


class UserSettings:
    def __init__(self, data_client: DataClient) -> None:
        self.data_client = data_client

    def get_settings_btn(self, tg_id: str) -> list:
        btn = ["Знакомства"]
        return btn

    def get_meet_enable_btn(self, tg_id: str) -> list:
        if self.data_client.check_user_meet_enable(user_id=tg_id):
            return ["Участвую"]
        else:
            return ["Не участвую"]

    async def user_settings_menu(self, msg: types.Message):
        await msg.answer("Выберите, что хотите настроить.",
                         reply_markup=create_keyboards(self.get_settings_btn(tg_id=msg.from_user.id)))
        await FSMWorkProgram.user_settings_menu.set()

    async def user_set_meet_enable(self, msg: types.Message):
        await msg.answer("Вы можете переключить режим нажатием на кнопку.",
                         reply_markup=create_keyboards(
                             self.get_meet_enable_btn(msg.from_user.id), cancel_btn=True
                         ))
        await FSMWorkProgram.user_set_meet_enable.set()

    async def user_save_meet_enable(self, msg: types.Message):
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
        new_value = "0" if msg.text == "Участвую" else "1"
        res = self.data_client.upd_user_info(user_id=msg.from_user.id,
                                             element="meet_enabled",
                                             new_value=new_value)
        if res:
            await msg.answer("Настройка изменена.",
                             reply_markup=create_keyboards(
                                 self.get_meet_enable_btn(msg.from_user.id), cancel_btn=True
                             ))
        else:
            await msg.answer("Произошла ошибка.")



    def run_handler(self) -> None:
        dp.register_message_handler(self.user_settings_menu,
                                    Text(equals="Настройки", ignore_case=True),
                                    state=[FSMWorkProgram.main_menu,
                                           FSMWorkProgram.admin_main_menu,
                                           FSMWorkProgram.main_menu_pa])
        dp.register_message_handler(self.user_set_meet_enable,
                                    state=FSMWorkProgram.user_settings_menu)
        dp.register_message_handler(self.user_save_meet_enable,
                                    state=FSMWorkProgram.user_set_meet_enable)
