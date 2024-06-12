from aiogram import types
from initial import bot, dp
from keyboards import create_keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from dataClient.db_mysql import DataClient

from config import FSMWorkProgram


class MeetMenu:
    btn_meet_main_menu = ["Смотреть анкеты",
                          "Настроить профиль",
                          "Настроить систему"]
    btn_profile_settings_meet = ["Имя",
                                 "Возраст",
                                 "Интересы",
                                 # "Любимые места",
                                 "Описание",
                                 "Пол",
                                 "Фотография"]
    btn_system_settings_meet = ["Кого ищешь",
                                "Возраст"]

    def __init__(self, data_client: DataClient) -> None:
        self.data_client = data_client

    async def meet_main_menu(self, msg: types.Message):
        await msg.answer("Выберите режим работы",
                         reply_markup=create_keyboards(self.btn_meet_main_menu, cancel_btn=True))
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
        result = self.data_client.check_meet_settings(tg_user_id=msg.from_user.id)
        if result:
            self.kb = InlineKeyboardMarkup(row_width=2)
            self.kb.add(InlineKeyboardButton(text="🚫", callback_data="-"),
                        InlineKeyboardButton(text="❤", callback_data="+"))
            await self.set_user_meet(msg=msg, state=state)
        else:
            await msg.answer("Сначала добавь в настройки следующую информацию: 'Пол' и 'Кого ищешь'.")

    async def negative_react(self, callback: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await callback.answer()
            self.data_client.set_user_reaction_meet(user_id=callback.from_user.id,
                                                    purpose_user_id=data["purpose_user_id"],
                                                    reaction="0")
        await self.set_user_meet(msg=callback, state=state)

    async def positive_react(self, callback: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await callback.answer()
            result = self.data_client.check_meet_match(user_tg_id=str(callback.from_user.id),
                                                       purpose_user_id=data["purpose_user_id"])
            print(result)
            self.data_client.set_user_reaction_meet(user_id=callback.from_user.id,
                                                    purpose_user_id=data["purpose_user_id"],
                                                    reaction="1")
            if not result:
                base_text = f"You have a match with: @"
                user_id = self.data_client.get_user_id(tg_id=str(callback.from_user.id))
                purpose_user_tg_id = self.data_client.get_user_tg_id(user_id=data["purpose_user_id"])
                user_tg_nick1 = self.data_client.get_user_tg_nick(user_id=data["purpose_user_id"])
                user_tg_nick2 = self.data_client.get_user_tg_nick(user_id=user_id)
                await callback.message.answer(base_text + user_tg_nick1)
                await bot.send_message(chat_id=purpose_user_tg_id, text=base_text+user_tg_nick2)
        await self.set_user_meet(msg=callback, state=state)

    async def profile_settings(self, msg: types.Message):
        await msg.answer("Выберите, что хотите изменить про себя",
                         reply_markup=create_keyboards(self.btn_profile_settings_meet, cancel_btn=True))
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
            await msg.answer("Хотите еще что-нибудь изменить?",
                             reply_markup=create_keyboards(self.btn_profile_settings_meet, cancel_btn=True))
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
            await msg.answer("Хотите еще что-нибудь изменить?",
                             reply_markup=create_keyboards(self.btn_profile_settings_meet, cancel_btn=True))
        else:
            await msg.answer("Произошла ошибка. Повторите попытку.")

    async def change_interests1(self, msg: types.Message):
        btn = self.data_client.get_category_interest_list()[1]
        await msg.answer("Выбери категорию интересов.",
                         reply_markup=create_keyboards(btn_list=btn, cancel_btn=True))
        await FSMWorkProgram.meet_change_interests1.set()

    async def change_interest2(self, msg: types.Message, state: FSMContext):
        category_id = self.data_client.get_category_interest_id(msg.text)
        async with state.proxy() as data:
            data["category_id"] = category_id
            data["category_title"] = msg.text
            user_id = self.data_client.get_user_id(str(msg.from_user.id))
            btn = self.data_client.get_interest_list(category_id=category_id, user_id=user_id)[1]
            btn = list(map(lambda x: x["title"] + x["res"], btn))
            await msg.answer("Нажмите на кнопку, чтобы изменить настройку.",
                             reply_markup=create_keyboards(btn_list=btn, cancel_btn=True))
            await FSMWorkProgram.meet_change_interests2.set()

    async def change_interest3(self, msg: types.Message, state: FSMContext):
        msg_text = msg.text.split(":")
        interest = msg_text[0]
        action = True if msg_text[1] == "off" else False
        user_id = self.data_client.get_user_id(str(msg.from_user.id))
        interest_id = self.data_client.get_interest_id(title=interest)

        result = self.data_client.upd_user_interest_info(user_id=user_id, interest_id=interest_id, action=action)
        async with state.proxy() as data:

            btn = self.data_client.get_interest_list(category_id=data["category_id"], user_id=user_id)[1]
            btn = list(map(lambda x: x["title"] + x["res"], btn))
            await msg.answer("Изменения сохранены.",
                             reply_markup=create_keyboards(btn_list=btn, cancel_btn=True))

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
            await msg.answer("Хотите еще что-нибудь изменить?",
                             reply_markup=create_keyboards(self.btn_profile_settings_meet, cancel_btn=True))
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
            await msg.answer("Хотите еще что-нибудь изменить?",
                             reply_markup=create_keyboards(self.btn_profile_settings_meet, cancel_btn=True))
        else:
            await msg.answer("Произошла ошибка. Повторите попытку.")

    async def change_sex_own(self, msg: types.Message):
        await msg.answer("Выбери свой пол.",
                         reply_markup=create_keyboards(["Boy", "Girl"], cancel_btn=True))
        await FSMWorkProgram.meet_change_sex_own.set()

    async def save_sex_own(self, msg: types.Message):
        new_value = "1" if msg.text == "Boy" else "0"
        result = self.data_client.upd_user_info(user_id=str(msg.from_user.id),
                                                element="sex",
                                                new_value=new_value)
        if result:
            await msg.answer("Изменения сохранены.")
            await FSMWorkProgram.meet_profile_settings.set()
            await msg.answer("Хотите еще что-нибудь изменить?",
                             reply_markup=create_keyboards(self.btn_profile_settings_meet, cancel_btn=True))
        else:
            await msg.answer("Произошла ошибка. Повторите попытку.")

    async def change_photo(self, msg: types.Message):
        await msg.answer("Отправь новое фото.",
                         reply_markup=create_keyboards(list()))
        await FSMWorkProgram.meet_change_photo.set()

    async def save_photo(self, msg: types.Message):
        photo_id = msg.photo[-1]["file_id"]
        result = self.data_client.upd_user_info(user_id=str(msg.from_user.id),
                                                element="photo_id",
                                                new_value=photo_id)
        if result:
            await msg.answer("Изменения сохранены.")
            await FSMWorkProgram.meet_profile_settings.set()
            await msg.answer("Хотите еще что-нибудь изменить?",
                             reply_markup=create_keyboards(self.btn_profile_settings_meet, cancel_btn=True))
        else:
            await msg.answer("Произошла ошибка. Повторите попытку.")

    async def system_settings(self, msg: types.Message):
        await msg.answer("Выбери, что хотите изменить про себя",
                         reply_markup=create_keyboards(self.btn_system_settings_meet, cancel_btn=True))
        await FSMWorkProgram.meet_system_settings.set()

    async def who_looking(self, msg: types.Message):
        await msg.answer("Выбери пол, кого ищешь.",
                         reply_markup=create_keyboards(["Boy", "Girl"], cancel_btn=True))
        await FSMWorkProgram.meet_change_sex_find.set()

    async def save_who_looking(self, msg: types.Message):
        new_value = '1' if msg.text == "Boy" else '0'
        result = self.data_client.upd_user_info(user_id=str(msg.from_user.id),
                                                element="sex_find",
                                                new_value=new_value)
        if result:
            await msg.answer("Изменения сохранены.")
            await FSMWorkProgram.meet_profile_settings.set()
            await msg.answer("Хотите еще что-нибудь изменить?",
                             reply_markup=create_keyboards(self.btn_system_settings_meet, cancel_btn=True))
        else:
            await msg.answer("Произошла ошибка. Повторите попытку.")

    async def age_looking1(self, msg: types.Message):
        await msg.answer("Введи минимальное значение возраста, кого ищешь.",
                         reply_markup=create_keyboards(list(), cancel_btn=True))
        await FSMWorkProgram.meet_change_age_find1.set()

    async def age_looking2(self, msg: types.Message, state: FSMContext):
        try:
            async with state.proxy() as data:
                new_value = int(msg.text)
                if 18 <= new_value <= 55:
                    data["start_age"] = new_value
                    await msg.answer("Введи максимальное значение возраста, кого ищешь.",
                                     reply_markup=create_keyboards(list(), cancel_btn=True))
                    await FSMWorkProgram.meet_change_age_find2.set()
                else:
                    await msg.answer("Недопустимое значение, повторите попытку.")
        except Exception:
            await msg.answer("Произошла ошибка. Повторите попытку.")

    async def save_age_looking(self, msg: types.Message, state: FSMContext):
        try:
            new_value = int(msg.text)
            async with state.proxy() as data:
                if 18 <= new_value <= 55 and new_value > data["start_age"]:

                    new_value = f"{data['start_age']}:{msg.text}"
                    result = self.data_client.upd_user_info(user_id=str(msg.from_user.id),
                                                            element="age_find",
                                                            new_value=new_value)
                    if result:
                        await msg.answer("Изменения сохранены.")
                        await FSMWorkProgram.meet_profile_settings.set()
                        await msg.answer("Хотите еще что-нибудь изменить?",
                                         reply_markup=create_keyboards(self.btn_system_settings_meet, cancel_btn=True))
                    else:
                        await msg.answer("Произошла ошибка. Повторите попытку.1")
        except Exception as ex:
            print(ex)
            await msg.answer("Произошла ошибка. Повторите попытку.2")

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
                                    state=FSMWorkProgram.meet_change_age)
        dp.register_message_handler(self.change_interests1,
                                    Text(equals="Интересы", ignore_case=True),
                                    state=FSMWorkProgram.meet_profile_settings)
        dp.register_message_handler(self.change_interest2,
                                    state=FSMWorkProgram.meet_change_interests1)
        dp.register_message_handler(self.change_interest3,
                                    state=FSMWorkProgram.meet_change_interests2)
        dp.register_message_handler(self.change_prefer_place,
                                    Text(equals="Любимые места", ignore_case=True),
                                    state=FSMWorkProgram.meet_profile_settings)
        dp.register_message_handler(self.save_prefer_place,
                                    state=FSMWorkProgram.meet_change_prefer_place)
        dp.register_message_handler(self.change_description,
                                    Text(equals="Описание", ignore_case=True),
                                    state=FSMWorkProgram.meet_profile_settings)
        dp.register_message_handler(self.save_description,
                                    state=FSMWorkProgram.meet_change_description)
        dp.register_message_handler(self.change_sex_own,
                                    Text(equals="Пол", ignore_case=True),
                                    state=FSMWorkProgram.meet_profile_settings)
        dp.register_message_handler(self.save_sex_own,
                                    state=FSMWorkProgram.meet_change_sex_own)
        dp.register_message_handler(self.change_photo,
                                    Text(equals="Фотография", ignore_case=True),
                                    state=FSMWorkProgram.meet_profile_settings)
        dp.register_message_handler(self.save_photo,
                                    content_types=["photo"],
                                    state=FSMWorkProgram.meet_change_photo)

        dp.register_message_handler(self.system_settings,
                                    Text(equals="Настроить систему", ignore_case=True),
                                    state=FSMWorkProgram.meet_main_menu)
        dp.register_message_handler(self.who_looking,
                                    Text(equals="Кого ищешь", ignore_case=True),
                                    state=FSMWorkProgram.meet_system_settings)
        dp.register_message_handler(self.save_who_looking,
                                    state=FSMWorkProgram.meet_change_sex_find)
        dp.register_message_handler(self.age_looking1,
                                    Text(equals="Возраст", ignore_case=True),
                                    state=FSMWorkProgram.meet_system_settings)
        dp.register_message_handler(self.age_looking2,
                                    state=FSMWorkProgram.meet_change_age_find1)
        dp.register_message_handler(self.save_age_looking,
                                   state=FSMWorkProgram.meet_change_age_find2)

        dp.register_callback_query_handler(self.negative_react,
                                           Text(equals="-"),
                                           state="*")

        dp.register_callback_query_handler(self.positive_react,
                                           Text(equals="+"),
                                           state="*")
