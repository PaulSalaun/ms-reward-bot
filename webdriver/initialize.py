from urllib.request import urlretrieve

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from daily_requests.connexion import bingconnect
from daily_requests.connexion import bingdisconnect
from daily_requests.progress import reward_count
from daily_requests.research import search
from daily_requests.reward import daily

PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51'
MOBILE_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
USER_DATA = 'C:/Users/paul.salaun/AppData/Local/Google/Chrome/User Data/Default'

CHROMEDRIVER_PATH = './chromedriver.exe'


# DO DAILY TASKS
def daily_tasks(profil_index: int, email: str, password: str) -> tuple[str, str]:
    optionshadow = Options()
    optionshadow.add_argument("--headless")
    driver = uc.Chrome(optionshadow, version_main=131, headless=False)
    print("Current session is {}".format(driver.session_id))
    driver.maximize_window()
    bingconnect.connect(driver, email, password, 1)
    daily.define_daily(driver, profil_index)
    daily.other_cards(driver)
    rewards, streak = reward_count.get_points(driver)
    bingdisconnect.disconnect(driver)
    print('[DISCONNECTED][DAILY]', email)
    driver.close()
    driver.quit()
    return rewards, streak


options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")


# DO PC RESEARCH
def pc_search(email: str, password: str):
    optionshadow = Options()
    optionshadow.add_argument("--headless")
    driver = uc.Chrome(optionshadow)
    bingconnect.connect(driver, email, password, 2)
    search.web_surfer(driver, 35, 1)
    bingdisconnect.disconnect(driver)
    print('[DISCONNECTED][PC SEARCH]', email)
    driver.close()
    driver.quit()


# DO MOBILE SEARCH
def mobie_search(email: str, password: str):
    options.add_argument("user-agent=" + MOBILE_USER_AGENT)
    driver = webdriver.Chrome(options=options)
    bingconnect.connect(driver, email, password, 3)
    search.web_surfer(driver, 25)
    bingdisconnect.disconnect(driver)
    print('[DISCONNECTED][MOBILE SEARCH]', email)
    driver.close()
    driver.quit()
