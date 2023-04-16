import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

POINTS = "#balanceToolTipDiv > p > mee-rewards-counter-animation > span"
DAY = "#dailypointToolTipDiv > p > mee-rewards-counter-animation > span"
STREAK = "#streakToolTipDiv > p > mee-rewards-counter-animation > span"


def get_points(driver):
    driver.get('https://rewards.microsoft.com/dashboard')
    time.sleep(1)

    reward_nb = (driver.find_element(By.CSS_SELECTOR, POINTS)).text
    day_nb = (driver.find_element(By.CSS_SELECTOR, DAY)).text
    streak_nb = (driver.find_element(By.CSS_SELECTOR, STREAK)).text
    print(reward_nb, day_nb, streak_nb)
    return reward_nb
