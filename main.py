import json
import os
import time
from random import randint
from tempfile import mkdtemp

from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium import webdriver
from selenium.common import ElementNotInteractableException, NoSuchElementException, InvalidSessionIdException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ProfileManager:
    def __init__(self):
        self.user_email = os.getenv("PROFILE_EMAIL")
        self.user_password = os.getenv("PROFILE_PASSWORD")

    def get_email(self):
        return self.user_email

    def get_password(self):
        return self.user_password


LINK = "https://www.bing.com/"
CONNECT_LINK = "https://login.live.com/"


def page_load(driver: WebDriver):
    wait = WebDriverWait(driver, 1)
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except:
        pass


def get_points(driver: WebDriver) -> str:
    wait = WebDriverWait(driver, 1)
    try:
        driver.get('https://rewards.microsoft.com/dashboard')
    except InvalidSessionIdException:
        print("[Rewards] Invalid session id")
        driver.quit()
        driver = getDriver()
        driver.get('https://rewards.microsoft.com/dashboard')

    # Look for web error
    error_pipe(driver)
    # Cookies pop-up closed
    quit_page_cookies(driver)

    page_load(driver)
    time.sleep(2)

    rewards_nb = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "#balanceToolTipDiv > p > mee-rewards-counter-animation > span"))).text
    return rewards_nb


# 1: DAILY / 2: PC SEARCH / 3: MOBILE SEARCH
def connect(driver: WebDriver, email: str, password: str):
    wait = WebDriverWait(driver, 1)

    driver.get('https://rewards.microsoft.com/dashboard')
    time.sleep(1)

    # Look for web error
    error_pipe(driver)

    try:
        print('[WEB]', email)
        email_connect(driver, email, password)
        print('[CONNECT]', 'Connected successfully', email)
        try:
            security = wait.until(EC.visibility_of_element_located((By.ID, 'iLandingViewAction')))
            security.click()
            print('[CONNECT]', 'Security popup')
            page_load(driver)
        except:
            pass

        try:
            popup = wait.until(EC.visibility_of_element_located((By.ID, 'idBtn_Back')))
            popup.click()
            print('[CONNECT]', 'Stay connected popup')
        except:
            pass
        try:
            popup = wait.until(EC.visibility_of_element_located((By.ID, 'declineButton')))
            popup.click()
            print('[CONNECT]', 'Stay connected popup')
        except:
            pass
        page_load(driver)

    except Exception as e:
        print('[STOP]', 'Error in connect : ', e)

    # Look for web error
    error_pipe(driver)


def email_connect(driver: WebDriver, email: str, password: str):
    wait = WebDriverWait(driver, 1)

    email_input = wait.until(EC.visibility_of_element_located((By.ID, 'i0116')))
    email_input.send_keys(email)
    next_button = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
    next_button.click()

    # pdb.set_trace()
    time.sleep(2)

    pass_input = wait.until(EC.visibility_of_element_located((By.ID, 'i0118')))
    pass_input.send_keys(password)
    end_button = wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
    end_button.click()
    time.sleep(0.33)


DECO_LINK = "https://rewards.bing.com/Signout"
CLEAR_DATA_LINK = "chrome://settings/clearBrowserData"


def disconnect(driver: WebDriver):
    wait = WebDriverWait(driver, 1)
    driver.get(DECO_LINK)
    time.sleep(1)
    try:
        driver.delete_all_cookies()
        time.sleep(1)
        # Clear browser datas
        driver.get(CLEAR_DATA_LINK)
        body = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
        body.send_keys(Keys.RETURN)
    except Exception as e:
        print('[ERROR]', 'Error in disconnection', e)


ERROR_CONNECT = "body > div.simpleSignIn > div.signInOptions > span > a"
ERROR_502_ID = "error-information-popup-content"

COOKIES_ID = "bnp_btn_accept"
HEADER_COOKIES_ID = "wcpConsentBannerCtrl"
HEADER_COOKIES_BUTTON = "#wcpConsentBannerCtrl > div._2j0fmugLb1FgYz6KPuB91w > button:nth-child(1)"
REWARD_BANNER_ID = "mbing-banner"

REWARD_URL = "https://rewards.bing.com/"
VALIDATED = '/div/card-content/mee-rewards-daily-set-item-content/div/a/mee-rewards-points/div/div/span[1]'
TASK_DONE = 'mee-icon mee-icon-SkypeCircleCheck'
TASK_NOT_DONE = 'mee-icon mee-icon-AddMedium'

IMG_NOT_VAL = "#quizWelcomeContainer > span.rqWcHeader > span > div > img"

