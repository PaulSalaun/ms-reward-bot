import os
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from requests.connexion import page_cookies

LINK = "https://www.bing.com/"


def web_surfer(driver: WebDriver):
    wait = WebDriverWait(driver, 10)
    driver.get(LINK)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "words.txt")

    with open(file_path, 'r') as file:
        words = file.read().split()
        print('[RESEARCH]', 'Started')
        for word in words:
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
            except:
                print('[ERROR]', 'Refresh needed')
                driver.refresh()
                time.sleep(1)
    print('[RESEARCH]', 'Done')

