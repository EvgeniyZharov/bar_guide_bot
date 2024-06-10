from aiogram import types
from initial import bot, dp
from keyboards import create_keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from dataClient.db_mysql import DataClient

from config import FSMWorkProgram

test_data = [
    {"name": "Test 1", "description": "Test 2", "interests": [1, 2, 3], "favorite place": ["bar1", "bar2"]},
    {"name": "Test 3", "description": "Test 4", "interests": [5, 2, 4], "favorite place": ["bar4", "bar44"]},
    {"name": "Test 5", "description": "Test 6", "interests": [4, 3, 7], "favorite place": ["bar3", "bar33"]},
    {"name": "Test 7", "description": "Test 8", "interests": [8, 9, 8], "favorite place": ["bar16", "bar66"]}
             ]


class MeetMenu:
    btn_meet_main_menu = ["Смотреть анкеты",
                          "Настроить профиль",
                          "Настроить систему"]
    btn_profile_settings_meet = ["Имя",
                                 "Возраст",
                                 "Интересы",
                                 "Любимые места",
                                 "Описание"]
    btn_system_settings_meet = ["Кого ищешь",
                                "Возраст",
                                "Цель"]

    def __init__(self, data_client: DataClient) -> None:
        self.data_client = data_client

    async def meet_main_menu(self, msg: types.Message):
        await msg.answer("Выберите режим работы",
                         reply_markup=create_keyboards(self.btn_meet_main_menu))
        await FSMWorkProgram.meet_main_menu.set()

    async def show_forms(self, msg: types.Message):
        # message = get_info
        pass

    async def set_user_meet(self, msg: [types.Message, types.CallbackQuery], state: FSMContext):

        async with state.proxy() as data:
            user_info = self.data_client.get_user_info_meet(user_id=msg.from_user.id)
            if user_info[0]:
                user_info = user_info[1][0]  # Get only result without bool flag
                text = f"Name: {user_info['name']}\nAge: {user_info['age']}\n" \
                       f"Desc: {user_info['description']}"
                msg_link = await bot.send_photo(chat_id=msg.from_user.id,
                                                photo=user_info["photo_id"],
                                                caption=text,
                                                reply_markup=self.kb)
                msg_link = msg_link["message_id"]
                data["msg_link"] = msg_link
                data["purpose_user_id"] = user_info['id']
            else:
                await bot.send_message(chat_id=msg.from_user.id,
                                       text="Анкеты закончились.")

    async def start_user_meet(self, msg: types.Message, state: FSMContext):
        self.kb = InlineKeyboardMarkup(row_width=2)
        self.kb.add(InlineKeyboardButton(text="🚫", callback_data="-"),
                    InlineKeyboardButton(text="❤", callback_data="+"))
        await self.set_user_meet(msg=msg, state=state)

    async def negative_react(self, callback: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            self.data_client.set_user_reaction_meet(user_id=callback.from_user.id,
                                                    purpose_user_id=data["purpose_user_id"],
                                                    reaction="0")
        await self.set_user_meet(msg=callback, state=state)

    async def positive_react(self, callback: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            self.data_client.set_user_reaction_meet(user_id=callback.from_user.id,
                                                    purpose_user_id=data["purpose_user_id"],
                                                    reaction="1")
        await self.set_user_meet(msg=callback, state=state)

    async def profile_settings(self, msg: types.Message):
        await msg.answer("Выберите, что хотите изменить про себя",
                         reply_markup=create_keyboards(self.btn_profile_settings_meet))
        await FSMWorkProgram.meet_profile_settings.set()

    async def change_name(self, msg: types.Message):
        await msg.answer("Введите новое имя.",
                         reply_markup=create_keyboards(list()))
        await FSMWorkProgram.meet_change_name.set()

    async def save_name(self, msg: types.Message):
        result = self.data_client.upd_user_info(user_id=str(msg.from_user.id),
                                                element="name",
                                                new_value=msg.text)
        if result:
            await msg.answer("Изменения сохранены.")
            await FSMWorkProgram.meet_profile_settings.set()
        else:
            await msg.answer("Произошла ошибка. Повторите попытку.")

    async def change_age(self, msg: types.Message):
        await msg.answer("Введите новый возраст.",
                         reply_markup=create_keyboards(list()))
        await FSMWorkProgram.meet_change_age.set()

    async def save_age(self, msg: types.Message):
        result = self.data_client.upd_user_info(user_id=str(msg.from_user.id),
                                                element="age",
                                                new_value=msg.text)
        if result:
            await msg.answer("Изменения сохранены.")
            await FSMWorkProgram.meet_profile_settings.set()
        else:
            await msg.answer("Произошла ошибка. Повторите попытку.")

    async def change_interests(self, msg: types.Message):
        await msg.answer("Введите новые интересы.",
                         reply_markup=create_keyboards(list()))
        await FSMWorkProgram.meet_change_interests.set()

    async def save_interests(self, msg: types.Message):
        result = self.data_client.upd_user_info(user_id=str(msg.from_user.id),
                                                element="interests",
                                                new_value=msg.text)
        if result:
            await msg.answer("Изменения сохранены.")
            await FSMWorkProgram.meet_profile_settings.set()
        else:
            await msg.answer("Произошла ошибка. Повторите попытку.")

    async def change_prefer_place(self, msg: types.Message):
        await msg.answer("Введите новые любимые места.",
                         reply_markup=create_keyboards(list()))
        await FSMWorkProgram.meet_change_prefer_place.set()

    async def save_prefer_place(self, msg: types.Message):
        result = self.data_client.upd_user_info(user_id=str(msg.from_user.id),
                                                element="prefer_place",
                                                new_value=msg.text)
        if result:
            await msg.answer("Изменения сохранены.")
            await FSMWorkProgram.meet_profile_settings.set()
        else:
            await msg.answer("Произошла ошибка. Повторите попытку.")

    async def change_description(self, msg: types.Message):
        await msg.answer("Введите новое описание.",
                         reply_markup=create_keyboards(list()))
        await FSMWorkProgram.meet_change_name.set()

    async def save_description(self, msg: types.Message):
        result = self.data_client.upd_user_info(user_id=str(msg.from_user.id),
                                                element="description",
                                                new_value=msg.text)
        if result:
            await msg.answer("Изменения сохранены.")
            await FSMWorkProgram.meet_profile_settings.set()
        else:
            await msg.answer("Произошла ошибка. Повторите попытку.")

    async def system_settings(self, msg: types.Message):
        await msg.answer("Выберите, что хотите изменить про себя",
                         reply_markup=create_keyboards(self.btn_system_settings_meet))
        await FSMWorkProgram.meet_system_settings.set()

    async def set_photo(self, msg: types.Message):
        await msg.answer(msg.photo[-1]["file_id"])

    def run_handler(self):
        # dp.register_message_handler(self.set_photo,
        #                             content_types=["photo"],
        #                             state="*")
        # dp.register_message_handler(self.start_user_meet,
        #                             commands=["test_1"],
        #                             state="*")
        dp.register_message_handler(self.meet_main_menu,
                                    Text(equals="Знакомства", ignore_case=True),
                                    state=[FSMWorkProgram.main_menu, FSMWorkProgram.admin_main_menu,
                                           FSMWorkProgram.main_menu_pa])

        dp.register_message_handler(self.start_user_meet,
                                    Text(equals="Смотреть анкеты", ignore_case=True),
                                    state=FSMWorkProgram.meet_main_menu)

        dp.register_message_handler(self.profile_settings,
                                    Text(equals="Настроить профиль", ignore_case=True),
                                    state=FSMWorkProgram.meet_main_menu)
        dp.register_message_handler(self.change_name,
                                    Text(equals="Имя", ignore_case=True),
                                    state=FSMWorkProgram.meet_profile_settings)
        dp.register_message_handler(self.save_name,
                                    state=FSMWorkProgram.meet_change_name)
        dp.register_message_handler(self.change_age,
                                    Text(equals="Возраст", ignore_case=True),
                                    state=FSMWorkProgram.meet_profile_settings)
        dp.register_message_handler(self.save_age,
                                    state=FSMWorkProgram.meet_change_name)
        dp.register_message_handler(self.change_interests,
                                    Text(equals="Интересы", ignore_case=True),
                                    state=FSMWorkProgram.meet_profile_settings)
        dp.register_message_handler(self.save_interests,
                                    state=FSMWorkProgram.meet_change_name)
        dp.register_message_handler(self.change_prefer_place,
                                    Text(equals="Любимые места", ignore_case=True),
                                    state=FSMWorkProgram.meet_profile_settings)
        dp.register_message_handler(self.save_prefer_place,
                                    state=FSMWorkProgram.meet_change_name)
        dp.register_message_handler(self.change_description,
                                    Text(equals="Описание", ignore_case=True),
                                    state=FSMWorkProgram.meet_profile_settings)
        dp.register_message_handler(self.save_description,
                                    state=FSMWorkProgram.meet_change_name)

        dp.register_message_handler(self.system_settings,
                                    Text(equals="Настроить систему", ignore_case=True),
                                    state=FSMWorkProgram.meet_main_menu)

        dp.register_callback_query_handler(self.negative_react,
                                           Text(equals="-"),
                                           state="*")

        dp.register_callback_query_handler(self.positive_react,
                                           Text(equals="+"),
                                           state="*")