POINT_GAIN = "#btoHeadPanel > span.rqMenubar > span.rqText > span > span.rqEarnedPoints > span"

VALIDATION = "#btPollOverlay > span > div > img"
CARD_CSS = "#more-activities > div > mee-card:nth-child({})"
VALIDATED_CSS = "#more-activities > div > mee-card:nth-child({}) > div > card-content > mee-rewards-more-activities-card-item > div > a > mee-rewards-points > div > div > span.mee-icon.mee-icon-SkypeCircleCheck"
NOT_VALIDATED_CSS = "#more-activities > div > mee-card:nth-child({}) > div > card-content > mee-rewards-more-activities-card-item > div > a > mee-rewards-points > div > div > span.mee-icon.mee-icon-AddMedium"
POPUP_SPOTIFY = "#modal-host > div:nth-child(2) > button"

POPUP_CLOSE = "//*[@id='modal-host']/div[2]"
LINK_ACTUALITE = "//*[@id='legalTextBox']/div/div/div[3]/a"

STATUS_CHECKED = "mee-icon mee-icon-SkypeCircleCheck"
NOT_EDGED = "//*[@id='legalTextBox']/div/div/div[3]/a/span/ng-transclude"


def reconnect_session(driver: WebDriver):
    time.sleep(0.5)
    try:
        driver.find_element(By.CSS_SELECTOR, ERROR_CONNECT).click()
        print('[DISCONNECT]', 'Reconnection done')
        time.sleep(2)
    except:
        pass


def error_pipe(driver: WebDriver):
    error_502(driver)


def error_502(driver: WebDriver):
    try:
        while True:
            if driver.find_element(By.ID, ERROR_502_ID):
                time.sleep(10)
                driver.refresh()
            else:
                print('[ERROR 502]', 'Done')
    except:
        pass


def quit_page_cookies(driver: WebDriver):
    page_load(driver)
    time.sleep(1)
    try:
        driver.find_element(By.ID, COOKIES_ID).click()
        print('[COOKIES]', 'Pop-up cookies closed')
    except:
        pass


def quit_reward_banner(driver: WebDriver):
    time.sleep(1)
    try:
        banner = driver.find_element(By.ID, REWARD_BANNER_ID)
        style_before = banner.get_attribute("style")
        if "display: none;" not in style_before:
            print('[COOKIES]', 'Reward banner present')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            style_before = banner.get_attribute("style")
            if "display: none;" in style_before:
                print('[COOKIES]', 'Reward banner closed')
            else:
                print('[ERROR COOKIES]', 'Banner always present')
    except NoSuchElementException:
        pass


def header_cookies(driver: WebDriver):
    try:
        driver.find_element(By.CSS_SELECTOR, HEADER_COOKIES_BUTTON).click()
        print('[COOKIES]', 'Header cookies closed')
        time.sleep(1)
    except NoSuchElementException:
        pass


JOUR1 = '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[1]'
JOUR2 = '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[2]'
JOUR3 = '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[3]'

quiz_list = ["Quiz", "connaissez", "réponse", "expresso", "bonus", "pause-café"]
sondage_list = ["Sondage", "Choisissez", "comparez", "préférence"]
ceci_cela_list = ["correctement", "Ceci", "cela?", "jusqu’à", "question,", "50"]


def define_daily(driver: WebDriver):
    wait = WebDriverWait(driver, 1)
    header_cookies(driver)
    page_load(driver)

    try:
        popup = wait.until(EC.visibility_of_element_located((By.ID, 'reward_pivot_earn')))
        popup.click()
        time.sleep(1)
        if popup.is_displayed():
            popup.click()
        print('[CONNECT]', 'Streak popup')
    except:
        pass

    chaines_de_caracteres = generate_cdc(driver)

    try:
        assign_task(driver, chaines_de_caracteres)

    except ElementNotInteractableException:
        print('[ERROR]', 'Element not interactable')
        time.sleep(1)
        reconnect_session(driver)
        quit_page_cookies(driver)
        try:
            assign_task(driver, chaines_de_caracteres)
        except:
            print('[ERROR]', 'Never interactable')
            pass

    except Exception as e:
        print('[ERROR]', e)
        pass


