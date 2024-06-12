from aiogram import types
from initial import bot, dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from dataClient.db_mysql import DataClient

from keyboards import create_keyboards
from config import FSMWorkProgram


class PlaceSettings:
    btn_admin_main_menu = ["Смотреть заведения",
                           "Найти заведение",
                           "Заведения рядом",
                           "Мероприятия",
                           "О проекте",
                           "Системные настройки"]
    btn_place_settings = ["Добавить категорию",
                          "Добавить заведение",
                          "Обновить информацию"]
    btn_place_upd_settings = ["Изменить название",
                              "Изменить описание",
                              "Изменить контакт",
                              "Изменить сайт",
                              "Изменить меню"]
    btn_upd_menu = ["Добавить позицию",
                    "Удалить позицию"]

    def __init__(self, data_client: DataClient):
        self.data_client = data_client

    def check_place_category(self, category_title: str) -> [bool, str]:
        if category_title:
            if not self.data_client.place_category_exist(category_title):
                return [True, f"Название принято, теперь введите описание для категории."]
            else:
                return [False, "Такое название уже добавлено."]
        else:
            return [False, "Неккоректное название.\nПовторите"]

    def check_place(self, place_title: str) -> [bool, str]:
        if place_title:
            if not self.data_client.place_exist(place_title):
                return [True, f"Название принято, теперь введите описание для заведения."]
            else:
                return [False, "Такое название уже добавлено."]
        else:
            return [False, "Неккоректное название.\nПовторите"]

    async def choice_option_place_settings(self, msg: types.Message):
        back_msg = "Выберите, какую операцию хотите выполнить."
        await msg.answer(back_msg,
                         reply_markup=create_keyboards(self.btn_place_settings, cancel_btn=True))
        await FSMWorkProgram.place_settings_option.set()

    @staticmethod
    async def start_set_new_place_category(msg: types.Message):
        await msg.answer("Введите название для новой категории.",
                         reply_markup=create_keyboards(list(), cancel_btn=True))
        await FSMWorkProgram.set_place_category.set()

    async def set_place_category_title(self, msg: types.Message, state: FSMContext):
        result = self.check_place_category(msg.text)
        if result[0]:
            async with state.proxy() as data:
                data["category_title"] = msg.text
            await msg.answer(result[1])
            await FSMWorkProgram.set_place_category_title.set()
        else:
            await msg.answer(result[1])

    @staticmethod
    async def set_place_category_description(msg: types.Message, state: FSMContext):
        if len(msg.text) > 10:
            async with state.proxy() as data:
                data["description"] = msg.text
                back_msg = f"Сохранить следующую информацию?\nНазвание: {data['category_title']}\n" \
                           f"Описание: {msg.text}"
                await msg.answer(back_msg,
                                 reply_markup=create_keyboards(list(), yes_no_btn=True))
                await FSMWorkProgram.set_place_category_description.set()
        else:
            await msg.answer("Неккоректное описание, повторите.")

    async def save_new_place_category(self, msg: types.Message, state: FSMContext):
        if msg.text == "Да":
            async with state.proxy() as data:
                result = self.data_client.set_place_category(title=data["category_title"],
                                                             description=data["description"])
            await msg.answer("Категория добавлена.",
                             reply_markup=create_keyboards(self.btn_place_settings, cancel_btn=True))
            await state.reset_data()
            await FSMWorkProgram.place_settings_option.set()
        else:
            await msg.answer("Начнем с начала, введите другое название.",
                             reply_markup=create_keyboards(list(), cancel_btn=True))
            await state.reset_data()
            await FSMWorkProgram.set_place_category.set()

    async def set_place(self, msg: types.Message):
        category_btn = self.data_client.get_place_category_list()[1]
        await msg.answer("Выберите категорию для нового места.",
                         reply_markup=create_keyboards(category_btn, cancel_btn=True))
        await FSMWorkProgram.set_place.set()

    async def set_category_id(self, msg: types.Message, state: FSMContext):
        if self.data_client.place_category_exist(msg.text):
            place_category_id = self.data_client.get_place_category_id(msg.text)
            async with state.proxy() as data:
                data["category_title"] = msg.text
                data["category_id"] = place_category_id
            await msg.answer("Введите название заведения",
                             reply_markup=create_keyboards(list(), cancel_btn=True))
            await FSMWorkProgram.set_place_category_id.set()
        else:
            await msg.answer("Нужно выбрать из предложенных вариантов.\nПовторите попытку")

    async def set_place_title(self, msg: types.Message, state: FSMContext):
        result = self.check_place(msg.text)
        if result[0]:
            async with state.proxy() as data:
                data["place_title"] = msg.text
            await msg.answer(result[1])
            await FSMWorkProgram.set_place_title.set()
        else:
            await msg.answer(result[1])

    async def set_place_description(self, msg: types.Message, state: FSMContext):
        if len(msg.text) > 10:
            async with state.proxy() as data:
                data["place_description"] = msg.text
                await msg.answer("Введите адрес заведения")
                await FSMWorkProgram.set_place_description.set()
        else:
            await msg.answer("Неккоректное название, повторите.")

    async def set_place_address(self, msg: types.Message, state: FSMContext):
        if len(msg.text) > 5:
            async with state.proxy() as data:
                data["place_address"] = msg.text
                await msg.answer("Введите ссылку на сайт заведения..")
                await FSMWorkProgram.set_place_address.set()
        else:
            await msg.answer("Неккоректное начение, повторите.")

    async def set_place_site_link(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["place_site"] = msg.text
            await msg.answer("Отправьте фото заведения.")
            await FSMWorkProgram.set_place_site_link.set()

    async def set_place_photo(self, msg: types.Message, state: FSMContext):
        if msg.content_type != "photo":
            await msg.answer("Необходимо фото. Повторите попытку.")
        else:
            async with state.proxy() as data:
                data["place_photo"] = msg.photo[-1]["file_id"]
            await msg.answer("Введите контакт заведения.")
            await FSMWorkProgram.set_place_photo.set()

    async def set_place_contact(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["place_contact"] = msg.text
            await msg.answer("Введите время работы заведения.")
            await FSMWorkProgram.set_place_contact.set()

    async def set_place_work_time(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["place_work_time"] = msg.text
            back_msg = f"Сохранить следующую информацию?\nНазвание: {data['place_title']}\n" \
                       f"Описание: {data['place_description']}\nКатегория: {data['category_title']}\n" \
                       f"Адрес: {data['place_address']}\nСайт: {data['place_site']}\n" \
                       f"Контакт: {data['place_contact']}\nВремя работы: {data['place_work_time']}"
            await msg.answer_photo(data["place_photo"], back_msg,
                                   reply_markup=create_keyboards(list(), yes_no_btn=True))

            await FSMWorkProgram.set_place_work_time.set()

    async def save_new_place(self, msg: types.Message, state: FSMContext):
        if msg.text == "Да":
            async with state.proxy() as data:
                result = self.data_client.set_place(title=data["place_title"],
                                                    description=data["place_description"],
                                                    category_id=data["category_id"],
                                                    address=data["place_address"],
                                                    site=data["place_site"],
                                                    contact=data["place_contact"],
                                                    work_time=data["place_work_time"],
                                                    photo_id=data["place_photo"])
            if result:
                await msg.answer("Заведение добавлено.",
                                 reply_markup=create_keyboards(self.btn_admin_main_menu))
            else:
                await msg.answer("Произошла ошибка, сейчас нельзя добавить новое заведение.",
                                 reply_markup=create_keyboards(self.btn_admin_main_menu))
            await state.reset_data()
            await FSMWorkProgram.admin_main_menu.set()
            await state.reset_data()
        elif msg.text == "Нет":
            category_list = self.data_client.get_place_category_list()
            await msg.answer("Начнем с начала, выберите категорию.",
                             reply_markup=create_keyboards(category_list, cancel_btn=True))
            await state.reset_data()
            await FSMWorkProgram.set_place.set()

    async def choice_category_place_upd_inf(self, msg: types.Message):
        btn = self.data_client.get_place_category_list()[1]
        await msg.answer("Выберите категорию заведения.",
                         reply_markup=create_keyboards(btn_list=btn, cancel_btn=True))
        await FSMWorkProgram.choice_category_place_upd_inf.set()

    async def choice_place_upd_inf(self, msg: types.Message, state: FSMContext):
        category_id = self.data_client.get_place_category_id(msg.text)
        async with state.proxy() as data:
            data["category"] = msg.text
            data["category_id"] = category_id
        btn = self.data_client.get_place_list(category_id=category_id)[1]
        await msg.answer("Выберите заведение из предложенных.",
                         reply_markup=create_keyboards(btn_list=btn, cancel_btn=True))
        await FSMWorkProgram.choice_place_upd_inf.set()

    async def choice_upd_settings(self, msg: types.Message, state: FSMContext):
        place_id = self.data_client.get_place_id(title=msg.text)
        async with state.proxy() as data:
            data["place"] = msg.text
            data["place_id"] = place_id

        await msg.answer("Вебрите, что нужно сделать.",
                         reply_markup=create_keyboards(self.btn_place_upd_settings, cancel_btn=True))

        await FSMWorkProgram.choice_upd_settings.set()

    async def upd_place_title(self, msg: types.Message):
        await msg.answer("Введите новое название для заведения")
        await FSMWorkProgram.upd_place_title.set()

    async def save_upd_place_title(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:

            res = self.data_client.upd_place_info(place_id=data["place_id"],
                                                  element="title",
                                                  new_value=msg.text)
            if res:
                await msg.answer("Новое название сохранено")
            else:
                await msg.answer("Новое название НЕ сохранено")
        await FSMWorkProgram.choice_upd_settings.set()

    async def upd_place_description(self, msg: types.Message):
        await msg.answer("Введите новое описание для заведения")
        await FSMWorkProgram.upd_place_description.set()

    async def save_upd_place_description(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:

            res = self.data_client.upd_place_info(place_id=data["place_id"],
                                                  element="description",
                                                  new_value=msg.text)
            if res:
                await msg.answer("Новое описание сохранено")
            else:
                await msg.answer("Новое описание НЕ сохранено")
        await FSMWorkProgram.choice_upd_settings.set()

    async def upd_place_contact(self, msg: types.Message):
        await msg.answer("Введите новый контакт для заведения")
        await FSMWorkProgram.upd_place_contact.set()

    async def save_upd_place_contact(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:

            res = self.data_client.upd_place_info(place_id=data["place_id"],
                                                  element="contact",
                                                  new_value=msg.text)
            if res:
                await msg.answer("Новый контакт сохранено")
            else:
                await msg.answer("Новый контакт НЕ сохранено")
        await FSMWorkProgram.choice_upd_settings.set()

    async def upd_place_site(self, msg: types.Message):
        await msg.answer("Введите новый сайт для заведения")
        await FSMWorkProgram.upd_place_site.set()

    async def save_upd_place_site(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:

            res = self.data_client.upd_place_info(place_id=data["place_id"],
                                                  element="site",
                                                  new_value=msg.text)
            if res:
                await msg.answer("Новый сайт сохранено")
            else:
                await msg.answer("Новый сайт НЕ сохранено")
        await FSMWorkProgram.choice_upd_settings.set()

    async def upd_place_menu(self, msg: types.Message):
        await msg.answer("Выберите вариант изменения меню",
                         reply_markup=create_keyboards(self.btn_upd_menu, cancel_btn=True))
        await FSMWorkProgram.upd_place_menu.set()

    async def add_new_dish(self, msg: types.Message):
        await msg.answer("Введите для новой позиции: название/описание/состав/цену")
        await FSMWorkProgram.add_new_dish.set()

    async def set_dish_info(self, msg: types.Message, state: FSMContext):
        new_dish = msg.text.split('/')
        title, description, composition, price = new_dish[0], new_dish[1], new_dish[2], new_dish[3]
        async with state.proxy() as data:
            data["dish_title"] = title
            data["dish_description"] = description
            data["dish_composition"] = composition
            data["dish_price"] = price
            await msg.answer("Теперь отправьте фото для блюда")
        await FSMWorkProgram.set_dish_info.set()

    async def set_dish_photo(self, msg: types.Message, state: FSMContext):
        if msg.content_type != "photo":
            await msg.answer("Необходимо фото. Повторите попытку.")
        else:
            async with state.proxy() as data:
                data["dish_photo"] = msg.photo[-1]["file_id"]
            await msg.answer("Сохарнить информацию?",
                             reply_markup=create_keyboards(btn_list=list(), yes_no_btn=True, cancel_btn=True))
            await FSMWorkProgram.set_dish_photo.set()

    async def save_dish_info(self, msg: types.Message, state: FSMContext):
        if msg.text == "Да":
            async with state.proxy() as data:
                result = self.data_client.set_menu(place_id=data["place_id"],
                                                   title=data["dish_title"],
                                                   description=data["dish_description"],
                                                   composition=data["dish_composition"],
                                                   price=data["dish_price"],
                                                   image_id=data["dish_photo"])
            await msg.answer("Блюдо добавлено.",
                             reply_markup=create_keyboards(self.btn_place_settings, cancel_btn=True))
            await state.reset_data()
            await FSMWorkProgram.choice_upd_settings.set()
        else:
            await msg.answer("Начнем с начала, введите другое название.",
                             reply_markup=create_keyboards(list(), cancel_btn=True))
            await state.reset_data()
            await FSMWorkProgram.set_dish_info.set()
        await FSMWorkProgram.save_dish_info.set()

    async def del_dish_start(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            btn = self.data_client.get_menu_list(place_id=data["place_id"])
            await msg.answer("Выберите блюдо, которое хотите удалить",
                             reply_markup=create_keyboards(btn, cancel_btn=True))
            await FSMWorkProgram.del_dish.set()

    async def del_dish(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            res = self.data_client.del_menu
            if res:
                await msg.answer("Позиция удалена")
            else:
                await msg.answer("Произошла ошибка.")







    def run_handler(self):
        dp.register_message_handler(self.choice_option_place_settings,
                                    Text(equals="Настройки: заведения", ignore_case=True),
                                    state=FSMWorkProgram.admin_settings)

        # dp.register_message_handler(self.choice_option_place_settings,
        #                             Text(equals="Добавить категорию", ignore_case=True),
        #                             state=FSMWorkProgram.admin_choice_settings_option)

        dp.register_message_handler(self.start_set_new_place_category,
                                    Text(equals="Добавить категорию", ignore_case=True),
                                    state=FSMWorkProgram.place_settings_option)
        dp.register_message_handler(self.set_place_category_title,
                                    state=FSMWorkProgram.set_place_category)
        dp.register_message_handler(self.set_place_category_description,
                                    state=FSMWorkProgram.set_place_category_title)
        dp.register_message_handler(self.save_new_place_category,
                                    state=FSMWorkProgram.set_place_category_description)

        dp.register_message_handler(self.set_place,
                                    Text(equals="Добавить заведение", ignore_case=True),
                                    state=FSMWorkProgram.place_settings_option)
        dp.register_message_handler(self.set_category_id,
                                    state=FSMWorkProgram.set_place)
        dp.register_message_handler(self.set_place_title,
                                    state=FSMWorkProgram.set_place_category_id)
        dp.register_message_handler(self.set_place_description,
                                    state=FSMWorkProgram.set_place_title)
        dp.register_message_handler(self.set_place_address,
                                    state=FSMWorkProgram.set_place_description)
        dp.register_message_handler(self.set_place_site_link,
                                    state=FSMWorkProgram.set_place_address)
        dp.register_message_handler(self.set_place_photo,
                                    state=FSMWorkProgram.set_place_site_link,
                                    content_types=["photo"])
        dp.register_message_handler(self.set_place_contact,
                                    state=FSMWorkProgram.set_place_photo)
        dp.register_message_handler(self.set_place_work_time,
                                    state=FSMWorkProgram.set_place_contact)
        dp.register_message_handler(self.save_new_place,
                                    state=FSMWorkProgram.set_place_work_time)

        dp.register_message_handler(self.choice_category_place_upd_inf,
                                    Text(equals="Обновить информацию", ignore_case=True),
                                    state=FSMWorkProgram.place_settings_option)
        dp.register_message_handler(self.choice_place_upd_inf,
                                    state=FSMWorkProgram.choice_category_place_upd_inf)
        dp.register_message_handler(self.choice_upd_settings,
                                    state=FSMWorkProgram.choice_place_upd_inf)
        dp.register_message_handler(self.upd_place_title,
                                    Text(equals="Изменить название", ignore_case=True),
                                    state=FSMWorkProgram.choice_upd_settings)
        dp.register_message_handler(self.save_upd_place_title,
                                    state=FSMWorkProgram.upd_place_title)
        dp.register_message_handler(self.upd_place_description,
                                    Text(equals="Изменить описание", ignore_case=True),
                                    state=FSMWorkProgram.choice_upd_settings)
        dp.register_message_handler(self.save_upd_place_description,
                                    state=FSMWorkProgram.upd_place_description)
        dp.register_message_handler(self.upd_place_contact,
                                    Text(equals="Изменить контакт", ignore_case=True),
                                    state=FSMWorkProgram.choice_upd_settings)
        dp.register_message_handler(self.save_upd_place_contact,
                                    state=FSMWorkProgram.upd_place_contact)
        dp.register_message_handler(self.upd_place_site,
                                    Text(equals="Изменить сайт", ignore_case=True),
                                    state=FSMWorkProgram.choice_upd_settings)
        dp.register_message_handler(self.save_upd_place_site,
                                    state=FSMWorkProgram.upd_place_site)
        dp.register_message_handler(self.upd_place_menu,
                                    Text(equals="Изменить меню", ignore_case=True),
                                    state=FSMWorkProgram.choice_upd_settings)
        dp.register_message_handler(self.add_new_dish,
                                    Text(equals="Добавить позицию", ignore_case=True),
                                    state=FSMWorkProgram.upd_place_menu)
        dp.register_message_handler(self.set_dish_info,
                                    state=FSMWorkProgram.add_new_dish)
        dp.register_message_handler(self.set_dish_photo,
                                    state=FSMWorkProgram.set_dish_info,
                                    content_types=["photo"])
        dp.register_message_handler(self.save_dish_info,
                                    state=FSMWorkProgram.set_dish_photo)
        dp.register_message_handler(self.del_dish_start,
                                    Text(equals="Удалить позицию", ignore_case=True),
                                    state=FSMWorkProgram.upd_place_menu)
        dp.register_message_handler(self.del_dish,
                                    state=FSMWorkProgram.del_dish_start)


