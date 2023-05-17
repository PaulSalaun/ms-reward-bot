import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import time_wait

REWARD_URL = "https://rewards.bing.com/"
VALIDATED = " > div > card-content > mee-rewards-daily-set-item-content > div > a > mee-rewards-points > div > div > " \
            "span.mee-icon.mee-icon-SkypeCircleCheck"
NOT_VALIDATED = " > div > card-content > mee-rewards-daily-set-item-content > div > a > mee-rewards-points > div > div " \
                "> span.mee-icon.mee-icon-AddMedium"


def random_task(driver: WebDriver, path_css: str):
    wait = WebDriverWait(driver, 10)
    time.sleep(1)

    try:
        clicker = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, path_css)))
        clicker.click()
        driver.switch_to.window(driver.window_handles[1])
        time_wait.page_load(driver)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.get(REWARD_URL)
        time_wait.page_load(driver)

        if driver.find_element(By.CSS_SELECTOR, path_css + VALIDATED):
            print('[RANDOM]', 'Done')
        elif driver.find_element(By.CSS_SELECTOR, path_css + NOT_VALIDATED):
            print('[RANDOM]', 'Not Validated')
            random_task(driver, path_css)
        else:
            print('[RANDOM]', 'ERROR')

    except Exception as e:
        print("The error is: ", e)
        pass
