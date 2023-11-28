import json
import time
import pdb

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver

from daily_requests.errors import error_manager
from utils import time_wait

REWARD = "https://rewards.microsoft.com/dashboard"
LINK = "https://www.bing.com/"
CONNECT_LINK = "https://login.live.com/"


# 1: DAILY / 2: PC SEARCH / 3: MOBILE SEARCH
def connect(driver: WebDriver, email: str, password: str, momentum: int):
    wait = WebDriverWait(driver, 10)

    if momentum == 1:
        driver.get('https://rewards.microsoft.com/dashboard')
        time.sleep(1)

        # Look for web error
        error_manager.error_pipe(driver)

        try:
            print('[WEB]', email)
            email_connect(driver, email, password)

            if driver.find_element(By.ID, 'iLandingViewAction'):
                security = wait.until(EC.visibility_of_element_located((By.ID, 'iLandingViewAction')))
                security.click()
                print('[CONNECT]', 'Security popup')

            time_wait.page_load(driver)

            if driver.find_element(By.ID, 'idBtn_Back'):
                stayco_button = wait.until(EC.visibility_of_element_located((By.ID, 'idBtn_Back')))
                stayco_button.click()
                print('[CONNECT]', 'Stay connected popup')

            time_wait.page_load(driver)

        except NoSuchElementException:
            print('[STOP]', 'Error in connect')

        # Look for web error
        error_manager.error_pipe(driver)

    elif momentum == 2:
        driver.get(CONNECT_LINK)
        print('[PC]', email)
        try:
            email_connect(driver, email, password)

        except Exception as e:
            print('[ERROR]', 'At pc connect', e)

    elif momentum == 3:
        driver.get(LINK)
        print('[MOBILE]', email)
        time.sleep(1)
        burger_button = wait.until(EC.visibility_of_element_located((By.ID, 'mHamburger')))
        burger_button.click()

        connect_button = wait.until(EC.visibility_of_element_located((By.ID, 'hb_s')))
        connect_button.click()
        time.sleep(1)

        try:
            email_connect(driver, email, password)

        except Exception as e:
            print('[ERROR]', 'At mobile connect', e)

    else:
        raise ConnectionError("Type is not Daily/PC/MOBILE")


def email_connect(driver: WebDriver, email: str, password: str):
    wait = WebDriverWait(driver, 10)

    email_input = wait.until(EC.visibility_of_element_located((By.ID, 'i0116')))
    email_input.send_keys(email)
    next_button = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
    next_button.click()

    # pdb.set_trace()

    pass_input = wait.until(EC.visibility_of_element_located((By.ID, 'i0118')))
    pass_input.send_keys(password)
    end_button = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
    end_button.click()
    time.sleep(0.33)
