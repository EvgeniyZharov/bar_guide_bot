from aiogram.dispatcher.filters.state import StatesGroup, State


MAIN_TOKEN = "6486870977:AAHeE8jNCvaGlmFfmWsLTHPzxhr0lKeAR40"

# host = "185.212.148.117"
# user = "user_4"
# password = "passWORD1234!"
host = "147.78.64.216"
user = "user1"
password = "pass123"

USER_STATUS = {
    "base": "01",
    "silver": "04",
    "gold": "10",
    "brilliant": "40",
}


interests = ["Фотографии", "Музыка", "Пение", "Фитнес", "Путешествия", "Рестораны"]


class FSMWorkProgram(StatesGroup):
    # Status for main menu
    main_menu = State()

    # 1-st variation work - get all places for category
    get_place_category = State()

    # 2-nd variation work - find place for it`s title
    set_title_place = State()

    # 3-rd variation work - find place for location
    set_self_location = State()

    # 4-st variation work - get all announces for category
    get_announce_category = State()
    get_announce = State()

    # Base states 1. For work with places info
    get_place = State()
    choice_place = State()
    # get_reviews = State()
    get_menu = State()
    get_meal = State()
    get_announces = State()
    set_review = State()
    set_review_rating = State()
    set_review_text = State()
    save_new_review = State()
    set_name_reservist = State()
    set_phone_reservist = State()
    set_date_reserve = State()
    set_time_reserve = State()
    set_count_visitors = State()
    save_reserve = State()
    save_new_reserve = State()

    # Admin work
    to_admin_main_menu = State()
    admin_main_menu = State()
    admin_settings = State()

    place_settings_option = State()
    # Place category settings
    set_place_category = State()
    set_place_category_title = State()
    set_place_category_description = State()
    save_new_place_category = State()
    # Place settings
    set_place = State()
    set_place_category_id = State()
    set_place_title = State()
    set_place_description = State()
    set_place_address = State()
    set_place_site_link = State()
    set_place_photo = State()
    set_place_contact = State()
    set_place_work_time = State()
    save_new_place = State()
    # Update place info
    choice_category_place_upd_inf = State()
    choice_place_upd_inf = State()
    upd_place_title = State()
    choice_upd_settings = State()
    save_upd_place_title = State()
    upd_place_description = State()
    save_upd_place_description = State()
    upd_place_contact = State()
    save_upd_place_contact = State()
    upd_place_site = State()
    save_upd_place_site = State()
    upd_place_menu = State()
    add_new_dish = State()
    set_dish_info = State()
    set_dish_photo = State()
    save_dish_info = State()
    del_dish_start = State()
    del_dish = State()



    announce_settings_option = State()
    # Announce category settings
    set_announce_category = State()
    set_announce_category_title = State()
    set_announce_category_description = State()
    save_new_announce_category = State()
    # Announce settings
    set_announce = State()
    set_announce_category_id = State()
    set_announce_place_id = State()
    set_announce_title = State()
    set_announce_description = State()
    set_announce_price = State()
    set_announce_link_ticker = State()
    set_announce_date = State()
    set_announce_time = State()
    set_announce_photo = State()

    # Place admin work
    entrance_pa = State()
    start_reg_pa = State()
    choice_place_category_reg_pa = State()
    choice_place_reg_pa = State()
    check_reg_pa = State()
    save_reg_pa = State()
    authorize_pa = State()
    success_entrance_pa = State()

    main_menu_pa = State()

    pa_settings_menu = State()
    # Settings of place information


    # Settings of announce information

    # Settings of menu information

    pa_reserve_menu = State()
    # Show list of reserves

    # Meet Servise
    meet_main_menu = State()
    meet_profile_settings = State()
    meet_change_enable = State()
    meet_save_enable = State()
    meet_change_name = State()
    meet_change_age = State()
    meet_change_image = State()
    meet_change_interests = State()
    meet_change_description = State()
    meet_change_prefer_place = State()
    meet_show_profile = State()
    meet_system_settings = State()
    meet_change_sex_find = State()
    meet_save_sex_find = State()
    meet_change_age_find = State()
    meet_save_age_find = State()
    meet_form_watch = State()

    meet_show_forms = State()

    # User settings menu
    user_settings_menu = State()
    user_set_meet_enable = State()


