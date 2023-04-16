import os
import time
import asyncio

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from requests.connexion import bingconnect
from requests.connexion import bingdisconnect
from requests.reward import daily
from requests.research import search
from requests.progress import reward_count

PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'


def run_driver(email, password):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    profile_dir = os.path.join(project_dir, "botboy")

    options = Options()
    options.add_argument("user-agent=" + PC_USER_AGENT)
    prefs = {"profile.default_content_setting_values.geolocation": 2,
             "credentials_enable_service": False,
             "profile.password_manager_enabled": False,
             "webrtc.ip_handling_policy": "disable_non_proxied_udp",
             "webrtc.multiple_routes_enabled": False,
             "webrtc.nonproxied_udp_enabled": False}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    driver.get('https://rewards.microsoft.com/dashboard')
    time.sleep(1)

    bingconnect.connect(driver, email, password)

    # Actions for daily rewards
    daily.define_daily(driver)

    # Actions for daily research
    search.web_surfer(driver)

    # Get the reward count
    rewards = reward_count.get_points(driver)

    bingdisconnect.disconnect(driver)
    driver.quit()
    return rewards
