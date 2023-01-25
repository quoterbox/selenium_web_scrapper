import os
import csv
from dotenv import load_dotenv
from selenium import webdriver
from scrapper.scrapper import Scrapper

load_dotenv()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 OPR/89.0.4447.71")
#chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1600,900')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-setuid-sandbox')
chrome_options.add_argument('--disk-cache-size=0')

# Yes / No browser visualization
# chrome_options.headless = True

driver = webdriver.Chrome(options=chrome_options)
driver.delete_all_cookies()

webdata_scrapper = Scrapper(
    driver,
    {
        # for relative links
        "website": "https://app.acquire.com",
        # if you need to be logged in
        "login_data": {
            "login": os.getenv("LOGIN"),
            "password": os.getenv("PASSWORD"),
        },
        # 0 - maximum
        "maximum_count_items": 5,
        "xpath_options": {
            "auth": {
                "login_xpath": {"XPATH": "/html/body/div[1]/div/div/div[2]/div[1]/div/input"},
                "password_xpath": {"XPATH": "/html/body/div[1]/div/div/div[3]/div[1]/div/input"},
                "login_button_xpath": {"XPATH": "/html/body/div[1]/div/div/button[2]"},
            },
            "load_page": {
                # for counting items before click on "load more" button
                "items_class": ".projects-list .project-item",
                "next_page_link_xpath": {"XPATH": "/html/body/div[1]/div/div/div[3]/div[2]/div/button"},
            },
            "list_page": {
                "first_item": {
                    "item_body": {"XPATH": "/html/body/div[1]/div/div/div[3]/div[2]/div/div[1]"},
                    "list_fields": {
                        "item_name": {"XPATH": "/html/body/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/a/span"},
                        "location": {"XPATH": "/html/body/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div[1]/div[1]/div[1]/div[2]/span"},
                        "detail_link": {"XPATH": "/html/body/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div[2]/a"},
                    },
                },
                "second_item": {
                    "item_body": {"XPATH": "/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]"},
                },
            },
            "detail_page": {
                "detail_page_waiting_tag": {
                    "CSS": ".title.title-h2"
                },
                "detail_fields": {
                    "asking_price": {
                        "XPATH": "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/span",
                        "CSS": ".asking-price-wrap .asking-price-title",
                    },
                    "asking_price_reasoning": {
                        "XPATH": "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/div[3]/span[2]",
                        "CSS": ".price-reasoning-wrap .desc-2",
                    },
                    "date_founded": {
                        "XPATH": "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/div[4]/div[1]/div/span",
                        "CSS": ".project-info-list .text-wrap .small-data",
                    },
                    "desc_title": {
                        "XPATH": "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/div[5]/div[2]/span",
                        "CSS": ".base-info-wrap .headline-wrap .title-h3.listing-headline",
                    },
                    "description": {
                        "XPATH": "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/div[5]/div[3]/span",
                        "CSS": ".description-wrap .description.desc-2",
                    },
                    "business_model": {"XPATH": "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[1]/span[2]"},
                    "tech_stack": {"XPATH": "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[2]"},
                    "product_competitors": {"XPATH": "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/span"},
                    "growth_opportunity": {"XPATH": "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[4]/span[2]"},
                    "key_assets": {"XPATH": "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[5]/div"},
                    "reason_selling": {"XPATH": "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[1]/span[2]"},
                    "financing": {"XPATH": "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[2]/span[2]"},
                    "ttm_gross_revenue": {"XPATH": "/html/body/div[1]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div/div[2]"},
                    "ttm_net_profit": {"XPATH": "/html/body/div[1]/div[3]/div/div[3]/div[2]/div[2]/div[2]/div/div[2]"},
                    "last_months_gross_revenue": {"XPATH": "/html/body/div[1]/div[3]/div/div[3]/div[2]/div[2]/div[3]/div/div[2]"},
                    "last_months_net_profit": {"XPATH": "/html/body/div[1]/div[3]/div/div[3]/div[2]/div[2]/div[4]/div/div[2]"},
                    "customers": {"XPATH": "/html/body/div[1]/div[3]/div/div[4]/div[2]/div[2]/div[1]/div/div[2]"},
                    "annual_recurring_revenue": {"XPATH": "/html/body/div[1]/div[3]/div/div[4]/div[2]/div[2]/div[2]/div/div[2]"},
                    "annual_growth_rate": {"XPATH": "/html/body/div[1]/div[3]/div/div[4]/div[2]/div[2]/div[3]/div/div[2]"},
                }
            },
        },
        # time delays will be randomly selected between min and max value
        "time_options": {
            "delay_before_open_next_page": [1, 5],
            "delay_before_close": [5, 10],
            "delay_between_item": [1, 1],
            "wait_login_form": 120,
            "wait_item_body": 120,
            "wait_detail_page": 120,
        },
        # pixels offsets will be randomly selected between min and max value
        # read documentation for these options:
        # https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html?highlight=scroll_from_origin#selenium.webdriver.common.action_chains.ActionChains.scroll_from_origin
        "scroll_options": {
            "scroll_origin_x_offset": [0, 0],
            "scroll_origin_y_offset": [0, 0],
            "scroll_delta_x": [0, 0],
            "scroll_delta_y": [0, 0],
        }
    }
)

webdata_scrapper.run([
    # Just for example
    "https://app.acquire.com/marketplace",
])

webdata_items = webdata_scrapper.get_webdata_items()
fields = dict(zip(webdata_items[0].keys(), webdata_items[0].keys()))

output_file = "web_items.csv"
with open(output_file, "a", encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, delimiter=';', fieldnames=fields.keys())
    writer.writerow(fields)
with open(output_file, "a", encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, delimiter=';', fieldnames=fields.keys())
    for webdata_item in webdata_items:
        writer.writerow(webdata_item)

print("Records has been successfully saved to the file!")
