import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def sondage_task(driver, path_css):
    wait = WebDriverWait(driver, 10)

    try:
        clicker = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, path_css)))
        clicker.click()
        time.sleep(3)

        driver.switch_to.window(driver.window_handles[1])

        choix_sondage = wait.until(EC.visibility_of_element_located((By.ID, "btoption1")))
        choix_sondage.click()
        time.sleep(5)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print("The error is: ", e)
        pass
