from aiogram import types
from initial import bot, dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from dataClient.db_mysql import DataClient

from keyboards import create_keyboards
from config import FSMWorkProgram

from handlers.place_admin.AutorizationAdmin import AuthorizationAdmin
from handlers.place_admin.CreateAccount import CreateAccount
from handlers.place_admin.MainMenu import MainMenu


class PAClient:
    btn_pa_main_menu = ["Мое заведение",
                        "Смотреть заведения",
                        "Найти заведение",
                        "Заведения рядом",
                        "Мероприятия",
                        "О проекте",
                        ]
    btn_settings = ["Список резервов",
                    "Настройки меню",
                    "Настройки информации о заведении",
                    ]
    btn_admin_place = ["Зарегистрироваться",
                       "Авторизироваться"]

    def __init__(self, data_client: DataClient):
        self.data_client = data_client

        self.CreateAccount = CreateAccount(data_client=data_client)
        self.AuthorizationAdmin = AuthorizationAdmin(data_client=data_client)
        self.MainMenu = MainMenu(data_client=data_client)

    # async def set_new_place_admin(self, msg: types.Message):
    #     places = self.data_client.get_place_list()
    #     await msg.answer("Выберите заведение, в котором Вы работаете.",
    #                      reply_markup=create_keyboards(places))
    #     await FSMWorkProgram.start_create_pa.set()
    #
    # async def save_new_pa(self, msg: types.Message):
    #     if self.data_client.place_exist(msg.text):
    #         place_id = self.data_client.get_place_id(msg.text)
    #         result = self.data_client.set_place_admin(user_id=msg.from_user.id,
    #                                                   user_name=msg.from_user.full_name,
    #                                                   place_id=place_id)
    #         if result:
    #             await msg.answer(f"Вы успешно зарегистрированы, как администратор {msg.text}.",
    #                              reply_markup=create_keyboards(self.btn_pa_main_menu))
    #             await FSMWorkProgram.pa_main_menu.set()
    #
    #         else:
    #             await msg.answer("Произошла ошибка. Сейчас зарегистрироваться нельзя")
    #     else:
    #         await msg.answer("Такого заведения нет, выберите из существующих.")
    async def to_admin(self, msg: types.Message):
        await msg.answer("Войдите в свой аккаунт, либо создайте новый.",
                         reply_markup=create_keyboards(self.btn_admin_place))
        await FSMWorkProgram.entrance_pa.set()

    def run_handler(self):
        dp.register_message_handler(self.to_admin,
                                    commands=["to_place_admin"],
                                    state="*")

        self.CreateAccount.run_handler()
        self.AuthorizationAdmin.run_handler()
        self.MainMenu.run_handler()

        # Run function

