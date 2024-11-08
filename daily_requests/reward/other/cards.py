import pdb
import string
import time
from random import random

from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import lambda_function
from daily_requests.reward.other.search_dict import SearchEnum
from daily_requests.reward.types import quiz, cecicela
from utils import time_wait

CARD_CSS = "#more-activities > div > mee-card:nth-child({})"
VALIDATED_CSS = "#more-activities > div > mee-card:nth-child({}) > div > card-content > mee-rewards-more-activities-card-item > div > a > mee-rewards-points > div > div > span.mee-icon.mee-icon-SkypeCircleCheck"
NOT_VALIDATED_CSS = "#more-activities > div > mee-card:nth-child({}) > div > card-content > mee-rewards-more-activities-card-item > div > a > mee-rewards-points > div > div > span.mee-icon.mee-icon-AddMedium"
POPUP_SPOTIFY = "#modal-host > div:nth-child(2) > button"

POPUP_CLOSE = "//*[@id='modal-host']/div[2]"
LINK_ACTUALITE = "//*[@id='legalTextBox']/div/div/div[3]/a"

STATUS_CHECKED = "mee-icon mee-icon-SkypeCircleCheck"
NOT_EDGED = "//*[@id='legalTextBox']/div/div/div[3]/a/span/ng-transclude"


# Todo -> Card NOT VALIDATED = action : None
# If switch onglet -> Task / Popup
def more_cards(driver: WebDriver):
    wait = WebDriverWait(driver, 10)
    i = 1
    while True:
        time.sleep(2)
        time_wait.page_load(driver)
        rebooter(driver)
        card = driver.find_element(By.CSS_SELECTOR, CARD_CSS.format(i))
        # card = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, CARD_CSS.format(i))))
        try:
            # If done -> pass
            driver.find_element(By.CSS_SELECTOR, NOT_VALIDATED_CSS.format(i))
            if "quiz" in card.text.lower().split() and "expresso" in card.text.lower().split():
                print('[CARD]', i, 'Quiz expresso')
                card.click()
                driver.switch_to.window(driver.window_handles[1])
                time_wait.page_load(driver)
                quiz.task_quiz(driver, 2)
            elif "quiz" in card.text.lower().split() and "bonus" in card.text.lower().split():
                print('[CARD]', i, 'Quiz bonus')
                card.click()
                driver.switch_to.window(driver.window_handles[1])
                time_wait.page_load(driver)
                quiz.task_quiz(driver, 1)
            elif "quiz" in card.text.lower().split() and "pause-café" in card.text.lower().split():
                print('[CARD]', i, 'Quiz pause café')
                card.click()
                driver.switch_to.window(driver.window_handles[1])
                time_wait.page_load(driver)
                quiz.task_quiz(driver, 1)
            elif "cela?" in card.text.lower().split():
                print('[CARD]', i, 'Ceci cela')
                card.click()
                driver.switch_to.window(driver.window_handles[1])
                time_wait.page_load(driver)
                cecicela.task_cecicela(driver)
            elif "bing" in card.text.lower().split() and (
                    "avec" in card.text.lower().split() or "sur" in card.text.lower().split()):
                print('[CARD]', i, 'Recherche')
                answer = "Not learn"
                for key in SearchEnum.search_enum_dict:
                    if key in card.text.lower():
                        answer = SearchEnum.search_enum_dict[key]
                print('[Recherche]', i, answer)
                card.click()
                driver.switch_to.window(driver.window_handles[1])
                if answer != "":
                    rechercheTask(driver, answer)
            elif "actualités" in card.text.lower().split():
                print('[CARD]', i, 'Actualite')
                card.click()
                wait.until(EC.visibility_of_element_located((By.XPATH, POPUP_CLOSE)))
                driver.find_element(By.XPATH, LINK_ACTUALITE).click()
                driver.switch_to.window(driver.window_handles[1])
            elif "suivez" in card.text.lower().split() and "visite" in card.text.lower().split():
                print('[CARD]', i, 'Visite guidée')
                card.click()
                wait.until(EC.visibility_of_element_located((By.ID, "welcome-tour-slide")))
                driver.find_element(By.XPATH, "//*[@id='modal-host']/div[2]/button").click()
                driver.switch_to.window(driver.window_handles[1])
            elif "microsoft" in card.text.lower().split() and "edge" in card.text.lower().split():
                print('[CARD]', i, 'Not Edge')
                card.click()
                wait.until(EC.visibility_of_element_located((By.XPATH, NOT_EDGED)))
                driver.find_element(By.XPATH, NOT_EDGED).click()
                driver.switch_to.window(driver.window_handles[1])
            else:
                print('[CARD]', i, 'Random')
                card.click()
                try:
                    driver.switch_to.window(driver.window_handles[1])
                    time_wait.page_load(driver)
                    time.sleep(1)
                except:
                    pass
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time_wait.page_load(driver)
        except:
            print('[CARD]', i, 'Done')
            pass
        i += 1


def close_spotify_popup(driver: WebDriver):
    popup_close = driver.find_element(By.CSS_SELECTOR, POPUP_SPOTIFY)
    popup_close.click()


def rebooter(driver: WebDriver):
    try:
        notyou = driver.find_element(By.TAG_NAME, "body")
        if "Ce n’est pas vous, c’est nous." in notyou.text:
            driver.refresh()
            time_wait.page_load(driver)
        else:
            pass
    except:
        pass


def rechercheTask(driver: WebDriver, value: str):
    wait = WebDriverWait(driver, 10)
    time_wait.page_load(driver)
    # driver.save_screenshot("screenshots/recherche_home.png")

    connect = driver.find_element(By.ID, "id_l")
    # No connected ->
    if connect.text.lower().__contains__("connexion"):
        connect.click()
        time.sleep(1)

        try:
            print('[Recherche]', "Non connecté", main.getMail())
            driver.find_element(By.ID, "id_text_signin").click()
            time.sleep(2)

            email_input = wait.until(EC.visibility_of_element_located((By.ID, 'i0116')))
            email_input.send_keys(main.getMail())
            next_button = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
            next_button.click()
            time.sleep(2)

            pass_input = wait.until(EC.visibility_of_element_located((By.ID, 'i0118')))
            pass_input.send_keys(main.getPass())
            next_button.click()
            time.sleep(2)

            try:
                popup = wait.until(EC.visibility_of_element_located((By.ID, 'declineButton')))
                popup.click()
                print('[CONNECT]', 'Stay connected popup')
            except:
                pass

            recherche(driver, value)
        except:
            print('[Recherche]', "ERROR: Account item not found")

        try:
            print('[Recherche]', "Connecté")
            recherche(driver, value)
        except:
            print('[Recherche]', "ERROR: Already connected")
    else:
        recherche(driver, value)


def recherche(driver: WebDriver, value: str):
    try:
        element = driver.find_element(By.ID, 'sb_form_q')
        element.click()
        element.send_keys(value)
        time.sleep(1)
        element.send_keys(Keys.RETURN)
        time.sleep(2)
        time_wait.page_load(driver)
        if driver.find_element(By.ID, "bnp_container"):
            driver.find_element(By.ID, 'bnp_btn_reject').click()
            print('[Recherche]', "Cookies closed")
        else:
            pass
        time.sleep(2)
    except:
        print('[Recherche]', "Break")
        pass