def assign_task(driver: WebDriver, cdc: list):
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
                quiz(driver, define_task(i, driver), 1)
            if "bonus" in mots_chaine:
                print('[QUIZ]', 'bonus')
                quiz(driver, define_task(i, driver), 1)
            else:
                print('[QUIZ]', 'expresso')
                quiz(driver, define_task(i, driver), 2)

        elif pourcentage_ceci_cela > 50:
            # print(f"Validated : {', '.join(mots_ceci_cela_list)}")
            print('[DAILY]', {i + 1}, f"Ceci cela: {pourcentage_ceci_cela:.2f}%")
            ceci_cela(driver, define_task(i, driver))

        elif pourcentage_sondage > 50:
            # print(f"Validated : {', '.join(mots_sondage_list)}")
            print('[DAILY]', {i + 1}, f"Sondage : {pourcentage_sondage:.2f}%")
            sondage_task(driver, define_task(i, driver))

        else:
            print('[DAILY]', {i + 1}, 'Random')
            random_task(driver, define_task(i, driver))

        time.sleep(1)
        i += 1


def other_cards(driver: WebDriver):
    try:
        print('[CARDS]', 'Started')
        more_cards(driver)
    except Exception as e:
        print("[CARDS]", "No more cards")
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
        page_load(driver)
        if driver.find_element(By.XPATH, JOUR1):
            chaines_de_caracteres.append(driver.find_element(By.XPATH, JOUR1).text)
            chaines_de_caracteres.append(driver.find_element(By.XPATH, JOUR2).text)
            chaines_de_caracteres.append(driver.find_element(By.XPATH, JOUR3).text)
        else:
            print('NO CSS')
        return chaines_de_caracteres
    except Exception as e:
        driver.save_screenshot("connect.png")
        print("[CONNECT]", "Error while connecting ", e)


def random_task(driver: WebDriver, xpath: str):
    wait = WebDriverWait(driver, 1)
    time.sleep(1)

    try:
        clicker = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        clicker.click()
        driver.switch_to.window(driver.window_handles[1])
        page_load(driver)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.get(REWARD_URL)
        page_load(driver)

        validation_task = driver.find_element(By.XPATH, xpath + VALIDATED)
        if validation_task.get_attribute("class") == TASK_DONE:
            print('[RANDOM]', 'Done')
        elif validation_task.get_attribute("class") == TASK_NOT_DONE:
            print('[RANDOM]', 'Not Validated')
            random_task(driver, xpath)
        else:
            print('[RANDOM]', 'ERROR')

    except Exception as e:
        print("[RANDOM]", "Error: ", e)
        pass


def quiz(driver: WebDriver, xpath: str, style: int):
    wait = WebDriverWait(driver, 1)

    try:
        clicker = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        clicker.click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])

        # Disconnect error
        reconnect_session(driver)

        # Cookies pop-up closed
        quit_page_cookies(driver)
        # *** TASK ***

        task_quiz(driver, style)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.get(REWARD_URL)
        page_load(driver)

        validation_task = driver.find_element(By.XPATH, xpath + VALIDATED)
        if validation_task.get_attribute("class") == TASK_DONE:
            print('[QUIZ]', 'Done')
        elif validation_task.get_attribute("class") == TASK_NOT_DONE:
            print('[QUIZ]', 'Not Validated')
            task_quiz(driver, style)
        else:
            print('[QUIZ]', 'ERROR')

    except Exception as e:
        print("The error is in QUIZ: ", e)
        pass


def task_quiz(driver: WebDriver, style: int):
    wait = WebDriverWait(driver, 1)
    reconnect_session(driver)
    quit_page_cookies(driver)

    page_load(driver)
    try:
        driver.find_element(By.ID, "quizCompleteContainer")
        pass
    except:
        try:
            driver.implicitly_wait(1)
            run_quiz = driver.find_element(By.ID, "rqStartQuiz")
            run_quiz.click()
        except:
            print('QUIZ', 'Already started')
            pass

        while True:
            page_load(driver)
            time.sleep(1)
            try:
                driver.find_element(By.ID, "quizCompleteContainer")
                print('Quiz complete')
                break
            except:
                if style == 1:
                    click_case_correct_option(driver)
                else:
                    click_case(driver)
    else:
        print('[QUIZ]', 'KO')


def click_case_correct_option(driver: WebDriver):
    button_index = 0
    wait = WebDriverWait(driver, 1)
    page_load(driver)

    try:
        while driver.find_element(By.ID, "bt_corOpCnt").text != "5":
            print('[Quiz]', driver.find_element(By.ID, "bt_corOpCnt").text)
            button = wait.until(EC.visibility_of_element_located((By.ID, "rqAnswerOption" + str(button_index))))
            if button.get_attribute("iscorrectoption") == "True":
                button.click()
            if button_index == 8:
                print('[Quiz]', 'Error find truth, reboot')
                button_index = 0
                driver.implicitly_wait(1)
            else:
                pass
            driver.implicitly_wait(1)
            button_index += 1
    except:
        pass


