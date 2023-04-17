import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def random_task(driver, path_css):
    wait = WebDriverWait(driver, 10)

    try:
        clicker = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, path_css)))
        clicker.click()

        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print('[JEU]', 'Done')

    except Exception as e:
        print("The error is: ", e)
        pass
