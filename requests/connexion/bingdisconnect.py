import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def disconnect(driver):
    wait = WebDriverWait(driver, 10)
    driver.get('https://bing.com')

    element = driver.find_element(By.ID, 'sb_form_q')
    element.send_keys('WebDriver')
    element.submit()
    time.sleep(1)

    account_button = wait.until(EC.visibility_of_element_located((By.ID, 'id_l')))
    account_button.click()

    deco_button = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#id_d > div > div.id_signout > a > span')))
    deco_button.click()
    time.sleep(2)

    print("** WebDriver disconnected **")
