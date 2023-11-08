import pdb
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from daily_requests.connexion import page_cookies
from daily_requests.errors import error_manager
from utils import time_wait

REWARD_URL = "https://rewards.bing.com/"
IMG_NOT_VAL = "#quizWelcomeContainer > span.rqWcHeader > span > div > img"

VALIDATED = '/div/card-content/mee-rewards-daily-set-item-content/div/a/mee-rewards-points/div/div/span[1]'
TASK_DONE = 'mee-icon mee-icon-SkypeCircleCheck'
TASK_NOT_DONE = 'mee-icon mee-icon-AddMedium'


def quiz(driver: WebDriver, xpath: str, style: int):
    wait = WebDriverWait(driver, 10)

    try:
        clicker = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        clicker.click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])

        # Disconnect error
        error_manager.reconnect_session(driver)

        # Cookies pop-up closed
        page_cookies.quit_page_cookies(driver)
        # *** TASK ***

        task_quiz(driver, style)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.get(REWARD_URL)
        time_wait.page_load(driver)

        validation_task = driver.find_element(By.XPATH, xpath + VALIDATED)
        if validation_task.get_attribute("class") == TASK_DONE:
            print('[QUIZ]', 'Done')
        elif validation_task.get_attribute("class") == TASK_NOT_DONE:
            print('[QUIZ]', 'Not Validated')
            task_quiz(driver, style)
        else:
            print('[QUIZ]', 'ERROR')

    except Exception as e:
        print("The error is in QUIZ: ", e)
        pass


def task_quiz(driver: WebDriver, style: int):
    wait = WebDriverWait(driver, 10)
    error_manager.reconnect_session(driver)
    page_cookies.quit_page_cookies(driver)

    time_wait.page_load(driver)
    try:
        driver.find_element(By.ID, "quizCompleteContainer")
    except:
        run_quiz = wait.until(EC.visibility_of_element_located((By.ID, "rqStartQuiz")))
        run_quiz.click()

        while True:
            time_wait.page_load(driver)
            time.sleep(1)
            try:
                driver.find_element(By.ID, "quizCompleteContainer")
                break
            except:
                if style == 1:
                    click_case_correct_option(driver)
                else:
                    click_case(driver)


def click_case_correct_option(driver: WebDriver):
    button_index = 0
    winnable = 0
    wait = WebDriverWait(driver, 5)
    while True:
        time_wait.page_load(driver)
        button = wait.until(EC.visibility_of_element_located((By.ID, "rqAnswerOption" + str(button_index))))
        try:
            if winnable == 5:
                break
            elif button.get_attribute("iscorrectoption") == "True":
                print('[QUIZ]', 'Good')
                button.click()
                winnable += 1
            else:
                print('[QUIZ]', 'Not')
                pass

            time.sleep(1)
            button_index += 1
        except:
            print('[QUIZ]', 'ERROR')
            break


def click_case(driver: WebDriver):
    button_index = 0
    wait = WebDriverWait(driver, 5)
    while True:
        time_wait.page_load(driver)
        button = wait.until(EC.visibility_of_element_located((By.ID, "rqAnswerOption" + str(button_index))))
        try:
            button.click()
            time.sleep(1)
            button_index += 1
        except:
            print('[QUIZ]', 'ERROR')
            break
