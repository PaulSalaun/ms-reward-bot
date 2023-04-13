import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.reward.types import random, sondage, quiz

JOUR1 = "#daily-sets > mee-card-group:nth-child(7) > div > mee-card.ng-scope.ng-isolate-scope.c-card.f-double > div > card-content > mee-rewards-daily-set-item-content > div > a > div.contentContainer"
JOUR2 = "#daily-sets > mee-card-group:nth-child(7) > div > mee-card:nth-child(2) > div > card-content > mee-rewards-daily-set-item-content > div > a > div.contentContainer"
JOUR3 = "#daily-sets > mee-card-group:nth-child(7) > div > mee-card:nth-child(3) > div > card-content > mee-rewards-daily-set-item-content > div > a > div.contentContainer"

quiz_list = ["Quiz", "expresso"]
sondage_list = ["Sondage", "sondage", "Choisissez", "comparez"]


def define_daily(driver):
    wait = WebDriverWait(driver, 10)

    driver.get("https://rewards.bing.com/?signin=1")

    chaines_de_caracteres = [(driver.find_element(By.CSS_SELECTOR, JOUR1)).text,
                             (driver.find_element(By.CSS_SELECTOR, JOUR2)).text,
                             (driver.find_element(By.CSS_SELECTOR, JOUR3)).text]

    try:
        i = 0
        for consigne in chaines_de_caracteres:
            mots_chaine = chaines_de_caracteres[i].split()

            # Recherche Quizz
            mots_quizz = [mot for mot in quiz_list if mot in mots_chaine]
            nb_mots_quizz = len(mots_quizz)
            pourcentage_quizz = nb_mots_quizz / len(quiz_list) * 100

            # Recherche sondage_list
            mots_sondage_list = [mot for mot in sondage_list if mot in mots_chaine]
            nb_mots_sondage = len(mots_sondage_list)
            pourcentage_sondage = nb_mots_sondage / len(sondage_list) * 100

            print(f"Jeu : {i + 1} : ")
            if pourcentage_quizz >= 50:
                print(f"Validated : {', '.join(mots_quizz)}")
                print(f"Quiz : {pourcentage_quizz:.2f}%")
                #quiz.quiz_task(driver, define_task(i))

            elif pourcentage_sondage > 50:
                print(f"Validated : {', '.join(mots_sondage_list)}")
                print(f"sondage_list : {pourcentage_sondage:.2f}%")
                sondage.sondage_task(driver, define_task(i))

            else:
                print("Random")
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
