import os
import time
import asyncio

from selenium import webdriver
from selenium.webdriver.edge.options import Options

from requests.connexion import bingconnect
from requests.connexion import bingdisconnect
from requests.reward import daily
from requests.research import search


def run_driver(email, password):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    profile_dir = os.path.join(project_dir, "botboy")

    options = Options()
    options.add_argument(f"--user-data-dir={profile_dir}")

    driver = webdriver.Edge(options=options)
    driver.get('https://bing.com')
    time.sleep(2)

    bingconnect.connect(driver, email, password)

    # Actions for daily rewards
    #daily.define_daily(driver)

    # Actions for daily research
    search.web_surfer(driver)

    bingdisconnect.disconnect(driver)

    driver.quit()
