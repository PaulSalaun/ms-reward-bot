import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

IMG_NOT_VAL = "#quizWelcomeContainer > span.rqWcHeader > span > div > img"


def quiz_task(driver, path_css):
    wait = WebDriverWait(driver, 10)

    try:
        clicker = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, path_css)))
        clicker.click()
        time.sleep(3)

        driver.switch_to.window(driver.window_handles[1])

        run_quiz = wait.until(EC.visibility_of_element_located((By.ID, "rqStartQuiz")))

        if driver.find_element(By.CSS_SELECTOR, "#quizWelcomeContainer > span.rqWcHeader > span > span").text == "30":

            img_value = driver.find_element(By.CSS_SELECTOR, IMG_NOT_VAL)
            if img_value.get_attribute("alt") == "Image du signe plus":
                print("Quiz TODO")
                run_quiz.click()
                time.sleep(1)

                button_index = 0
                button_id = "rqAnswerOption" + str(button_index)
                good_answer_count = driver.find_element(By.ID, "bt_corOpCnt")

                for question_num in range(1, 4):
                    button_index = 0
                    print(good_answer_count)
                    print(button_index)
                    while good_answer_count != "5":
                        try:
                            button = driver.find_element(By.ID, button_id)
                            button.click()
                            button_index += 1
                            button_id = "rqAnswerOption" + str(button_index)
                            print(good_answer_count)
                            time.sleep(2)
                        except NoSuchElementException:
                            print("Button not found")
                            break
                    time.sleep(5)
                time.sleep(5)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            else:
                print("ALREADY VALIDATED")
        else:
            print("No 30 pts")

    except Exception as e:
        print("The error is: ", e)
        pass
