import pdb
import time
from typing import Tuple

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.connexion import page_cookies

POINTS = "#balanceToolTipDiv > p > mee-rewards-counter-animation > span"
STREAK = "#streakToolTipDiv > p > mee-rewards-counter-animation > span"
LINK = "https://www.bing.com/"


def get_points(driver: WebDriver) -> tuple[str, str]:
    wait = WebDriverWait(driver, 10)
    driver.get(LINK)
    time.sleep(1)

    # Cookies pop-up closed
    page_cookies.quit_page_cookies(driver)

    burger_button = wait.until(EC.visibility_of_element_located((By.ID, 'mHamburger')))
    burger_button.click()

    connect_button = wait.until(EC.visibility_of_element_located((By.ID, 'fly_id_rwds_b')))
    connect_button.click()

    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)

    rewards_nb = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, POINTS))).text
    streaks_nb = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, STREAK))).text
    return rewards_nb, streaks_nb
