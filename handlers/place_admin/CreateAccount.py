from aiogram import types
from initial import bot, dp
from keyboards import create_keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from dataClient.db_mysql import DataClient

from config import FSMWorkProgram


class CreateAccount:
    def __init__(self, data_client: DataClient) -> None:
        self.data_client = data_client

    async def start_reg_pa(self, msg: types.Message):
        if self.data_client.pa_is_exist(str(msg.from_user.id)):
            await msg.answer("Вы уже зарегистрированы, авторизируйтесь.",
                             reply_markup=create_keyboards(["Авторизироваться"]))
        else:
            btn = self.data_client.get_place_category_list()[1]
            await msg.answer("Выберите категорию заведения",
                             reply_markup=create_keyboards(btn))
            await FSMWorkProgram.start_reg_pa.set()

    async def choice_place_category_reg_pa(self, msg: types.Message, state: FSMContext):
        category_id = self.data_client.get_place_category_id(msg.text)
        async with state.proxy() as data:
            data["category"] = msg.text
            data["category_id"] = category_id
            btn = self.data_client.get_place_list(category_id=category_id)[1]
            await msg.answer("Выберите заведение.",
                             reply_markup=create_keyboards(btn))
            await FSMWorkProgram.choice_place_category_reg_pa.set()

    async def choice_place_reg_pa(self, msg: types.Message, state: FSMContext):
        place_id = self.data_client.get_place_id(msg.text)
        async with state.proxy() as data:
            data["place"] = msg.text
            data["place_id"] = place_id
            await msg.answer("Введите: свое имя/пароль/логин",
                             reply_markup=create_keyboards(list()))
            await FSMWorkProgram.choice_place_reg_pa.set()

    async def check_reg_pa(self, msg: types.Message, state: FSMContext):
        info = msg.text.split("/")
        name, password, login = info[0], info[1], info[2]
        async with state.proxy() as data:
            data["name"] = name
            data["password"] = password
            data["login"] = login
            message = f"Зарегистрироваться?\n\nЗаведение: {data['place']}\nИмя: {name}\n" \
                  f"Пароль: {password}\nЛогин: {login}."
            await msg.answer(message,
                             reply_markup=create_keyboards(list(), yes_no_btn=True))
        await FSMWorkProgram.check_reg_pa.set()

    async def save_reg_pa(self, msg: types.Message, state: FSMContext):
        if msg.text == "Да":
            async with state.proxy() as data:
                result = self.data_client.set_place_admin(place_id=data["place_id"],
                                                          user_name=data["name"],
                                                          user_pass=data["password"],
                                                          login=data["login"],
                                                          user_id=str(msg.from_user.id)
                                                          )

            await msg.answer("Вы зарегистрировались.",
                             reply_markup=create_keyboards(["В главное меню"]))
            await state.reset_data()
            await FSMWorkProgram.save_reg_pa.set()
        else:
            await msg.answer("Произошла ошибка.",
                             reply_markup=create_keyboards(list(), cancel_btn=True))
        #     await state.reset_data()
        #     await FSMWorkProgram.set_dish_info.set()
        # await FSMWorkProgram.save_dish_info.set()

    def run_handler(self) -> None:
        dp.register_message_handler(self.start_reg_pa,
                                    Text(equals="Зарегистрироваться", ignore_case=True),
                                    state=FSMWorkProgram.entrance_pa)
        dp.register_message_handler(self.choice_place_category_reg_pa,
                                    state=FSMWorkProgram.start_reg_pa)
        dp.register_message_handler(self.choice_place_reg_pa,
                                    state=FSMWorkProgram.choice_place_category_reg_pa)
        dp.register_message_handler(self.check_reg_pa,
                                    state=FSMWorkProgram.choice_place_reg_pa)
        dp.register_message_handler(self.save_reg_pa,
                                    state=FSMWorkProgram.check_reg_pa)


