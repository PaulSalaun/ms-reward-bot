import pdb
import time

from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.connexion import page_cookies

DECO_LINK = "https://rewards.bing.com/Signout"
CLEAR_DATA_LINK = "chrome://settings/clearBrowserData"


def disconnect(driver: WebDriver):
    wait = WebDriverWait(driver, 10)
    driver.get(DECO_LINK)
    time.sleep(1)
    try:
        driver.delete_all_cookies()
        time.sleep(1)
        # Clear browser datas
        driver.get(CLEAR_DATA_LINK)
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
        driver.send_keys(Keys.RETURN)
    except Exception as e:
        print('[ERROR]', 'Error in disconnection', e)
