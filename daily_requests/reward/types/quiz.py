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


def quiz(driver: WebDriver, xpath: str):
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
        task_quiz(driver)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.get(REWARD_URL)
        time_wait.page_load(driver)

        validation_task = driver.find_element(By.XPATH, xpath + VALIDATED)
        if validation_task.get_attribute("class") == TASK_DONE:
            print('[QUIZ]', 'Done')
        elif validation_task.get_attribute("class") == TASK_NOT_DONE:
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
            time.sleep(1)
            try:
                driver.find_element(By.ID, "quizCompleteContainer")
                break
            except:
                click_case(driver)
                time_wait.page_load(driver)


def click_case(driver: WebDriver):
    button_index = 0
    winnable = 0
    wait = WebDriverWait(driver, 5)
    while True:
        time_wait.page_load(driver)
        button = wait.until(EC.visibility_of_element_located((By.ID, "rqAnswerOption" + str(button_index))))
        try:
            if button.get_attribute("iscorrectoption") == "True":
                button.click()
                winnable += 1
            else:
                button.click()

            button_index += 1
            if winnable == 5:
                break
        except:
            break
