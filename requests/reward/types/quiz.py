import pdb
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.connexion import page_cookies
from requests.errors import error_manager
from utils import time_wait

REWARD_URL = "https://rewards.bing.com/"
IMG_NOT_VAL = "#quizWelcomeContainer > span.rqWcHeader > span > div > img"
VALIDATED = " > div > card-content > mee-rewards-daily-set-item-content > div > a > mee-rewards-points > div > div > " \
            "span.mee-icon.mee-icon-SkypeCircleCheck"
NOT_VALIDATED = " > div > card-content > mee-rewards-daily-set-item-content > div > a > mee-rewards-points > div > div " \
                "> span.mee-icon.mee-icon-AddMedium"


def quiz(driver: WebDriver, path_css: str):
    wait = WebDriverWait(driver, 10)

    try:
        clicker = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, path_css)))
        clicker.click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])

        # Disconnect error
        error_manager.reconnect_session(driver)

        # Cookies pop-up closed
        page_cookies.quit_page_cookies(driver)

        # *** TASK ***
        task_quiz(driver)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.get(REWARD_URL)
        time_wait.page_load(driver)

        if driver.find_element(By.CSS_SELECTOR, path_css + VALIDATED):
            print('[QUIZ]', 'Done')
        elif driver.find_element(By.CSS_SELECTOR, path_css + NOT_VALIDATED):
            print('[QUIZ]', 'Not Validated')
            task_quiz(driver)
        else:
            print('[QUIZ]', 'ERROR')

    except Exception as e:
        print("The error is in QUIZ: ", e)
        pass


def task_quiz(driver: WebDriver):
    wait = WebDriverWait(driver, 10)
    error_manager.reconnect_session(driver)
    page_cookies.quit_page_cookies(driver)

    try:
        driver.find_element(By.ID, "quizCompleteContainer")
    except:
        run_quiz = wait.until(EC.visibility_of_element_located((By.ID, "rqStartQuiz")))
        run_quiz.click()

        while True:
            try:
                driver.find_element(By.ID, "quizCompleteContainer")
                break
            except:
                click_case(driver)
                time_wait.page_load(driver)


def click_case(driver: WebDriver):
    button_index = 0
    while True:
        button_id = "rqAnswerOption" + str(button_index)
        try:
            # Loop if timeout during counting to retry
            if button_index == 10:
                button_index = 0
            else:
                button = driver.find_element(By.ID, button_id)
                button.click()
                button_index += 1
                time_wait.page_load(driver)
                time.sleep(0.5)
        except:
            break