def click_case(driver: WebDriver):
    button_index = 0
    is_finished = True
    wait = WebDriverWait(driver, 1)
    while is_finished:
        print('[QUIZ]', button_index)
        page_load(driver)
        time.sleep(2)
        if button_index == 4:
            print('[QUIZ]', 'raz')
            button_index = 0
        try:
            driver.find_element(By.ID, "rqAnswerOption" + str(button_index))
            button = wait.until(EC.visibility_of_element_located((By.ID, "rqAnswerOption" + str(button_index))))
            button.click()
            button_index += 1
        except:
            print('[QUIZ]', 'Break')
            is_finished = False
            driver.implicitly_wait(1)


def ceci_cela(driver: WebDriver, xpath: str):
    wait = WebDriverWait(driver, 1)
    time.sleep(1)

    try:
        clicker = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        clicker.click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)

        # Disconnect error
        reconnect_session(driver)

        # Cookies pop-up closed
        quit_page_cookies(driver)

        # *** TASK ***
        task_cecicela(driver)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()
        page_load(driver)

        validation_task = driver.find_element(By.XPATH, xpath + VALIDATED)
        if validation_task.get_attribute("class") == TASK_DONE:
            print('[CECI-CELA]', 'Done')
        elif validation_task.get_attribute("class") == TASK_NOT_DONE:
            print('[CECI_CELA]', 'Not Validated')
            ceci_cela(driver, xpath)
        else:
            print('[CECI-CELA]', 'ERROR')

    except Exception as e:
        print("The error is: ", e)
        pass


def task_cecicela(driver: WebDriver):
    wait = WebDriverWait(driver, 1)
    page_load(driver)
    reconnect_session(driver)
    quit_page_cookies(driver)

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
                page_load(driver)
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


def sondage_task(driver: WebDriver, xpath: str):
    wait = WebDriverWait(driver, 1)
    time.sleep(1)
    try:
        clicker = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        clicker.click()
        driver.switch_to.window(driver.window_handles[1])

        # Disconnect error
        reconnect_session(driver)
        # Cookies pop-up closed
        quit_page_cookies(driver)

        image_validation = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, VALIDATION)))
        if image_validation.get_attribute("alt") == "Image d’une coche":
            pass

        else:
            choix_sondage = wait.until(EC.visibility_of_element_located((By.ID, "btoption1")))
            choix_sondage.click()
            time.sleep(5)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.get(REWARD_URL)
        page_load(driver)

        validation_task = driver.find_element(By.XPATH, xpath + VALIDATED)
        if validation_task.get_attribute("class") == TASK_DONE:
            print('[SONDAGE]', 'Done')
        elif validation_task.get_attribute("class") == TASK_NOT_DONE:
            print('[SONDAGE]', 'Not Validated')
            sondage_task(driver, xpath)
        else:
            print('[SONDAGE]', 'ERROR')

    except Exception as e:
        print("The error is in SONDAGE: ", e)
        pass


# If switch onglet -> Task / Popup
def more_cards(driver: WebDriver):
    wait = WebDriverWait(driver, 1)
    i = 1
    while True:
        time.sleep(2)
        page_load(driver)
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
                page_load(driver)
                task_quiz(driver, 2)
            elif "quiz" in card.text.lower().split() and "bonus" in card.text.lower().split():
                print('[CARD]', i, 'Quiz bonus')
                card.click()
                driver.switch_to.window(driver.window_handles[1])
                page_load(driver)
                task_quiz(driver, 1)
            elif "quiz" in card.text.lower().split() and "pause-café" in card.text.lower().split():
                print('[CARD]', i, 'Quiz pause café')
                card.click()
                driver.switch_to.window(driver.window_handles[1])
                page_load(driver)
                task_quiz(driver, 1)
            elif "cela?" in card.text.lower().split():
                print('[CARD]', i, 'Ceci cela')
                card.click()
                driver.switch_to.window(driver.window_handles[1])
                page_load(driver)
                task_cecicela(driver)
            elif "bing" in card.text.lower().split() and (
                    "avec" in card.text.lower().split() or "sur" in card.text.lower().split()):
                print('[CARD]', i, 'Recherche')
                answer = "Not learn"
                for key in SearchEnum.search_enum_dict:
                    if key in card.text.lower():
                        answer = SearchEnum.search_enum_dict[key]
                print('[Recherche]', i, "-", answer)
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
                    page_load(driver)
                    time.sleep(1)
                except:
                    pass
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            page_load(driver)
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
            page_load(driver)
        else:
            pass
    except:
        pass


