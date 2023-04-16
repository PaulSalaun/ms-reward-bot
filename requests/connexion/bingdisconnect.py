import pdb
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.connexion import page_cookies

LINK = "https://rewards.microsoft.com/dashboard"


def disconnect(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(LINK)
    time.sleep(1)

    page_cookies.header_cookies(driver)

    pdb.set_trace()

    try:
        account_button = driver.find_element(By.ID, 'img_sec')
        account_button.click()
        print('[DISCONNECT]', 'custom PP')

    except:
        account_button = driver.find_element(By.ID, 'img_sec_default')
        account_button.click()
        print('[DISCONNECT]', 'default PP')

    deco_button = wait.until(EC.visibility_of_element_located((By.ID, 'mectrl_body_signOut')))
    deco_button.click()
    time.sleep(2)

    print("** WebDriver disconnected **")
