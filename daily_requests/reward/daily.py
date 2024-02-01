import pdb
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException

from profils import profile_manager
from daily_requests.connexion import page_cookies
from daily_requests.errors import error_manager
from daily_requests.reward.other import cards
from daily_requests.reward.types import default, sondage, quiz, cecicela
from utils import time_wait

JOUR1 = '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[1]'
JOUR2 = '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[2]'
JOUR3 = '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[3]'

quiz_list = ["Quiz", "connaissez", "réponse", "expresso", "bonus", "pause-café"]
sondage_list = ["Sondage", "Choisissez", "comparez", "préférence"]
ceci_cela_list = ["correctement", "Ceci", "cela?", "jusqu’à", "question,", "50"]


def define_daily(driver: WebDriver, profil_index: int):
    # Look for cookies
    page_cookies.header_cookies(driver)
    time_wait.page_load(driver)
    time.sleep(1)

    chaines_de_caracteres = generate_cdc(driver)

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
            pass

    except Exception as e:
        print('[ERROR]', e)
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
            if "pause-café" in mots_chaine:
                print('[QUIZ]', 'Pause-café')
                quiz.quiz(driver, define_task(i, driver), 1)
            if "bonus" in mots_chaine:
                print('[QUIZ]', 'bonus')
                quiz.quiz(driver, define_task(i, driver), 1)
            else:
                print('[QUIZ]', 'expresso')
                quiz.quiz(driver, define_task(i, driver), 2)

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

        i += 1


def other_cards(driver: WebDriver):
    try:
        print('[CARDS]', 'Started')
        cards.more_cards(driver)
    except Exception as e:
        print("[CARDS] No more cards :")
        pass


def define_task(i: int, driver: WebDriver):
    if i == 0:
        return JOUR1
    elif i == 1:
        return JOUR2
    else:
        return JOUR3


def generate_cdc(driver: WebDriver):
    try:
        chaines_de_caracteres = []
        driver.refresh()
        time_wait.page_load(driver)
        if driver.find_element(By.XPATH, JOUR1):
            chaines_de_caracteres.append(driver.find_element(By.XPATH, JOUR1).text)
            chaines_de_caracteres.append(driver.find_element(By.XPATH, JOUR2).text)
            chaines_de_caracteres.append(driver.find_element(By.XPATH, JOUR3).text)
        else:
            print('NO CSS')
        return chaines_de_caracteres
    except Exception as e:
        print("[CONNECT]", "Error while connecting ", e)
