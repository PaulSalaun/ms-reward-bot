import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import time_wait

REWARD_URL = "https://rewards.bing.com/"
VALIDATED = '/div/card-content/mee-rewards-daily-set-item-content/div/a/mee-rewards-points/div/div/span[1]'
TASK_DONE = 'mee-icon mee-icon-SkypeCircleCheck'
TASK_NOT_DONE = 'mee-icon mee-icon-AddMedium'


def random_task(driver: WebDriver, xpath: str):
    wait = WebDriverWait(driver, 10)
    time.sleep(1)

    try:
        clicker = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        clicker.click()
        driver.switch_to.window(driver.window_handles[1])
        time_wait.page_load(driver)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.get(REWARD_URL)
        time_wait.page_load(driver)

        validation_task = driver.find_element(By.XPATH, xpath + VALIDATED)
        if validation_task.get_attribute("class") == TASK_DONE:
            print('[RANDOM]', 'Done')
        elif validation_task.get_attribute("class") == TASK_NOT_DONE:
            print('[RANDOM]', 'Not Validated')
            random_task(driver, xpath)
        else:
            print('[RANDOM]', 'ERROR')

    except Exception as e:
        print("[RANDOM]", "Error: ", e)
        pass
