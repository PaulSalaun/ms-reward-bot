import pdb
import time
from typing import Tuple

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.connexion import page_cookies
from requests.errors import error_manager
from utils import time_wait

POINTS = "#balanceToolTipDiv > p > mee-rewards-counter-animation > span"
STREAK = "#streakToolTipDiv > p > mee-rewards-counter-animation > span"
LINK = 'https://rewards.microsoft.com/dashboard'


def get_points(driver: WebDriver) -> tuple[str, str]:
    wait = WebDriverWait(driver, 10)
    driver.get(LINK)
    # Look for web error
    error_manager.error_pipe(driver)
    # Cookies pop-up closed
    page_cookies.quit_page_cookies(driver)

    time_wait.page_load(driver)
    time.sleep(2)

    rewards_nb = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, POINTS))).text
    streaks_nb = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, STREAK))).text
    return rewards_nb, streaks_nb
