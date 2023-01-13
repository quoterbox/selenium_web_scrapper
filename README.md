# Get data from any website with Selenium

## Description of the crawler

1. This is a simple Python class to get startups from any website without API.
2. GPRScrapper makes use Selenium library for Python and chromedriver as well(or any other for your web browser).
3. GPRScrapper allows you to receive data in the desired language.
4. It's easy to use in any browser with XPATH copy and paste.

## Setup

### How to start python script in shell

1. Install python 3.7+ https://www.python.org/downloads/windows/ (or version for you OS)
2. Install pipenv `pip install --user pipenv`. Docs are here: https://github.com/pypa/pipenv
3. To install all packages run this command: `pipenv install`
4. To start python script: `pipenv run py main.py` (for windows)
5. Download Chromedriver for yor own Google Chrome version (or your own, Gecko driver for Firefox etc.), from this page:
https://chromedriver.chromium.org and put it next to the `main.py` file.
