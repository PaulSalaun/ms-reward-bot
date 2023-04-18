import os
import pdb
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from requests.connexion import bingconnect
from requests.connexion import bingdisconnect
from requests.reward import daily
from requests.research import search
from requests.progress import reward_count

PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51'
MOBILE_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'


def run_driver(email: str, password: str, isMobile: bool):
    options = Options()
    if not isMobile:
        options.add_argument("user-agent=" + PC_USER_AGENT)
        driver = webdriver.Chrome(options=options)

        bingconnect.connect(driver, email, password, isMobile)

        # Actions for daily rewards
        daily.define_daily(driver)

        # Actions for daily research
        search.web_surfer(driver)

        bingdisconnect.disconnect(driver)
        driver.quit()

    else:
        options.add_argument("user-agent=" + MOBILE_USER_AGENT)
        driver = webdriver.Chrome(options=options)

        bingconnect.connect(driver, email, password, isMobile)

        # Mobile search
        search.web_surfer(driver)

        # Get the reward count
        rewards, streak = reward_count.get_points(driver)

        bingdisconnect.disconnect(driver)
        driver.quit()

        return rewards, streak
