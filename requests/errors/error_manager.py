import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

ERROR_CONNECT = "body > div.simpleSignIn > div.signInOptions > span > a"


def reconnect_session(driver: WebDriver):
    time.sleep(0.5)
    try:
        driver.find_element(By.CSS_SELECTOR, ERROR_CONNECT).click()
        print('[DISCONNECT]', 'Reconnection done')
        time.sleep(1)
    except:
        pass
