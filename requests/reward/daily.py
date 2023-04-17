import pdb
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.connexion import page_cookies
from requests.reward.types import random, sondage, quiz, cecicela

JOUR1 = "#daily-sets > mee-card-group:nth-child(7) > div > mee-card.ng-scope.ng-isolate-scope.c-card.f-double > div > card-content > mee-rewards-daily-set-item-content > div > a > div.contentContainer"
JOUR2 = "#daily-sets > mee-card-group:nth-child(7) > div > mee-card:nth-child(2) > div > card-content > mee-rewards-daily-set-item-content > div > a > div.contentContainer"
JOUR3 = "#daily-sets > mee-card-group:nth-child(7) > div > mee-card:nth-child(3) > div > card-content > mee-rewards-daily-set-item-content > div > a > div.contentContainer"

quiz_list = ["Quiz", "connaissez", "réponse", "expresso", "bonus", "pause-café"]
sondage_list = ["Sondage", "Choisissez", "comparez", "préférence"]
ceci_cela_list = ["correctement", "Ceci", "cela?", "jusqu’à", "question,", "50"]


def define_daily(driver):
    wait = WebDriverWait(driver, 10)

    # Look for cookies
    page_cookies.header_cookies(driver)

    chaines_de_caracteres = [(driver.find_element(By.CSS_SELECTOR, JOUR1)).text,
                             (driver.find_element(By.CSS_SELECTOR, JOUR2)).text,
                             (driver.find_element(By.CSS_SELECTOR, JOUR3)).text]

    try:
        i = 0
        for jeu in chaines_de_caracteres:
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

            print('[JEU]', {i + 1})
            if pourcentage_quizz >= 50:
                # print(f"Validated : {', '.join(mots_quizz)}")
                print('[JEU]', f"Quiz : {pourcentage_quizz:.2f}%")
                quiz.quiz_task(driver, define_task(i))

            elif pourcentage_ceci_cela > 50:
                # print(f"Validated : {', '.join(mots_ceci_cela_list)}")
                print('[JEU]', f"Ceci cela: {pourcentage_ceci_cela:.2f}%")
                cecicela.ceci_cela_task(driver, define_task(i))

            elif pourcentage_sondage > 50:
                # print(f"Validated : {', '.join(mots_sondage_list)}")
                print('[JEU]', f"Sondage : {pourcentage_sondage:.2f}%")
                sondage.sondage_task(driver, define_task(i))

            else:
                print('[JEU]', 'Random')
                random.random_task(driver, define_task(i))

            i += 1

    except Exception as e:
        print("The error is: ", e)
        pass


def define_task(i):
    if i == 0:
        return JOUR1
    elif i == 1:
        return JOUR2
    else:
        return JOUR3
