import pdb
from random import randint

from selenium.webdriver.chrome.webdriver import WebDriver

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.connexion import page_cookies
from requests.errors import error_manager
from utils import time_wait

ERROR_CONNECT = "body > div.simpleSignIn > div.signInOptions > span > a"
POINT_GAIN = "#btoHeadPanel > span.rqMenubar > span.rqText > span > span.rqEarnedPoints > span"


def ceci_cela(driver: WebDriver, path_css: str):
    wait = WebDriverWait(driver, 10)
    time.sleep(1)

    try:
        clicker = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, path_css)))
        clicker.click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)

        # Disconnect error
        error_manager.reconnect_session(driver)

        # Cookies pop-up closed
        page_cookies.quit_page_cookies(driver)

        # *** TASK ***
        task_cecicela(driver)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print("The error is: ", e)
        pass


def task_cecicela(driver: WebDriver):
    wait = WebDriverWait(driver, 10)
    time_wait.page_load(driver)
    error_manager.reconnect_session(driver)
    page_cookies.quit_page_cookies(driver)

    try:
        driver.find_element(By.ID, "quizCompleteContainer")
        print('[CECI-CELA]', '[DONE]', driver.find_element(By.CSS_SELECTOR, POINT_GAIN).text, '/ 50')

    except:
        run_quiz = wait.until(EC.visibility_of_element_located((By.ID, "rqStartQuiz")))
        run_quiz.click()
        i = 0
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, "quizCompleteContainer")))
                print('[CECI-CELA]', driver.find_element(By.CSS_SELECTOR, POINT_GAIN).text, '/ 50')
                break
            except:
                choix_ceci_cela = wait.until(EC.visibility_of_element_located((By.ID, define_choice())))
                choix_ceci_cela.click()
                time_wait.page_load(driver)
                i += 1
        print('[JEU]', 'Done')


def define_choice():
    chiffre = randint(1, 2)
    if chiffre == 1:
        print('[CECI-CELA]', 'Choix 1')
        return "rqAnswerOption0"
    else:
        print('[CECI-CELA]', 'Choix 2')
        return "rqAnswerOption1"
