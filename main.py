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

output_file = {
    "name": "web_items.csv",
    "fields": {
        "item_name": "Startup Name",
        "location": "Location",
        "detail_link": "Detail link",
        "asking_price": "Asking price",
        "asking_price_reasoning": "Asking price reasoning",
        "date_founded": "Date founded",
        "desc_title": "Description title",
        "description": "Description",
        "business_model": "Business model and pricing",
        "tech_stack": "Tech stack this product is built on",
        "product_competitors": "Product competitors",
        "growth_opportunity": "Growth opportunity",
        "key_assets": "Key assets",
        "reason_selling": "Reason for selling",
        "financing": "Financing",
        "ttm_gross_revenue": "TTM gross revenue",
        "ttm_net_profit": "TTM net profit",
        "last_months_gross_revenue": "Last months gross revenue",
        "last_months_net_profit": "Last months net profit",
        "Customers": "Customers",
        "annual_recurring_revenue": "Annual recurring revenue",
        "annual_growth_rate": "Annual growth rate",
    }
}

output_file_short = output_file.copy()
output_file_detail = output_file.copy()
output_file_short["name"] = "web_items_short.csv"
output_file_detail["name"] = "web_items_detail.csv"

# Example of reading data
webdata_short_items = []
with open("all_startups.csv", encoding='utf-8', newline='') as csvfile:
    webdata_short_items_reader = csv.reader(csvfile, delimiter=';')
    for i, row in enumerate(webdata_short_items_reader):
        if i > 1500:
            webdata_short_items.append({
                "item_name": row[0],
                "location": row[1],
                "detail_link": row[2],
                "asking_price": row[3],
                "asking_price_reasoning": row[4],
                "date_founded": row[5],
                "desc_title": row[6],
                "description": row[7],
                "business_model": row[8],
                "tech_stack": row[9],
                "product_competitors": row[10],
                "growth_opportunity": row[11],
                "key_assets": row[12],
                "reason_selling": row[13],
                "financing": row[14],
                "ttm_gross_revenue": row[15],
                "ttm_net_profit": row[16],
                "last_months_gross_revenue": row[17],
                "last_months_net_profit": row[18],
                "Customers": row[19],
                "annual_recurring_revenue": row[20],
                "annual_growth_rate": row[21],
            })
# Example of reading data

acquire_startups_scrapper = Scrapper(
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
        "count_items": 3000,
        # for counting items before click on "load more" button
        "items_class": ".projects-list .project-item",
        # Easy to use: you should copy these xpaths from your browser (right click and select "Inspect element")
        # Advanced user: you can write your own XPATH/CSS for every element
        "xpath_options": {
            "login_xpath": {"XPATH": "/html/body/div[1]/div/div/div[2]/div[1]/div/input"},
            "password_xpath": {"XPATH": "/html/body/div[1]/div/div/div[3]/div[1]/div/input"},
            "login_button_xpath": {"XPATH": "/html/body/div[1]/div/div/button[2]"},
            "next_page_link_xpath": {"XPATH": "/html/body/div[1]/div/div/div[3]/div[2]/div/button"},
            "first_item": {
                "item_body": {"XPATH": "/html/body/div[1]/div/div/div[3]/div[2]/div/div[1]"},
                "item_name": {"XPATH": "/html/body/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/a/span"},
                "location": {"XPATH": "/html/body/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div[1]/div[1]/div[1]/div[2]/span"},
                "detail_link": {"XPATH": "/html/body/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div[2]/a"},
            },
            "second_item": {
                "item_body": {"XPATH": "/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]"},
            },
            "detail_page_title": {
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
                "Customers": {"XPATH": "/html/body/div[1]/div[3]/div/div[4]/div[2]/div[2]/div[1]/div/div[2]"},
                "annual_recurring_revenue": {"XPATH": "/html/body/div[1]/div[3]/div/div[4]/div[2]/div[2]/div[2]/div/div[2]"},
                "annual_growth_rate": {"XPATH": "/html/body/div[1]/div[3]/div/div[4]/div[2]/div[2]/div[3]/div/div[2]"},
            }
        },
        # time delays will be randomly selected between min and max value
        "time_options": {
            "delay_before_open_next_page": [1, 5],
            "delay_before_close": [5, 10],
            "delay_between_item": [1, 1]
        },
        # pixels offsets will be randomly selected between min and max value
        # read documentation for these options:
        # https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html?highlight=scroll_from_origin#selenium.webdriver.common.action_chains.ActionChains.scroll_from_origin
        "scroll_options": {
            "scroll_origin_x_offset": [0, 0],
            "scroll_origin_y_offset": [0, 0],
            "scroll_delta_x": [0, 0],
            "scroll_delta_y": [0, 0],
        },
        "write_in_file_realtime": {
            "write": True,
            "output_files": {
                "output_file_short": output_file_short,
                "output_file_detail": output_file_detail
            }
        },
        "input_file_short_data": webdata_short_items
    }
)

acquire_startups_scrapper.run([
    # Just for example
    "https://app.acquire.com/marketplace",
])

with open(output_file["name"], "w", encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, delimiter=';', fieldnames=output_file["fields"].keys())
    writer.writerow(output_file["fields"])

with open(output_file["name"], "a", encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, delimiter=';', fieldnames=output_file["fields"].keys())
    for webdata_item in acquire_startups_scrapper.get_webdata_items():
        writer.writerow(webdata_item)

print("Records has been successfully saved to the file!")
