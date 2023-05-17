import pdb
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.connexion import page_cookies
from requests.errors import error_manager
from utils import time_wait

REWARD_URL = "https://rewards.bing.com/"
VALIDATION = "#btPollOverlay > span > div > img"
VALIDATED = " > div > card-content > mee-rewards-daily-set-item-content > div > a > mee-rewards-points > div > div > " \
            "span.mee-icon.mee-icon-SkypeCircleCheck"
NOT_VALIDATED = " > div > card-content > mee-rewards-daily-set-item-content > div > a > mee-rewards-points > div > div " \
                "> span.mee-icon.mee-icon-AddMedium"


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
            pass

        else:
            choix_sondage = wait.until(EC.visibility_of_element_located((By.ID, "btoption1")))
            choix_sondage.click()
            time.sleep(5)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        driver.get(REWARD_URL)
        time_wait.page_load(driver)

        if driver.find_element(By.CSS_SELECTOR, path_css + VALIDATED):
            print('[SONDAGE]', 'Done')
        elif driver.find_element(By.CSS_SELECTOR, path_css + NOT_VALIDATED):
            print('[SONDAGE]', 'Not Validated')
            sondage_task(driver, path_css)
        else:
            print('[SONDAGE]', 'ERROR')

    except Exception as e:
        print("The error is: ", e)
        pass
