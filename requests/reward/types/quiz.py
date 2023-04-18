import pdb
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.connexion import page_cookies
from requests.errors import error_manager

IMG_NOT_VAL = "#quizWelcomeContainer > span.rqWcHeader > span > div > img"


def quiz_task(driver, path_css):
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

        try:
            driver.find_element(By.ID, "quizCompleteContainer")
            print('[QUIZ]', '[DONE]')

        except:
            # Commencez à jouer
            run_quiz = wait.until(EC.visibility_of_element_located((By.ID, "rqStartQuiz")))
            run_quiz.click()

            while True:
                try:
                    driver.find_element(By.ID, "quizCompleteContainer")
                    break
                except:
                    click_case(driver)
                    time.sleep(2)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print('[JEU]', 'Done')

    except Exception as e:
        print("The error is: ", e)
        pass


def click_case(driver: WebDriver):
    button_index = 0
    button_id = "rqAnswerOption" + str(button_index)
    print(driver.find_element(By.ID, 'bt_corOpCnt').text)
    while True:
        try:
            button = driver.find_element(By.ID, button_id)
            button.click()
            button_index += 1
            button_id = "rqAnswerOption" + str(button_index)
            time.sleep(1)
        except:
            break
