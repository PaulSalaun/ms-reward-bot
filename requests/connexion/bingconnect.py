import json
import time
import pdb

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver

from requests.errors import error_manager

LINK = "https://www.bing.com/"


def connect(driver: WebDriver, email: str, password: str, isMobile: bool):
    wait = WebDriverWait(driver, 10)

    if not isMobile:
        driver.get('https://rewards.microsoft.com/dashboard')
        time.sleep(1)

        # Look for web error
        error_manager.error_pipe(driver)

        if driver.find_element(By.ID, "i0116"):
            try:
                email_input = wait.until(EC.visibility_of_element_located((By.ID, 'i0116')))
                email_input.send_keys(email)
                next_button = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
                next_button.click()

                pass_input = wait.until(EC.visibility_of_element_located((By.ID, 'i0118')))
                pass_input.send_keys(password)
                end_button = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
                end_button.click()
                time.sleep(0.33)

                if driver.find_element(By.ID, 'idBtn_Back'):
                    stayco_button = wait.until(EC.visibility_of_element_located((By.ID, 'idBtn_Back')))
                    stayco_button.click()
                time.sleep(1)

            except NoSuchElementException:
                pdb.set_trace()

            # Look for web error
            error_manager.error_pipe(driver)

    else:
        driver.get(LINK)
        time.sleep(1)
        burger_button = wait.until(EC.visibility_of_element_located((By.ID, 'mHamburger')))
        burger_button.click()

        connect_button = wait.until(EC.visibility_of_element_located((By.ID, 'hb_s')))
        connect_button.click()
        time.sleep(1)

        if driver.find_element(By.ID, "i0116"):
            email_input = wait.until(EC.visibility_of_element_located((By.ID, 'i0116')))
            email_input.send_keys(email)
            next_button = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
            next_button.click()

            pass_input = wait.until(EC.visibility_of_element_located((By.ID, 'i0118')))
            pass_input.send_keys(password)
            end_button = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
            end_button.click()
            time.sleep(0.33)
