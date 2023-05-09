import pdb
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

COOKIES_ID = "bnp_btn_accept"
HEADER_COOKIES_ID = "wcpConsentBannerCtrl"
HEADER_COOKIES_BUTTON = "#wcpConsentBannerCtrl > div._2j0fmugLb1FgYz6KPuB91w > button:nth-child(1)"
REWARD_BANNER_ID = "mbing-banner"


def quit_page_cookies(driver: WebDriver):
    time.sleep(1)
    try:
        driver.find_element(By.ID, COOKIES_ID).click()
        print('[COOKIES]', 'Pop-up cookies closed')
    except:
        pass


def quit_reward_banner(driver: WebDriver):
    time.sleep(1)
    try:
        banner = driver.find_element(By.ID, REWARD_BANNER_ID)
        style_before = banner.get_attribute("style")
        if "display: none;" not in style_before:
            print('[COOKIES]', 'Reward banner present')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            style_before = banner.get_attribute("style")
            if "display: none;" in style_before:
                print('[COOKIES]', 'Reward banner closed')
            else:
                print('[ERROR COOKIES]', 'Banner always present')
                pdb.set_trace()
    except NoSuchElementException:
        pass


def header_cookies(driver: WebDriver):
    try:
        driver.find_element(By.CSS_SELECTOR, HEADER_COOKIES_BUTTON).click()
        print('[COOKIES]', 'Header cookies closed')
    except NoSuchElementException:
        pass
