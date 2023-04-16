import os
import pdb
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.connexion import page_cookies

LINK = "https://www.bing.com/search?q=test&form=QBLH&sp=-1&lq=0&pq=test&sc=10-4&qs=n&sk=&cvid=0DBE77F2E2C44D9FAAE8BDCFDAC627ED&ghsh=0&ghacc=0&ghpl="


def web_surfer(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(LINK)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "words.txt")

    page_cookies.quit_page_cookies(driver)

    time.sleep(1)
    with open(file_path, 'r') as file:
        words = file.read().split()
        for word in words:
            element = driver.find_element(By.ID, 'sb_form_q')
            try:
                element.clear()
            except:
                pass
            finally:
                time.sleep(1)
                element.send_keys(word)
                element.submit()
