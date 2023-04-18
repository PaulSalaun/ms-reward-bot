import time

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

ERROR_CONNECT = "body > div.simpleSignIn > div.signInOptions > span > a"
ERROR_502_ID = "error-information-popup-content"


def reconnect_session(driver: WebDriver):
    time.sleep(0.5)
    try:
        driver.find_element(By.CSS_SELECTOR, ERROR_CONNECT).click()
        print('[DISCONNECT]', 'Reconnection done')
        time.sleep(1)
    except:
        pass


def error_pipe(driver: WebDriver):
    error_502(driver)


def error_502(driver: WebDriver):
    try:
        while True:
            if driver.find_element(By.ID, ERROR_502_ID).is_displayed():
                time.sleep(10)
                driver.refresh()
            else:
                print('[ERROR 502]', 'Done')
    except :
        pass
