import re
import time
import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

from scrapper.scrapper_saver import ScrapperSaver


class Scrapper:
    driver = False
    saver = False
    __main_xpath = ""
    __website = ""
    __webdata_items = []
    __start_list_page_data = []

    # 0 - maximum
    __maximum_count_items = 10

    login_data = {
        "login": "",
        "password": "",
    }
    xpath_options = {}
    regexp_xpath_options = {}
    time_options = {
        "delay_before_open_modal": [5, 10],
        "delay_before_close": [5, 10],
        "delay_between_review": [1, 3],
        "wait_login_form": 120,
        "wait_item_body": 120
    }
    scroll_options = {
        "scroll_origin_x_offset": [0, 0],
        "scroll_origin_y_offset": [0, 0],
        "scroll_delta_x": [0, 0],
        "scroll_delta_y": [0, 0],
    }

    def __init__(self, driver: webdriver, options: {}, *args):
        self.driver = driver
        if args:
            self.saver = args[0]
        self.actions = ActionChains(self.driver)
        self.__website = options["website"]
        if "login_data" in options:
            self.__set_login_data(options["login_data"])
        self.__set_maximum_count_items(options["maximum_count_items"])
        self.__set_xpath_options(options["xpath_options"])
        self.__set_time_options(options["time_options"])
        self.__set_scroll_options(options["scroll_options"])

        self.__main_xpath = self.__find_main_xpath(
            options["xpath_options"]["list_page"]["first_item"]["item_body"]["XPATH"],
            options["xpath_options"]["list_page"]["second_item"]["item_body"]["XPATH"]
        )

        self.__set_regexp_xpath_options(self.__main_xpath, options["xpath_options"]["list_page"]["first_item"])

    def get_webdata_items(self) -> []:
        return self.__webdata_items

    def load_list_page_data(self, start_list_page_data: []):
        self.__start_list_page_data = start_list_page_data

    def run(self, app_links: []):

        start_time = datetime.datetime.now()

        for app_link in app_links:
            print("-- Scraping has been started from: %s --" % app_link)
            self.__webdata_items += self.__get_data_from_app(app_link)
            print("-- Scraping has been finished from: %s --" % app_link)

        self.__sleep(*self.time_options["delay_before_close"])
        self.driver.close()

        self.__count_time(start_time, datetime.datetime.now())

    def __set_regexp_xpath_options(self, main_xpath: str, first_item: {}):
        for key, value in first_item.items():
            if key == "list_fields":
                for list_fields_key, list_fields_value in value.items():
                    self.__replace_xpath(main_xpath, list_fields_key, list_fields_value)
            else:
                self.__replace_xpath(main_xpath, key, value)

    def __replace_xpath(self, main_xpath: str, field_key: {}, field_value: {}):
        self.regexp_xpath_options[field_key] = {}
        self.regexp_xpath_options[field_key]["XPATH"] = field_value["XPATH"].replace(main_xpath, "%s")
        self.regexp_xpath_options[field_key]["XPATH"] = re.sub(
            r'(%s)(\[\d+])(.*)', r'\1[%d]\3',
            self.regexp_xpath_options[field_key]["XPATH"]
        )

    def __set_maximum_count_items(self, maximum_count_items: int):
        self.__maximum_count_items = maximum_count_items

    def __set_login_data(self, login_data: {}):
        self.login_data = login_data

    def __set_xpath_options(self, xpath_options: {}):
        self.xpath_options = xpath_options

    def __set_time_options(self, time_options: {}):
        self.time_options = time_options

    def __set_scroll_options(self, scroll_options: {}):
        self.scroll_options = scroll_options

    def __get_data_from_app(self, website_link: str) -> []:

        # Step 1
        self.driver.get(website_link)

        # Step 2
        if self.login_data:
            self.__login(self.login_data)

        # The first loading for accept cookies
        self.__find_webdata_field(1, "item_body")

        # Step 3 - List
        if not self.__start_list_page_data:
            webdata_short_items = self.__find_short_items(website_link)
        else:
            webdata_short_items = self.__start_list_page_data

        # Step 4 - Details
        webdata_items = self.__find_detail_items(webdata_short_items)

        return webdata_items

    def __find_short_items(self, website_link: str, *args) -> []:
        webdata_short_items = []

        webdata_item_num = 1
        while True:
            webdata_short_item = self.__get_webdata_item_from_app(webdata_item_num)
            webdata_short_items.append(webdata_short_item)

            if self.saver:
                self.saver.save_list_page_row(webdata_short_item)

            if self.__maximum_count_items != 0 and self.__maximum_count_items <= webdata_item_num:
                break

            page_elements_count = len(self.driver.find_elements(By.CSS_SELECTOR, self.xpath_options["load_page"]["items_class"]))
            if page_elements_count <= webdata_item_num:
                self.__sleep(*self.time_options["delay_before_open_next_page"])
                self.__load_more_items(self.xpath_options["load_page"]["next_page_link_xpath"])

            webdata_item_num = webdata_item_num + 1
            self.__sleep(*self.time_options["delay_between_item"])

        return webdata_short_items

    def __find_detail_items(self, webdata_short_items: [], *args) -> []:
        webdata_detail_items = []
        webdata_item_num = 1

        for webdata_item in webdata_short_items:
            if "detail_link" in webdata_item:
                self.driver.get(webdata_item["detail_link"])
                self.__waiting_anytype_selector(
                    self.xpath_options["detail_page"]["detail_page_waiting_tag"],
                    self.time_options["wait_detail_page"]
                )
                webdata_item_with_details = self.__get_webdata_item_details(webdata_item)
                webdata_detail_items.append(webdata_item_with_details)

                if self.saver:
                    self.saver.save_detail_page_row(webdata_item_with_details)
            else:
                print("-- `detail_link` is required for scrapping detail data. "
                      "`detail_link` field has not been found for item num - %d" % webdata_item_num)
                webdata_detail_items.append(webdata_item)

                if self.saver:
                    self.saver.save_detail_page_row(webdata_item)

            if self.__maximum_count_items != 0 and self.__maximum_count_items <= webdata_item_num:
                break

            webdata_item_num = webdata_item_num + 1
            self.__sleep(*self.time_options["delay_between_item"])

        return webdata_detail_items

    def __login(self, login_data: {}):
        print("Login to service")

        login_field = self.__waiting_anytype_selector(self.xpath_options["auth"]["login_xpath"], self.time_options["wait_login_form"])
        pass_field = self.__waiting_anytype_selector(self.xpath_options["auth"]["password_xpath"], self.time_options["wait_login_form"])
        login_button = self.__waiting_anytype_selector(self.xpath_options["auth"]["login_button_xpath"], self.time_options["wait_login_form"])

        self.actions.move_to_element(login_field).perform()
        login_field.send_keys(login_data["login"])
        self.__sleep(2, 5)
        self.actions.move_to_element(pass_field).perform()
        pass_field.send_keys(login_data["password"])
        self.__sleep(2, 5)
        self.actions.move_to_element(login_button).perform()
        self.actions.click(login_button).perform()

    def __get_webdata_item_from_app(self, webdata_item_num: int) -> {}:
        print("Webdata item num - %d" % webdata_item_num)

        webdata_item = {}

        for field_name, value in self.regexp_xpath_options.items():
            field = self.__find_webdata_field(webdata_item_num, field_name)

            if field:
                if field_name == "item_body":
                    self.__scroll_to_webdata_item(field)
                elif field_name == "detail_link":
                    webdata_item[field_name] = self.__format_uri(field.get_attribute("href"))
                else:
                    webdata_item[field_name] = self.__clear_string(field.text)
            else:
                webdata_item[field_name] = "None"

        return webdata_item

    def __find_webdata_field(self, webdata_item_num: int, field_name: str) -> WebElement:
        try:
            main_xpath_test = self.__main_xpath
            field_selector = self.regexp_xpath_options[field_name]
            field_to_find = {"XPATH": field_selector["XPATH"] % (main_xpath_test, webdata_item_num)}

            if field_name == "item_body":
                field = self.__waiting_anytype_selector(field_to_find, self.time_options["wait_item_body"])
            else:
                field = self.__waiting_anytype_selector(field_to_find, 1)

            if field_name != "item_body" and field:
                print("field_name - %s" % field_name)
                print("%s: %s" % (field_name, field.text))
            return field
        except NoSuchElementException:
            print("%s for the webdata_item num - %d - has not been found!" % (field_name, webdata_item_num))
            pass

    def __get_webdata_item_details(self, webdata_item: {}) -> {}:
        for field_name, value in self.xpath_options["detail_page"]["detail_fields"].items():

            field = self.__find_webdata_detail_field(field_name)

            if field:
                webdata_item[field_name] = self.__clear_string(field.text)
                self.__scroll_to_webdata_item(field)
            else:
                webdata_item[field_name] = "None"

        return webdata_item

    def __find_webdata_detail_field(self, field_name: str) -> WebElement:
        waiting_time = 1
        element = self.__waiting_anytype_selector(self.xpath_options["detail_page"]["detail_fields"][field_name], waiting_time)
        return element

    def __load_more_items(self, load_button_xpath: str):
        try:
            load_button = self.driver.find_element(By.XPATH, load_button_xpath)
            self.actions.move_to_element(load_button).perform()
            self.actions.click(load_button).perform()
        except NoSuchElementException:
            print("%s has not been found!" % load_button_xpath)
            pass

    def __scroll_to_webdata_item(self, webdata_item: WebElement):
        scroll_to_webdata_item = ScrollOrigin(
            webdata_item,
            random.randint(*self.scroll_options["scroll_origin_x_offset"]),
            random.randint(*self.scroll_options["scroll_origin_y_offset"])
        )
        self.actions.scroll_from_origin(
            scroll_to_webdata_item,
            random.randint(*self.scroll_options["scroll_delta_x"]),
            random.randint(*self.scroll_options["scroll_delta_y"])
        ).move_to_element(webdata_item).perform()

    def __waiting_anytype_selector(self, selector: {}, wait_time: int) -> WebElement:
        print("Waiting for selector or XPATH has been started")

        if "XPATH" in selector:
            print("-- Waiting for XPATH %s --" % (selector["XPATH"]))
            try:
                element = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, selector["XPATH"])))
                print("Waiting has been finished for XPATH %s" % selector["XPATH"])
                return element
            except TimeoutException:
                print("Waiting ERROR for XPATH %s" % selector["XPATH"])
                pass

        if "CSS" in selector:
            print("-- Waiting for CSS selector %s --" % selector["CSS"])
            try:
                element = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector["CSS"])))
                print("Waiting has been finished for CSS selector %s" % selector["CSS"])
                return element
            except TimeoutException:
                print("Waiting ERROR for CSS selector %s" % selector["CSS"])
                pass

    def __format_uri(self, uri: str) -> str:
        if not re.findall("http(s)?://", uri):
            uri = self.__website + uri
        return uri

    @staticmethod
    def __count_time(start_time, end_time):
        delta_time = end_time - start_time
        dt_days = delta_time.days
        dt_hours, mod_sec = divmod(delta_time.seconds, 3600)
        dt_minutes, dt_seconds = divmod(mod_sec, 60)
        print("Time of execution: %s days %sh %sm %ss" % (dt_days, dt_hours, dt_minutes, dt_seconds))

    @staticmethod
    def __find_main_xpath(first_xpath: str, second_xpath: str) -> str:
        if len(first_xpath) != len(second_xpath):
            raise ValueError('XPATH for first and second items has different length! They must be the same length.')

        position = 0
        for key, letter in enumerate(first_xpath):
            if letter != second_xpath[key]:
                position = key
                break

        if not position:
            raise ValueError('Have no a difference between first and second items xpath! '
                             'They must have a different digits for some tag like "/html/div[1]" and "/html/div[2]".')

        return first_xpath[:position - 1]

    @staticmethod
    def __sleep(min_time: int, max_time: int):
        time.sleep(random.randint(min_time, max_time))

    @staticmethod
    def __clear_string(string: str) -> str:
        special_characters = [";", "\t", "\n", "\r", "\n\r", "<", ">"]
        return ''.join(filter(lambda i: i not in special_characters, string)).strip()
