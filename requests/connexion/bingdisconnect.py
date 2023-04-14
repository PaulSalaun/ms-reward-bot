import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LINK = "https://www.bing.com/search?q=test&form=QBLH&sp=-1&lq=0&pq=test&sc=10-4&qs=n&sk=&cvid=0DBE77F2E2C44D9FAAE8BDCFDAC627ED&ghsh=0&ghacc=0&ghpl="


def disconnect(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(LINK)
    time.sleep(1)

    account_button = wait.until(EC.visibility_of_element_located((By.ID, 'id_l')))
    account_button.click()

    deco_button = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#id_d > div > div.id_signout > a > span')))
    deco_button.click()
    time.sleep(2)

    print("** WebDriver disconnected **")
