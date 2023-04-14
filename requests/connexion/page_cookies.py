import time

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

COOKIES_ID = "bnp_btn_accept"


def quit_page_cookies(driver: WebDriver):
    time.sleep(1)
    if driver.find_element(By.ID, COOKIES_ID):
        driver.find_element(By.ID, COOKIES_ID).click()
    else:
        pass
