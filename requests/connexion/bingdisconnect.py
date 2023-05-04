import pdb
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.connexion import page_cookies

LINK = "https://rewards.microsoft.com/dashboard"


def disconnect(driver: WebDriver):
    wait = WebDriverWait(driver, 10)
    driver.get(LINK)
    time.sleep(1)

    page_cookies.header_cookies(driver)
    # Close Reward banner
    page_cookies.quit_reward_banner(driver)

    try:
        account_button = driver.find_element(By.ID, 'img_sec')
        account_button.click()

    except:
        account_button = driver.find_element(By.ID, 'img_sec_default')
        account_button.click()

    deco_button = wait.until(EC.visibility_of_element_located((By.ID, 'mectrl_body_signOut')))
    deco_button.click()
    time.sleep(2)
