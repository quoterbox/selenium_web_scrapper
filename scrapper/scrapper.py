import csv
import re
import time
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


class Scrapper:
    __main_xpath = ""
    __is_write_realtime = False
    __website = ""
    __items_class = ""
    __webdata_items = []
    __input_file_short_data = []

    # 0 - maximum
    __count_items = 10

    output_file_short = {}
    output_file_detail = {}

    login_data = {
        "login": "",
        "password": "",
    }
    xpath_options = {
        "login_xpath": "",
        "password_xpath": "",
        "login_button_xpath": "",
        "next_page_link_xpath": "",
        "first_item": {
            "item_body": "",
            "item_name": "",
            "location": "",
            "detail_link": "",
        },
        "detail_fields": {
            "asking_price": "",
            "asking_price_reasoning": "",
            "date_founded": "",
            "desc_title": "",
            "description": "",
            "business_model": "",
            "tech_stack": "",
            "product_competitors": "",
            "growth_opportunity": "",
            "key_assets": "",
            "reason_selling": "",
            "financing": "",
            "ttm_gross_revenue": "",
            "ttm_net_profit": "",
            "last_months_gross_revenue": "",
            "last_months_net_profit": "",
            "Customers": "",
            "annual_recurring_revenue": "",
            "annual_growth_rate": "",
        },
        "second_item": {
            "item_body": "",
        },
    }
    regexp_xpath_options = {
        "item_body": "",
        "item_name": "",
        "location": "",
        "detail_link": "",
    }
    time_options = {
        "delay_before_open_modal": [5, 10],
        "delay_before_close": [5, 10],
        "delay_between_review": [1, 3]
    }
    scroll_options = {
        "scroll_origin_x_offset": [0, 50],
        "scroll_origin_y_offset": [0, 50],
        "scroll_delta_x": [0, 50],
        "scroll_delta_y": [0, 50],
    }

    def __init__(self, driver: webdriver, options: {}):
        self.driver = driver
        self.actions = ActionChains(self.driver)
        self.__website = options["website"]
        self.__items_class = options["items_class"]
        self.__set_write_realtime(options["write_in_file_realtime"]["write"])
        self.__set_output_files(options["write_in_file_realtime"]["output_files"])
        self.__set_input_file(options["input_file_short_data"])
        self.__set_login_data(options["login_data"])
        self.__set_count_items(options["count_items"])
        self.__set_xpath_options(options["xpath_options"])
        self.__set_time_options(options["time_options"])
        self.__set_scroll_options(options["scroll_options"])

        self.__main_xpath = self.__find_main_xpath(
            options["xpath_options"]["first_item"]["item_body"],
            options["xpath_options"]["second_item"]["item_body"]
        )

        self.__set_regexp_xpath_options(self.__main_xpath, options["xpath_options"]["first_item"])

    def __set_regexp_xpath_options(self, main_xpath: str, first_item: {}):
        for key, value in first_item.items():
            self.regexp_xpath_options[key] = value.replace(main_xpath, "%s")
            self.regexp_xpath_options[key] = re.sub(r'(%s)(\[\d+])(.*)', r'\1[%d]\3', self.regexp_xpath_options[key])

    def __set_count_items(self, count_items: int):
        self.__count_items = count_items

    def __set_write_realtime(self, is_write_realtime: bool):
        self.__is_write_realtime = is_write_realtime

    def __set_output_files(self, output_files: {}):
        self.output_file_short = output_files["output_file_short"]
        self.output_file_detail = output_files["output_file_detail"]

    def __set_input_file(self, webdata_short_items: []):
        self.__input_file_short_data = webdata_short_items

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
        self.__login(self.login_data)

        # The first loading for accept cookies
        self.__find_webdata_field(1, "item_body")

        # Step 3
        if self.__is_write_realtime:

            # List
            if not self.__input_file_short_data:
                self.__create_file(self.output_file_short)

                with open(self.output_file_short["name"], "a", encoding='utf-8', newline='') as file:
                    writer_short = csv.DictWriter(file, delimiter=';', fieldnames=self.output_file_short["fields"].keys())
                    webdata_short_items = self.__find_short_items(website_link, writer_short)

                self.__create_file(self.output_file_detail)
            else:
                webdata_short_items = self.__input_file_short_data

            # Details
            with open(self.output_file_detail["name"], "a", encoding='utf-8', newline='') as file:
                writer_detail = csv.DictWriter(file, delimiter=';', fieldnames=self.output_file_detail["fields"].keys())
                webdata_items = self.__find_detail_items(webdata_short_items, writer_detail)
        else:
            # List
            if not self.__input_file_short_data:
                webdata_short_items = self.__find_short_items(website_link)
            else:
                webdata_short_items = self.__input_file_short_data

            # Details
            webdata_items = self.__find_detail_items(webdata_short_items)

        return webdata_items

    def __find_short_items(self, website_link: str, *args) -> []:
        webdata_short_items = []

        webdata_item_num = 1
        while True:
            webdata_short_item = self.__get_webdata_item_from_app(webdata_item_num)

            if self.__is_write_realtime:
                writer = args[0]
                writer.writerow(webdata_short_item)

            webdata_short_items.append(webdata_short_item)

            if self.__count_items != 0 and self.__count_items <= webdata_item_num:
                break

            page_elements_count = len(self.driver.find_elements(By.CSS_SELECTOR, self.__items_class))

            if page_elements_count <= webdata_item_num:
                self.__sleep(*self.time_options["delay_before_open_next_page"])
                self.__load_more_items(self.xpath_options["next_page_link_xpath"])

            webdata_item_num = webdata_item_num + 1
            self.__sleep(*self.time_options["delay_between_item"])

        return webdata_short_items

    def __find_detail_items(self, webdata_short_items: [], *args) -> []:
        webdata_detail_items = []
        webdata_item_num = 1

        for webdata_item in webdata_short_items:
            self.driver.get(webdata_item["detail_link"])
            webdata_item_with_details = self.__get_webdata_item_details(webdata_item)

            if self.__is_write_realtime:
                writer = args[0]
                writer.writerow(webdata_item_with_details)

            webdata_detail_items.append(webdata_item_with_details)

            if self.__count_items != 0 and self.__count_items <= webdata_item_num:
                break

            webdata_item_num = webdata_item_num + 1
            self.__sleep(*self.time_options["delay_between_item"])

        return webdata_detail_items

    def __login(self, login_data: {}):
        print("Login to service")

        self.__waiting_xpath(self.xpath_options["login_xpath"], 120)

        login_field = self.driver.find_element(By.XPATH, self.xpath_options["login_xpath"])
        pass_field = self.driver.find_element(By.XPATH, self.xpath_options["password_xpath"])
        login_button = self.driver.find_element(By.XPATH, self.xpath_options["login_button_xpath"])

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
                    webdata_item[field_name] = field.get_attribute("href")
                else:
                    webdata_item[field_name] = field.text
            else:
                webdata_item[field_name] = "None"

        return webdata_item

    def __find_webdata_field(self, webdata_item_num: int, field_name: str) -> WebElement:
        try:
            field_xpath = self.regexp_xpath_options[field_name] % (self.__main_xpath, webdata_item_num)

            if field_name == "item_body":
                self.__waiting_xpath(field_xpath, 120)
            else:
                self.__waiting_xpath(field_xpath, 1)

            field = self.driver.find_element(By.XPATH, field_xpath)

            if field_name != "item_body":
                print("%s: %s" % (field_name, field.text))
            return field
        except NoSuchElementException:
            print("%s for the webdata_item num - %d - has not been found!" % (field_name, webdata_item_num))
            pass

    def __get_webdata_item_details(self, webdata_item: {}) -> {}:

        for field_name, value in self.xpath_options["detail_fields"].items():

            field = self.__find_webdata_detail_field(field_name)

            if field:
                webdata_item[field_name] = field.text
            else:
                webdata_item[field_name] = "None"

        return webdata_item

    def __find_webdata_detail_field(self, field_name: str) -> WebElement:
        try:
            field_xpath = self.xpath_options["detail_fields"][field_name]
            self.__waiting_xpath(field_xpath, 5)
            field = self.driver.find_element(By.XPATH, field_xpath)

            print("%s: %s" % (field_name, field.text))

            return field
        except NoSuchElementException:
            print("%s has not been found!" % field_name)
            pass

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

    def get_webdata_items(self) -> []:
        return self.__webdata_items

    def run(self, app_links: []):
        for app_link in app_links:
            print("-- Start scrapping web items from: %s --" % app_link)
            self.__webdata_items += self.__get_data_from_app(app_link)

        self.__sleep(*self.time_options["delay_before_close"])
        self.driver.close()

    def __waiting_xpath(self, xpath: str, wait_time: int):
        print("Waiting has been started for loading page")
        print("-- waiting for XPATH %s --" % xpath)
        try:
            WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            print("Waiting ERROR for XPATH %s" % (xpath))
            pass
        print("Waiting has been finished for loading page")

    @staticmethod
    def __create_file(output_file: {}):
        with open(output_file["name"], "w", encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, delimiter=';', fieldnames=output_file["fields"].keys())
            writer.writerow(output_file["fields"])

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
    def clear_string(string: str) -> str:
        special_characters = [";", "\t", "\n", "\r", "\n\r", "<", ">"]
        return ''.join(filter(lambda i: i not in special_characters, string)).strip()