def rechercheTask(driver: WebDriver, value: str):
    page_load(driver)

    driver.get(
        "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=165&id=264960&wreply=https%3a%2f%2fwww.bing.com%2fsecure%2fPassport.aspx%3fedge_suppress_profile_switch%3d1%26requrl%3dhttps%253a%252f%252fwww.bing.com%252f%253fform%253dML2PCR%2526OCID%253dML2PCR%2526PUBL%253dRewardsDO%2526CREA%253dML2PCR%2526rwAutoFlyout%253dexb%2526wlexpsignin%253d1%26sig%3d1933D72C778565402BFDC21B769A641D%26nopa%3d2&wp=MBI_SSL&lc=1036&CSRFToken=2b834cc7-6ced-499c-bb0e-ba1be85b6095&cobrandid=c333cba8-c15c-4458-b082-7c8ce81bee85&aadredir=1&nopa=2")
    page_load(driver)

    recherche(driver, value)


def recherche(driver: WebDriver, value: str):
    try:
        element = driver.find_element(By.ID, 'sb_form_q')
        # element.click()
        element.send_keys(value)
        time.sleep(1)
        element.send_keys(Keys.RETURN)
        time.sleep(2)
        page_load(driver)
        if driver.find_element(By.ID, "bnp_container"):
            driver.find_element(By.ID, 'bnp_btn_reject').click()
            print('[Recherche]', "Cookies closed")
        else:
            pass
        time.sleep(2)
    except:
        pass


class SearchEnum:
    # Enum to link the answer for research cards
    search_enum_dict = {
        "quelle heure est-il ?": "quelle heure est-il au japon ?",
        "enrichissez votre vocabulaire": "signification polyphases",
        "suivez les élections": "résultats des élections",
        "faites vos achats plus vite": "casque sony wh-1000xm4 prix",
        "traduisez tout !": "traduction anglais étincellant",
        "rechercher paroles de chanson": "parole chanson macarena",
        "et si nous regardions ce film une nouvelle fois ?": "Cars 2",
        "vous avez des symptômes?": "symptome grippe",
        "apprendre à cuisiner recettes": "recette de risotto",
        "maisons près de chez vous!": "laforet immobilier",
        "trouvez des emplacements pour rester!": "Hostel Copenhague",
        "trop fatigué pour cuisiner ce soir?": "buffalo grill merignac",
        "conversion rapide de monnaie": "conversion couronne suedoise euro",
        "vérifier la météo": "quel temps fera t il demain",
        "comment se porte l’économie": "SP 500",
        "qui a gagné": "résultat brest l1",
        "temps de jeu": "snapshot Minecraft",
        "trouver un endroit à découvrir": "Suisse",
        "planifiez une petite escapade": "vol bordeaux açores",
        "tenez-vous informé des sujets d’actualité": "actualité sb29",
        "consulter postes à pourvoir": "poste à pourvoir mcdo"
    }


def getDriver():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_options.add_argument(f"--data-path={mkdtemp()}")
    chrome_options.add_argument(f"--disk- cache-dir={mkdtemp()}")
    chrome_options.add_argument("--remote-debugging-pipe")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--log-path=/tmp")
    chrome_options.binary_location = "/opt/chrome/chrome-linux64/chrome"

    service = Service(
        executable_path="/opt/chrome-driver/chromedriver-linux64/chromedriver",
        service_log_path="/tmp/chromedriver.log"
    )

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )

    return driver


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    print(context)

    manager = ProfileManager()
    email = manager.get_email()
    password = manager.get_password()

    discord = os.getenv("DISCORD_WEBHOOK")

    driver = getDriver()

    print('[START]', '------------- ', email, '--------------')
    print("Current session is {}".format(driver.session_id))

    # Connect user from dict
    connect(driver, email, password)

    # Run daily tasks to obtain the streak
    define_daily(driver)
    # Run cards to obtain more rewards
    other_cards(driver)

    # Get the user's rewards
    reward = get_points(driver)

    # Disconnect user
    disconnect(driver)
    print('[DISCONNECTED][DAILY]', email)
    driver.close()
    driver.quit()

    print('[DATA]', 'Reward updated', reward)
    print('[END]', '------------- ', email, '--------------')

    if discord:
        webhook = DiscordWebhook(
            url=discord
        )
        embed = DiscordEmbed(title=email,
                             description="Points Reward : " + reward, color="03b2f8")
        webhook.add_embed(embed)
        webhook.execute()

    return {
        "statusCode": 200,
        "body": json.dumps(event),
    }


if __name__ == '__main__':
    lambda_handler(None, None)
