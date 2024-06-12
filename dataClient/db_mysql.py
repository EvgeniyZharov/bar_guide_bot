from geopy.geocoders import Nominatim
from geopy.distance import geodesic as GD
import pymysql
import time
from config import host, user, password


class DataClient:
    DATABASE_NAME = "bar_guide_bot"
    actual_version = "a0.1"
    TABLES = ["place_category", "announce_category", "user", "place",
              "announce", "menu", "review", "reserve", "place_admin"]
    drop_tables = ["place_admin", "reserve", "review", "menu", "announce",
                   "announce_category", "user", "place", "place_category"]

    def connect(self):
        self.con = pymysql.Connection(
            host=self.host,
            user=self.user,
            port=3306,
            password=self.password,
            use_unicode=True,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )

    def __init__(self, host: str, user: str, password: str):
        self.geolocator = Nominatim(user_agent="Bar Guide")
        self.host = host
        self.user = user
        self.password = password
        self.connect()
        self.create_db()
        print(self.create_all_tables())

    def create_db(self, db_title: str = DATABASE_NAME) -> bool:
        try:
            request = f"CREATE DATABASE IF NOT EXISTS {db_title} CHARACTER SET utf8 COLLATE utf8_general_ci;"
            with self.con.cursor() as cur:
                cur.execute(request)
                self.con.commit()
                return True
        except Exception:
            return False

    def create_table(self, request: str) -> bool:
        try:
            with self.con.cursor() as cur:
                cur.execute(request)
                self.con.commit()
                return True
        except Exception as ex:
            print(ex)
            return False

    def create_place_category_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.place_category (id int AUTO_INCREMENT PRIMARY KEY,
                      title VARCHAR(50) UNIQUE NOT NULL,
                      description TEXT,
                      permission VARCHAR(20) DEFAULT '1',
                      version VARCHAR(10) DEFAULT '{self.actual_version}') CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_announce_category_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.announce_category (id int AUTO_INCREMENT PRIMARY KEY,
                      title VARCHAR(50) UNIQUE NOT NULL,
                      description TEXT,
                      permission VARCHAR(20) DEFAULT '1',
                      version VARCHAR(10) DEFAULT '{self.actual_version}'
                      ) CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_place_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.place (id int AUTO_INCREMENT PRIMARY KEY,
                      category_id int NOT NULL,
                      title VARCHAR(50) NOT NULL,
                      description TEXT NOT NULL,
                      address VARCHAR(200) NOT NULL,
                      rating float NOT NULL,
                      position VARCHAR(200) NOT NULL,
                      site VARCHAR(100) NOT NULL,
                      contact VARCHAR(100) NOT NULL,
                      work_time VARCHAR(50) NOT NULL,
                      photo_id VARCHAR(200) NOT NULL,
                      permission VARCHAR(20) DEFAULT '1',
                      version VARCHAR(10) DEFAULT '{self.actual_version}',
                      UNIQUE(title, address),
                      FOREIGN KEY(category_id) REFERENCES place_category(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_announce_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.announce (id int AUTO_INCREMENT PRIMARY KEY,
                      category_id int NOT NULL,
                      place_id int NOT NULL,
                      title VARCHAR(50) UNIQUE NOT NULL,
                      description TEXT NOT NULL,
                      ticker_price VARCHAR(50) NOT NULL,
                      ticker_link VARCHAR(100) NOT NULL,
                      date VARCHAR(50) NOT NULL,
                      time VARCHAR(50) NOT NULL,
                      photo_id VARCHAR(200),
                      permission VARCHAR(20) DEFAULT '1',
                      version VARCHAR(10) DEFAULT '{self.actual_version}',

                      FOREIGN KEY(category_id) REFERENCES announce_category(id) ON DELETE CASCADE ON UPDATE CASCADE,
                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_user_table(self) -> bool:
        default_photo_id = "AgACAgIAAxkBAAIPJmZnWTLWJbGxOPchUTogqbF7lwz5AALM3DEbCjU4S_zPWg7Po9C7AQADAgADeQADNQQ"
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.user (id int AUTO_INCREMENT PRIMARY KEY,
                      status VARCHAR(50) NOT NULL default 'base',
                      name VARCHAR(100) NOT NULL,
                      tg_id VARCHAR(50) UNIQUE NOT NULL,
                      tg_nick VARCHAR(100) UNIQUE NOT NULL,
                      photo_id VARCHAR(100) NOT NULL default '{default_photo_id}',
                      contact VARCHAR(20) NOT NULL,
                      age int,
                      age_find VARCHAR(10),
                      interests VARCHAR(300),
                      prefer_place VARCHAR(300),
                      sex CHAR,
                      sex_find CHAR,
                      description TEXT,
                      meet_enabled CHAR NOT NULL DEFAULT '0',
                      version VARCHAR(10) DEFAULT '{self.actual_version}',
                      permissions VARCHAR(20) DEFAULT '1') CHARACTER SET utf8;"""

        return self.create_table(request=request)

    def create_menu_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.menu (id int AUTO_INCREMENT PRIMARY KEY,
                      place_id int NOT NULL,
                      title VARCHAR(50) NOT NULL,
                      description TEXT NOT NULL,
                      composition TEXT NOT NULL,
                      price VARCHAR(20) NOT NULL,
                      image_id VARCHAR(200) NOT NULL,
                      version VARCHAR(10) DEFAULT '{self.actual_version}',

                      UNIQUE(title, place_id),
                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_review_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.review (id int AUTO_INCREMENT PRIMARY KEY,
                      place_id int NOT NULL,
                      user_name VARCHAR(50) NOT NULL,
                      user_id VARCHAR(50) NOT NULL,
                      text TEXT NOT NULL,
                      rating int NOT NULL,  
                      permission VARCHAR(20) DEFAULT '1',
                      version VARCHAR(10) DEFAULT '{self.actual_version}',

                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_reserve_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.reserve (id int AUTO_INCREMENT PRIMARY KEY,
                      place_id int NOT NULL,
                      user_name VARCHAR(50) NOT NULL,
                      user_id VARCHAR(50) NOT NULL,
                      date VARCHAR(50) NOT NULL,
                      time VARCHAR(50) NOT NULL,
                      user_number VARCHAR(20) NOT NULL,
                      permission VARCHAR(20) DEFAULT '1',
                      version VARCHAR(10) DEFAULT '{self.actual_version}',

                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_place_admin_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.place_admin (id int AUTO_INCREMENT PRIMARY KEY,
                      place_id int NOT NULL,
                      user_name VARCHAR(50) NOT NULL,
                      user_pass VARCHAR(20) NOT NULL,
                      login VARCHAR(30) NOT NULL,
                      user_id VARCHAR(50) NOT NULL, 
                      status_reg VARCHAR(10) NOT NULL,
                      last_connect VARCHAR(20) NOT NULL,
                      version VARCHAR(10) DEFAULT '{self.actual_version}',

                      UNIQUE(place_id, user_id),
                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_trip_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.trip (id int AUTO_INCREMENT PRIMARY KEY,
                      title int NOT NULL UNIQUE,
                      version VARCHAR(10) DEFAULT '{self.actual_version}',
                      description TEXT)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_trip_stages_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.trip_stages (id int AUTO_INCREMENT PRIMARY KEY,
                      trip_id int NOT NULL,
                      place_id int,
                      order_place int NOT NULL,
                      description TEXT NOT NULL,
                      version VARCHAR(10) DEFAULT '{self.actual_version}',

                      FOREIGN KEY(trip_id) REFERENCES trip(id) ON DELETE CASCADE ON UPDATE CASCADE,
                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_discounts_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.discounts (id int AUTO_INCREMENT PRIMARY KEY,
                      place_id int NOT NULL,
                      description TEXT NOT NULL,
                      dates VARCHAR(30) NOT NULL,
                      version VARCHAR(10) DEFAULT '{self.actual_version}',

                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_workers_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.workers (id int AUTO_INCREMENT PRIMARY KEY,
                      name VARCHAR(30) NOT NULL UNIQUE,
                      place_id int NOT NULL,
                      tg_id VARCHAR(20) NOT NULL,
                      user_id int NOT NULL,
                      version VARCHAR(10) DEFAULT '{self.actual_version}',

                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE,
                      FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_tips_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.tips (id int AUTO_INCREMENT PRIMARY KEY,
                      worker_id int NOT NULL,
                      place_id int NOT NULL,
                      payment float NOT NULL,
                      version VARCHAR(10) DEFAULT '{self.actual_version}',

                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE,
                      FOREIGN KEY(worker_id) REFERENCES workers(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_lovers_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.lovers (id int AUTO_INCREMENT PRIMARY KEY,
                      user_id int NOT NULL,
                      purpose_user_id int NOT NULL,
                      status_match char NOT NULL,
                      version VARCHAR(10) DEFAULT '{self.actual_version}',

                      FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE,
                      FOREIGN KEY(purpose_user_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_category_interest_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.category_interest 
                      (id int AUTO_INCREMENT PRIMARY KEY,
                      version VARCHAR(10) DEFAULT '{self.actual_version}',
                      title VARCHAR(50) NOT NULL UNIQUE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_interest_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.interest (id int AUTO_INCREMENT PRIMARY KEY,
                      title VARCHAR(50) NOT NULL UNIQUE,
                      category_id int NOT NULL,
                      version VARCHAR(10) DEFAULT '{self.actual_version}',
                      
                      FOREIGN KEY(category_id) REFERENCES category_interest(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_user_interest_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.user_interest (id int AUTO_INCREMENT PRIMARY KEY,
                      interest_id int not null,
                      user_id int not null,
                      version VARCHAR(10) DEFAULT '{self.actual_version}',
                      
                      UNIQUE(user_id, interest_id),
                      FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE,
                      FOREIGN KEY(interest_id) REFERENCES interest(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_favorite_place_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.favorite_place (id int AUTO_INCREMENT PRIMARY KEY,
                      place_id int NOT NULL,
                      user_id int NOT NULL,
                      version VARCHAR(10) DEFAULT '{self.actual_version}',

                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE,
                      FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_category_event_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.category_event (id int AUTO_INCREMENT PRIMARY KEY,
                      title VARCHAR(50) NOT NULL UNIQUE,
                      version VARCHAR(10) DEFAULT '{self.actual_version}',
                      description TEXT)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_event_table(self) -> bool:
        image_link_default = "AgACAgIAAxkBAAISjmZosd86mjH3J7DmxM7QHrfrdRntAAJY1jEbdw5JSzR3wkznFzFEAQADAgADeQADNQQ"
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.event (id int AUTO_INCREMENT PRIMARY KEY,
                      category_id int NOT NULL,
                      title VARCHAR(50) NOT NULL,
                      description TEXT NOT NULL,
                      time VARCHAR(50) NOT NULL,
                      link VARCHAR(100) NOT NULL,
                      image VARCHAR(150) NOT NULL DEFAULT '{image_link_default}',
                      address VARCHAR(100) NOT NULL,
                      contact VARCHAR(50) NOT NULL,
                      permission VARCHAR(20) DEFAULT '1',
                      version VARCHAR(10) DEFAULT '{self.actual_version}',

                      UNIQUE(category_id, title, address),
                      FOREIGN KEY(category_id) REFERENCES category_event(id) ON DELETE CASCADE ON UPDATE CASCADE)
                      CHARACTER SET utf8;"""
        return self.create_table(request=request)

    def create_all_tables(self) -> bool:
        result = (self.create_place_category_table()
                  & self.create_place_table()
                  & self.create_announce_category_table()
                  & self.create_announce_table()
                  & self.create_user_table()
                  & self.create_menu_table()
                  & self.create_review_table()
                  & self.create_reserve_table()
                  & self.create_place_admin_table()
                  & self.create_trip_table()
                  & self.create_trip_stages_table()
                  & self.create_discounts_table()
                  & self.create_workers_table()
                  & self.create_tips_table()
                  & self.create_lovers_table()
                  & self.create_category_interest_table()
                  & self.create_interest_table()
                  & self.create_user_interest_table()
                  & self.create_favorite_place_table()
                  & self.create_category_event_table()
                  & self.create_event_table())
        return result

    def drop_table(self, table_title: str):
        request = f"DROP TABLE {self.DATABASE_NAME}.{table_title}"
        with self.con.cursor() as cur:
            cur.execute(request)

    def drop_all_tables(self) -> bool:
        try:
            for elem in self.drop_tables:
                self.drop_table(elem)
            return True
        except Exception as ex:
            print(ex)
            return False

    def set_new_data(self,
                     request: str,
                     record: list) -> bool:
        try:
            with self.con.cursor() as cur:
                cur.executemany(request, record)
                self.con.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def run_request(self,
                    request: str) -> bool:
        try:
            with self.con.cursor() as cur:
                cur.execute(query=request)
                self.con.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def set_place_category(self,
                           title: str,
                           description: str) -> bool:
        request = f"INSERT INTO {self.DATABASE_NAME}.place_category (title, description) " \
                  "VALUES (%s, %s);"
        record = [(title, description)]
        return self.set_new_data(request=request, record=record)

    def set_announce_category(self,
                              title: str,
                              description: str) -> bool:
        request = f"INSERT INTO {self.DATABASE_NAME}.announce_category (title, description) " \
                  "VALUES (%s, %s);"
        record = [(title, description)]
        return self.set_new_data(request=request, record=record)

    def set_place(self,
                  category_id: int,
                  title: str,
                  description: str,
                  address: str,
                  site: str,
                  contact: str,
                  work_time: str,
                  photo_id: str) -> bool:
        try:
            location = self.geolocator.geocode(address)
            position = f"{location.latitude}_{location.longitude}"
        except Exception:
            position = "0_0"
        rating = 0.
        request = f"INSERT INTO {self.DATABASE_NAME}.place (category_id, title, description," \
                  f"address, rating, position, site, contact, work_time, photo_id) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        record = [(category_id, title, description, address, rating, position, site, contact, work_time, photo_id)]
        return self.set_new_data(request=request, record=record)

    def set_announce(self,
                     category_id: int,
                     place_id: int,
                     title: str,
                     description: str,
                     ticker_price: str,
                     ticker_link: str,
                     date: str,
                     time_value: str,
                     photo_id: str) -> bool:
        request = f"INSERT INTO {self.DATABASE_NAME}.announce (category_id, place_id, title, " \
                  f"description, ticker_price, ticker_link, date, time, photo_id) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        record = [(category_id, place_id, title, description, ticker_price, ticker_link, date, time_value, photo_id)]
        return self.set_new_data(request=request, record=record)

    def set_user(self,
                 name: str,
                 tg_id: str,
                 tg_nick: str,
                 contact: str = "0") -> bool:
        status = "base"
        request = f"INSERT INTO {self.DATABASE_NAME}.user (status, name, tg_id, tg_nick, contact) " \
                  "VALUES (%s, %s, %s, %s, %s);"
        record = [(status, name, tg_id, tg_nick, contact)]
        return self.set_new_data(request=request, record=record)

    def set_menu(self,
                 place_id: int,
                 title: str,
                 description: str,
                 composition: str,
                 price: str,
                 image_id: str) -> bool:
        request = f"INSERT INTO {self.DATABASE_NAME}.menu (place_id, title, description," \
                  f"composition, price, image_id) " \
                  "VALUES (%s, %s, %s, %s, %s, %s);"
        record = [(place_id, title, description, composition, price, image_id)]
        return self.set_new_data(request=request, record=record)

    def set_review(self,
                   place_id: int,
                   user_name: str,
                   user_id: str,
                   text: str,
                   rating: int) -> bool:
        request = f"INSERT INTO {self.DATABASE_NAME}.review (place_id, user_name, user_id," \
                  f"text, rating) " \
                  "VALUES (%s, %s, %s, %s, %s);"
        record = [(place_id, user_name, user_id, text, rating)]
        # rating = self.get_info(f"SELECT rating from {self.DATABASE_NAME}.place where ")
        return self.set_new_data(request=request, record=record)

    def set_reserve(self,
                    place_id: int,
                    user_name: str,
                    user_id: str,
                    date: str,
                    time_value: str,
                    user_number: str) -> bool:
        request = f"INSERT INTO {self.DATABASE_NAME}.reserve (place_id, user_name, user_id," \
                  f"date, time, user_number) " \
                  "VALUES (%s, %s, %s, %s, %s, %s);"
        record = [(place_id, user_name, user_id, date, time_value, user_number)]
        return self.set_new_data(request=request, record=record)

    def set_place_admin(self,
                        place_id: int,
                        user_name: str,
                        user_pass: str,
                        login: str,
                        user_id: str,
                        status_reg: str = "0",
                        last_connect: str = "0") -> bool:
        request = f"INSERT INTO {self.DATABASE_NAME}.place_admin (place_id, user_name, user_id, user_pass, login, " \
                  f"status_reg, last_connect) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s);"
        record = [(place_id, user_name, user_id, user_pass, login, status_reg, last_connect)]
        return self.set_new_data(request=request, record=record)

    def set_worker_tip(self, worker_id: int, place_id: int, value_tip: int) -> bool:
        request = f"""INSERT INTO {self.DATABASE_NAME}.tips (worker_id, place_id, payment) 
                      values ({worker_id}, {place_id}, '{value_tip}');"""
        return self.run_request(request=request)

    def get_table_info(self, table_title: str) -> dict:
        if table_title in self.TABLES:
            request = f"SELECT * FROM {self.DATABASE_NAME}.{table_title};"
            with self.con.cursor() as cur:
                cur.execute(request)
            return cur.fetchall()

    def get_info(self, request: str) -> list:
        with self.con.cursor() as cur:
            cur.execute(request)
        return cur.fetchall()

    def get_list_values(self, request: str, key: str = "title") -> list:
        values = list()
        with self.con.cursor() as cur:
            cur.execute(request)
            for elem in cur.fetchall():
                values.append(elem[key])
        return values

    def get_exist(self, request: str) -> bool:
        with self.con.cursor() as cur:
            cur.execute(request)
        return len(cur.fetchall()) != 0

    def update_table(self, request: str) -> bool:
        try:
            with self.con.cursor() as cur:
                cur.execute(request)
                self.con.commit()
            return True
        except Exception:
            return False

    def get_place_info(self, title) -> dict:
        request = f"SELECT * FROM {self.DATABASE_NAME}.place WHERE title = '{title}';"
        return self.get_info(request=request)[0]

    def get_announce_info_for_title(self, title: str) -> dict:
        request = f"SELECT * FROM {self.DATABASE_NAME}.announce WHERE title = '{title}';"
        return self.get_info(request=request)[0]

    def get_announce_info_for_place(self, place_id: int, title: str) -> dict:
        request = f"SELECT * FROM {self.DATABASE_NAME}.place WHERE title = '{title}' AND place_id = '{place_id}';"
        return self.get_info(request=request)[0]

    def get_place_category(self) -> [bool, list]:
        request = f"SELECT title FROM {self.DATABASE_NAME}.place_category;"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_announce_category(self) -> [bool, list]:
        request = f"SELECT title FROM {self.DATABASE_NAME}.announce_category;"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_place_from_category(self, category_id: int) -> [bool, list]:
        request = f"SELECT title FROM {self.DATABASE_NAME}.place WHERE category_id = '{category_id}';"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_announce_from_category(self, category_id: int) -> [bool, list]:
        request = f"SELECT title FROM {self.DATABASE_NAME}.announce WHERE category_id = '{category_id}';"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_suitable_place(self, title: str) -> [bool, list]:
        request = f"SELECT title FROM {self.DATABASE_NAME}.place;"
        result = self.get_list_values(request=request)
        new_result = [elem for elem in result if title in elem]
        return [len(new_result) > 0, new_result]

    def get_near_position_place(self, position: str, radius: float = 5.0) -> [bool, list]:
        request = f"SELECT title, position FROM {self.DATABASE_NAME}.place;"
        result = self.get_info(request=request)
        user_lat = position.split("_")[0]
        user_long = position.split("_")[1]
        places = list()
        for elem in result:
            place_pos = elem["position"].split("_")
            place_lat = place_pos[0]
            place_long = place_pos[1]
            distance = round(GD((user_lat, user_long), (place_lat, place_long)).km, 2)
            if distance <= radius:
                places.append(elem["title"])
        return [len(places) > 0, places]

    def get_meal_list(self, place_id: int) -> [bool, list]:
        request = f"SELECT title FROM {self.DATABASE_NAME}.menu WHERE place_id = {place_id};"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_meal_info(self, title: str, place_id: int) -> dict:
        request = f"SELECT * FROM {self.DATABASE_NAME}.menu WHERE place_id = '{place_id}';"
        return self.get_info(request=request)[0]

    def get_place_review(self, place_id: int, limit: int = 3) -> [bool, [dict]]:
        request = f"SELECT * FROM {self.DATABASE_NAME}.review WHERE place_id = '{place_id}' " \
                  f"order by id desc limit {limit};"
        result = self.get_info(request=request)
        return [len(result) > 0, result]

    #
    # def get_all_review(self):
    #     for elem in self.data["review"]:
    #         print(elem["user_name"])

    def get_place_announce(self, place_id: int) -> [bool, list]:
        request = f"SELECT title FROM {self.DATABASE_NAME}.announce WHERE place_id = {place_id};"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    # def set_new_review(self,
    #                    place_id: int,
    #                    user_name: str,
    #                    user_link: str,
    #                    text: str,
    #                    rating: float):
    #     try:
    #         index = len(self.data["review"])
    #         template = self.templates["review"].copy()
    #         template["id"] = index
    #         template["place_id"] = place_id
    #         template["user_name"] = user_name
    #         template["user_link"] = user_link
    #         template["text"] = text
    #         template["rating"] = rating
    #         self.data["review"].append(template)
    #         return True
    #     except Exception:
    #         return False

    # def set_new_reserve(self,
    #                     place_id: int,
    #                     user_name: str,
    #                     user_link: str,
    #                     date: str,
    #                     time: str,
    #                     user_number: str):
    #     try:
    #         index = len(self.data["reserve"])
    #         template = self.templates["reserve"].copy()
    #         template["id"] = index
    #         template["place_id"] = place_id
    #         template["user_name"] = user_name
    #         template["user_link"] = user_link
    #         template["date"] = date
    #         template["time"] = time
    #         template["user_number"] = user_number
    #         self.data["reserve"].append(template)
    #         return True
    #     except Exception:
    #         return False

    def get_all_reserves(self, place_id: int):
        request = f"SELECT * FROM {self.DATABASE_NAME}.reserve WHERE place_id = '{place_id}';"
        result = self.get_info(request=request)
        return [len(result) > 0, result]

    ################################

    def user_exist(self, user_id: str) -> bool:
        request = f"SELECT * FROM {self.DATABASE_NAME}.user WHERE tg_id = '{user_id}';"
        return self.get_exist(request)

    def set_new_admin(self, user_id: str) -> bool:
        request = f"UPDATE {self.DATABASE_NAME}.user SET status = 'admin' WHERE tg_id = '{user_id}';"
        return self.update_table(request=request)

    def user_is_admin(self, user_id: str) -> bool:
        request = f"SELECT * FROM {self.DATABASE_NAME}.user WHERE tg_id = '{user_id}' AND status = 'admin';"
        return self.get_exist(request)

    def user_is_pa(self, user_id: str) -> bool:
        request = f"SELECT * FROM {self.DATABASE_NAME}.place_admin WHERE user_id = '{user_id}';"
        return self.get_exist(request)

    def pa_is_exist(self, user_id: str) -> bool:
        request = f"select * from {self.DATABASE_NAME}.place_admin where user_id = '{user_id}';"
        return self.get_exist(request=request)

    def place_category_exist(self, category_title: str) -> bool:
        request = f"SELECT * FROM {self.DATABASE_NAME}.place_category WHERE title = '{category_title}';"
        return self.get_exist(request)

    def place_exist(self, place_title: str) -> bool:
        request = f"SELECT * FROM {self.DATABASE_NAME}.place WHERE title = '{place_title}';"
        return self.get_exist(request)

    def get_place_category_list(self) -> list:
        request = f"SELECT title FROM {self.DATABASE_NAME}.place_category;"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_announce_category_list(self) -> list:
        request = f"SELECT title FROM {self.DATABASE_NAME}.announce_category;"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_all_place_list(self) -> list:
        request = f"SELECT title FROM {self.DATABASE_NAME}.place;"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_place_list(self, category_id: int) -> list:
        request = f"SELECT title FROM {self.DATABASE_NAME}.place WHERE category_id = '{category_id}';"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_menu_list(self, place_id: int) -> list:
        request = f"SELECT title FROM {self.DATABASE_NAME}.menu WHERE place_id = '{place_id}';"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_category_interest_list(self) -> list:
        request = f"SELECT title FROM {self.DATABASE_NAME}.category_interest;"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_interest_list(self, category_id: int, user_id: int) -> list:

        request = f"SELECT title, if(i.id IN (SELECT interest_id FROM {self.DATABASE_NAME}.user_interest " \
                  f"WHERE user_id = '{user_id}'), ':on', ':off') as res " \
                  f"FROM {self.DATABASE_NAME}.interest as i " \
                  f"WHERE category_id = '{category_id}';"
        result = self.get_info(request=request)
        return [len(result) > 0, result]

    def get_worker_from_place_list(self, place_id: int) -> list:
        request = f"SELECT name from {self.DATABASE_NAME}.workers WHERE place_id = '{place_id}';"
        result = self.get_list_values(request=request, key="name")
        return [len(result) > 0, result]

    def announce_category_exist(self, category_title: str) -> bool:
        request = f"SELECT * FROM {self.DATABASE_NAME}.announce_category WHERE title = '{category_title}';"
        return self.get_exist(request)

    def announce_exist(self, announce_title: str) -> bool:
        request = f"SELECT * FROM {self.DATABASE_NAME}.announce WHERE title = '{announce_title}';"
        return self.get_exist(request)

    def get_place_category_id(self, title: str) -> int:
        request = f"SELECT id FROM {self.DATABASE_NAME}.place_category WHERE title = '{title}';"
        return self.get_info(request=request)[0]["id"]

    def get_announce_category_id(self, title: str) -> int:
        request = f"SELECT id FROM {self.DATABASE_NAME}.announce_category WHERE title = '{title}';"
        return self.get_info(request=request)[0]["id"]

    def get_place_id(self, title: str) -> int:
        request = f"SELECT id FROM {self.DATABASE_NAME}.place WHERE title = '{title}';"
        return self.get_info(request=request)[0]["id"]

    def get_category_interest_id(self, title: str) -> int:
        request = f"SELECT id FROM {self.DATABASE_NAME}.category_interest WHERE title = '{title}';"
        return self.get_info(request=request)[0]["id"]

    def get_interest_id(self, title: str) -> int:
        request = f"SELECT id FROM {self.DATABASE_NAME}.interest WHERE title = '{title}';"
        return self.get_info(request=request)[0]["id"]

    def get_user_id(self, tg_id: str) -> int:
        request = f"SELECT id FROM {self.DATABASE_NAME}.user WHERE tg_id = '{tg_id}';"
        return self.get_info(request=request)[0]["id"]

    def get_worker_id(self, place_id: int, name: str) -> int:
        request = f"SELECT id FROM {self.DATABASE_NAME}.workers " \
                  f"WHERE place_id = '{place_id}' AND name = '{name}';"
        return self.get_info(request=request)[0]["id"]

    def get_place_description(self, place_id: int) -> str:
        request = f"SELECT description FROM {self.DATABASE_NAME}.place WHERE id = '{place_id}';"
        return self.get_info(request=request)[0]["description"]

    def get_place_contact(self, place_id: int) -> str:
        request = f"SELECT contact FROM {self.DATABASE_NAME}.place WHERE id = '{place_id}';"
        return self.get_info(request=request)[0]["contact"]

    def get_place_site(self, place_id: int) -> str:
        request = f"SELECT site FROM {self.DATABASE_NAME}.place WHERE id = '{place_id}';"
        return self.get_info(request=request)[0]["site"]

    def get_user_info_meet(self, user_id: int) -> [bool, dict]:
        request = f"""
            select a.name, a.age, a.interests, a.prefer_place, a.description, a.photo_id, a.id
            from {self.DATABASE_NAME}.user as a, {self.DATABASE_NAME}.user as b 
            where a.meet_enabled = '1' and a.sex = b.sex_find 
            and b.tg_id = '{user_id}' and a.id not in 
            (select purpose_user_id from {self.DATABASE_NAME}.lovers where user_id = b.id) limit 1;"""
        result = self.get_info(request=request)
        return [len(result) > 0, result]

    def get_user_tg_nick(self, user_id: int) -> str:
        request = f"""select tg_nick from {self.DATABASE_NAME}.user where id = '{user_id}';"""
        return self.get_info(request=request)[0]["tg_nick"]

    def get_user_tg_id(self, user_id: int) -> str:
        request = f"""select tg_id from {self.DATABASE_NAME}.user where id = '{user_id}';"""
        return self.get_info(request=request)[0]["tg_id"]

    def set_user_reaction_meet(self, user_id: int, purpose_user_id: int, reaction: str) -> bool:
        request = f"""insert into {self.DATABASE_NAME}.lovers (user_id, purpose_user_id, status_match) 
            values ((select id from {self.DATABASE_NAME}.user where tg_id = '{user_id}'), '{purpose_user_id}', '{reaction}');"""
        return self.run_request(request=request)

    def set_favorite_place(self, user_tg_id: str, place_id: int):
        request = f"""
                   insert into {self.DATABASE_NAME}.favorite_place (place_id, user_id) 
                   values ('{place_id}', (select id from bar_guide_bot.user where tg_id = '{user_tg_id}'));"""
        return self.run_request(request=request)

    # def check_permission(self, user_tg_id: str, perm_code: str) -> bool:
    #     request = f"SELECT permissions from {self.DATABASE_NAME}.user WHERE tg_id = '{user_tg_id}';"
    #     if self.get_info(request=request)[0]["permissions"]

    ################

    # Update data

    ################

    def upd_place_info(self, place_id: int, element: str, new_value: str) -> bool:
        accessible_values = ["title", "description", "contact", "site"]
        if element in accessible_values:
            request = f"UPDATE {self.DATABASE_NAME}.place set {element} = '{new_value}' " \
                      f"WHERE id = {place_id}"
            return self.run_request(request=request)
        else:
            return False

    def update_place_rating(self, place_id: int):
        req_1 = f"SELECT AVG(rating) as average from {self.DATABASE_NAME}.review WHERE place_id = '{place_id}';"
        value = round(self.get_info(request=req_1)[0]["average"], 1)
        req_2 = f"UPDATE {self.DATABASE_NAME}.place SET rating = '{value}' WHERE id = '{place_id}';"
        return self.run_request(request=req_2)

    def upd_user_info(self, user_id: str, element: str, new_value: str) -> bool:
        accessible_values = ["name", "photo_id", "contact", "age", "interests", "prefer_place",
                             "description", "meet_enabled", "sex", "sex_find", "age_find"]
        if element in accessible_values:
            request = f"UPDATE {self.DATABASE_NAME}.user set {element} = '{new_value}' " \
                      f"WHERE tg_id = '{user_id}';"
            return self.run_request(request=request)
        else:
            return False

    def upd_user_interest_info(self, user_id: int, interest_id: int, action: bool = 1) -> bool:
        if action:
            request = f"INSERT INTO {self.DATABASE_NAME}.user_interest " \
                      f"(interest_id, user_id) values ('{interest_id}', '{user_id}');"
        else:
            request = f"DELETE FROM {self.DATABASE_NAME}.user_interest " \
                      f"WHERE user_id = '{user_id}' AND interest_id = '{interest_id}'"
        return self.run_request(request=request)

    ################

    # Delete data

    ################

    def del_menu(self, place_id: int, title: str) -> bool:
        request = f"DELETE FROM {self.DATABASE_NAME}.menu WHERE place_id = '{place_id}' AND " \
                  f"title = '{title}';"
        return self.run_request(request=request)

    ################

    # CHECK data

    ################

    def check_status_reg_pa(self, user_id: str) -> str:
        request = f"select if(status_reg = '1', 1, 0) as res from {self.DATABASE_NAME}.place_admin " \
                  f"where user_id = '{user_id}';"

        res = self.get_info(request=request)[0]["res"]
        return f"{res}"

    def check_pass_log_pa(self, user_pass: str, login: str, user_id: str) -> bool:
        request = f"select if(user_pass = '{user_pass}' and login = '{login}', 1, 0) as res " \
                  f"from {self.DATABASE_NAME}.place_admin where user_id = '{user_id}';"
        res = self.get_info(request=request)[0]["res"]
        return res

    def check_user_meet_enable(self, user_id: str) -> bool:
        request = f"select if(meet_enabled = '1', 1, 0) as res " \
                  f"from {self.DATABASE_NAME}.user " \
                  f"where tg_id = '{user_id}';"
        return self.get_info(request=request)[0]["res"]

    def check_meet_match(self, user_tg_id: str, purpose_user_id: int) -> bool:
        request = f"""select id as res from {self.DATABASE_NAME}.lovers 
                      where user_id = (select id from {self.DATABASE_NAME}.user where tg_id = '{user_tg_id}') 
                      and purpose_user_id = '{purpose_user_id}';
                   """
        return len(self.get_info(request=request)) > 0

    def check_meet_settings(self, tg_user_id: str) -> bool:
        request = f"""SELECT IF(sex IS NOT NULL AND sex_find IS NOT NULL, 1, 0) as res from {self.DATABASE_NAME}.user 
                      WHERE tg_id = '{tg_user_id}';"""
        return self.get_info(request=request)[0]["res"]
