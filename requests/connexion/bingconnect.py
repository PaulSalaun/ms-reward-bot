import json
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver


def connect(driver: WebDriver, email: str, password: str):
    wait = WebDriverWait(driver, 10)

    if driver.find_element(By.ID, "i0116"):
        email_input = wait.until(EC.visibility_of_element_located((By.ID, 'i0116')))
        email_input.send_keys(email)
        next_button = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
        next_button.click()

        pass_input = wait.until(EC.visibility_of_element_located((By.ID, 'i0118')))
        pass_input.send_keys(password)
        end_button = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
        end_button.click()

        stayco_button = wait.until(EC.visibility_of_element_located((By.ID, 'idBtn_Back')))
        stayco_button.click()
        time.sleep(3)
