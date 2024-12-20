import os
import pdb
import random
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from daily_requests.connexion import page_cookies
from utils import time_wait

LINK = "https://www.bing.com/"


def web_surfer(driver: WebDriver, num_research: int, isPC: int = 0):
    wait = WebDriverWait(driver, 10)
    driver.get(LINK)
    time_wait.page_load(driver)
    page_cookies.quit_page_cookies(driver)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "words.txt")

    if isPC == 1:
        print('[PC]', 'Connecting...')
        page_cookies.quit_page_cookies(driver)
        connect = driver.find_element(By.ID, "id_s")
        try:
            connect.click()
        except:
            pass

    with open(file_path, 'r') as file:
        words = file.read().split()
        print('[RESEARCH]', 'Started')

        num_words_to_send = min(num_research, len(words))
        random_words = random.sample(words, num_words_to_send)

        for word in random_words:
            try:
                # Cookies pop-up closed
                page_cookies.quit_page_cookies(driver)

                element = driver.find_element(By.ID, 'sb_form_q')
                element.clear()

                while element.get_attribute('value') != '':
                    time.sleep(0.5)
                    element.clear()

                element.send_keys(word)
                element.submit()
                wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
            except:
                print('[ERROR]', 'Refresh needed')
                driver.refresh()
                time.sleep(1)
    print('[RESEARCH]', 'Done')
