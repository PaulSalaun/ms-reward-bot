import pdb
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.connexion import page_cookies
from requests.errors import error_manager

VALIDATION = "#btPollOverlay > span > div > img"


def sondage_task(driver: WebDriver, path_css: str):
    wait = WebDriverWait(driver, 10)
    time.sleep(1)
    try:
        clicker = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, path_css)))
        clicker.click()
        driver.switch_to.window(driver.window_handles[1])

        # Disconnect error
        error_manager.reconnect_session(driver)

        # Cookies pop-up closed
        page_cookies.quit_page_cookies(driver)

        image_validation = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, VALIDATION)))
        if image_validation.get_attribute("alt") == "Image d’une coche":
            print('[SONDAGE]', 'Done')

        else:
            choix_sondage = wait.until(EC.visibility_of_element_located((By.ID, "btoption1")))
            choix_sondage.click()
            time.sleep(5)
            print('[SONDAGE]', 'Done')

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print("The error is: ", e)
        pass
