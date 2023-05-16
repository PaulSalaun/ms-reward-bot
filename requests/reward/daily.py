import pdb
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

from profils import profile_manager
from requests.connexion import page_cookies
from requests.errors import error_manager
from requests.reward.other import cards
from requests.reward.types import default, sondage, quiz, cecicela
from utils import time_wait

JOUR1 = "#daily-sets > mee-card-group:nth-child(7) > div > mee-card.ng-scope.ng-isolate-scope.c-card.f-double > div > " \
        "card-content > mee-rewards-daily-set-item-content > div > a > div.contentContainer"
JOUR2 = "#daily-sets > mee-card-group:nth-child(7) > div > mee-card:nth-child(2) > div > card-content > " \
        "mee-rewards-daily-set-item-content > div > a > div.contentContainer"
JOUR3 = "#daily-sets > mee-card-group:nth-child(7) > div > mee-card:nth-child(3) > div > card-content > " \
        "mee-rewards-daily-set-item-content > div > a > div.contentContainer"

JOUR1bis = "#daily-sets > mee-card-group:nth-child(5) > div > mee-card.ng-scope.ng-isolate-scope.c-card.f-double > " \
           "div > card-content > mee-rewards-daily-set-item-content > div"
JOUR2bis = "#daily-sets > mee-card-group:nth-child(5) > div > mee-card:nth-child(2)"
JOUR3bis = "#daily-sets > mee-card-group:nth-child(5) > div > mee-card:nth-child(3)"

quiz_list = ["Quiz", "connaissez", "réponse", "expresso", "bonus", "pause-café"]
sondage_list = ["Sondage", "Choisissez", "comparez", "préférence"]
ceci_cela_list = ["correctement", "Ceci", "cela?", "jusqu’à", "question,", "50"]


def define_daily(driver: WebDriver, profil_index: int):
    # Look for cookies
    page_cookies.header_cookies(driver)

    # Define the daily
    chaines_de_caracteres = []
    try:
        chaines_de_caracteres.append(driver.find_element(By.CSS_SELECTOR, JOUR1).text)
        chaines_de_caracteres.append(driver.find_element(By.CSS_SELECTOR, JOUR2).text)
        chaines_de_caracteres.append(driver.find_element(By.CSS_SELECTOR, JOUR3).text)
    except NoSuchElementException:
        chaines_de_caracteres.append(driver.find_element(By.CSS_SELECTOR, JOUR1bis).text)
        chaines_de_caracteres.append(driver.find_element(By.CSS_SELECTOR, JOUR2bis).text)
        chaines_de_caracteres.append(driver.find_element(By.CSS_SELECTOR, JOUR3bis).text)

    try:
        assign_task(driver, profil_index, chaines_de_caracteres)

    except ElementNotInteractableException:
        print('[ERROR]', 'Element not interactable')
        time.sleep(1)
        error_manager.reconnect_session(driver)
        page_cookies.quit_page_cookies(driver)
        try:
            assign_task(driver, profil_index, chaines_de_caracteres)
        except:
            print('[ERROR]', 'Never interactable')
            pdb.set_trace()
            pass

    except Exception as e:
        print('[ERROR]', e)
        pdb.set_trace()
        pass


def assign_task(driver: WebDriver, profil_index: int, cdc: list):
    i = 0
    for jeu in cdc:
        mots_chaine = jeu.split()

        # Recherche Quizz
        mots_quizz = [mot for mot in quiz_list if mot in mots_chaine]
        nb_mots_quizz = len(mots_quizz)
        pourcentage_quizz = nb_mots_quizz / len(quiz_list) * 100

        # Recherche Ceci cela
        mots_ceci_cela_list = [mot for mot in ceci_cela_list if mot in mots_chaine]
        nb_mots_ceci_cela = len(mots_ceci_cela_list)
        pourcentage_ceci_cela = nb_mots_ceci_cela / len(ceci_cela_list) * 100

        # Recherche sondage_list
        mots_sondage_list = [mot for mot in sondage_list if mot in mots_chaine]
        nb_mots_sondage = len(mots_sondage_list)
        pourcentage_sondage = nb_mots_sondage / len(sondage_list) * 100

        if pourcentage_quizz >= 50:
            # print(f"Validated : {', '.join(mots_quizz)}")
            print('[DAILY]', {i + 1}, f"Quiz : {pourcentage_quizz:.2f}%")
            quiz.quiz(driver, define_task(i, driver))

        elif pourcentage_ceci_cela > 50:
            # print(f"Validated : {', '.join(mots_ceci_cela_list)}")
            print('[DAILY]', {i + 1}, f"Ceci cela: {pourcentage_ceci_cela:.2f}%")
            cecicela.ceci_cela(driver, define_task(i, driver))

        elif pourcentage_sondage > 50:
            # print(f"Validated : {', '.join(mots_sondage_list)}")
            print('[DAILY]', {i + 1}, f"Sondage : {pourcentage_sondage:.2f}%")
            sondage.sondage_task(driver, define_task(i, driver))

        else:
            print('[DAILY]', {i + 1}, 'Random')
            default.random_task(driver, define_task(i, driver))

        # Set Task[i] -> Done
        # TODO Verify if done
        profile_manager.task_done(i + 1, profil_index)
        i += 1


def other_cards(driver: WebDriver):
    try:
        print('[CARDS]', 'Started')
        cards.more_cards(driver)
    except Exception as e:
        print("Can't do more cards :", e)
        pass


def define_task(i: int, driver: WebDriver):
    if i == 0:
        if driver.find_element(By.CSS_SELECTOR, JOUR1).is_displayed():
            return JOUR1
        else:
            return JOUR1bis
    elif i == 1:
        if driver.find_element(By.CSS_SELECTOR, JOUR2).is_displayed():
            return JOUR2
        else:
            return JOUR2bis
    else:
        if driver.find_element(By.CSS_SELECTOR, JOUR3).is_displayed():
            return JOUR3
        else:
            return JOUR3bis
