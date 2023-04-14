import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_points(driver):
    reward_nb = (driver.find_element(By.ID, "id_rc")).text
    print(reward_nb)
    return reward_nb


