import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.reward import daily
from requests.reward.types import quiz
from utils import time_wait

CARD_CSS = "#more-activities > div > mee-card:nth-child({})"
VALIDATED_CSS = "#more-activities > div > mee-card:nth-child({}) > div > card-content > mee-rewards-more-activities-card-item > div > a > mee-rewards-points > div > div > span.mee-icon.mee-icon-SkypeCircleCheck"
NOT_VALIDATED_CSS = "#more-activities > div > mee-card:nth-child({}) > div > card-content > mee-rewards-more-activities-card-item > div > a > mee-rewards-points > div > div > span.mee-icon.mee-icon-AddMedium"
POPUP_SPOTIFY = "#modal-host > div:nth-child(2) > button"

STATUS_CHECKED = "mee-icon mee-icon-SkypeCircleCheck"


def more_cards(driver: WebDriver):
    wait = WebDriverWait(driver, 10)
    try:
        i = 1
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, CARD_CSS.format(i))))
        # While cards are clickable, try to click it
        while True:
            try:
                card = driver.find_element(By.CSS_SELECTOR, CARD_CSS.format(i))
                try:
                    # If done -> pass
                    driver.find_element(By.CSS_SELECTOR, NOT_VALIDATED_CSS.format(i))

                    if "quiz" in card.text.lower().split() and "expresso" in card.text.lower().split():
                        print('[CARD]', i, 'Quiz expresso')
                        card.click()
                        driver.switch_to.window(driver.window_handles[1])
                        time_wait.page_load(driver)
                        quiz.task_quiz(driver)
                    elif "quiz" in card.text.lower().split() and "bonus" in card.text.lower().split():
                        print('[CARD]', i, 'Quiz bonus')
                        card.click()
                        driver.switch_to.window(driver.window_handles[1])
                        time_wait.page_load(driver)
                        quiz.task_quiz(driver)
                    else:
                        print('[CARD]', i, 'Random')
                        try:
                            # If Spotify offer, close it
                            close_spotify_popup(driver)
                        except:
                            card.click()
                            driver.switch_to.window(driver.window_handles[1])
                            time_wait.page_load(driver)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                except:
                    pass
                time.sleep(0.5)
                i += 1
            except:
                print('[CARDS]', 'Done')
                break

    except Exception as e:
        print("The error is: ", e)
        pass


def close_spotify_popup(driver: WebDriver):
    popup_close = driver.find_element(By.CSS_SELECTOR, POPUP_SPOTIFY)
    popup_close.click()
