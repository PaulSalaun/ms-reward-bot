import json
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def connect(driver, email, password):
    wait = WebDriverWait(driver, 10)

    element = driver.find_element(By.ID, 'sb_form_q')
    element.send_keys('WebDriver')
    element.submit()

    time.sleep(1)
    connect_button = wait.until(EC.visibility_of_element_located((By.ID, 'id_a')))
    connect_button.click()

    email_input = wait.until(EC.visibility_of_element_located((By.ID, 'i0116')))
    email_input.send_keys(email)
    next_button = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
    next_button.click()

    pass_input = wait.until(EC.visibility_of_element_located((By.ID, 'i0118')))
    pass_input.send_keys(password)
    end_button = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
    end_button.click()
    time.sleep(10)
