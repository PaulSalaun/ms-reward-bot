import json
import os
import time

from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

from daily_requests.connexion import bingconnect, bingdisconnect
from daily_requests.progress import reward_count
from daily_requests.reward import daily
from profils import profile_manager


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    print(context)

    date = time.time().__str__().split('.')[0]
    webhook = DiscordWebhook(
        url="https://discord.com/api/webhooks/1255453326481424405/M98g63d5MSOLgVMbzil0hlJFi3Zj2RNyY_cqbF-YLeIkR9pHFKT3SvaTpGCZaMjyBzMP",
        content="** Resultat du <t:" + date + ":D> ** ")

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"

    service = ChromeService(executable_path=os.getcwd() + '/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    for i in range(0, profile_manager.get_len()):
        print('[START]', '------------- ', profile_manager.get_email(i), '--------------')

        setCredentials(profile_manager.get_email(i), profile_manager.get_pass(i))

        print("Current session is {}".format(driver.session_id))
        bingconnect.connect(driver, profile_manager.get_email(i), profile_manager.get_pass(i), 1)
        daily.define_daily(driver, i)
        daily.other_cards(driver)
        rewards, streak = reward_count.get_points(driver)
        bingdisconnect.disconnect(driver)
        print('[DISCONNECTED][DAILY]', profile_manager.get_email(i))
        driver.close()
        driver.quit()

        print('[DATA]', 'Reward updated', profile_manager.get_reward(i))
        print('[DATA]', 'Streak updated', profile_manager.get_streak(i))
        print('[END]', '------------- ', profile_manager.get_email(i), '--------------')

        embed = DiscordEmbed(title=profile_manager.get_email(i),
                             description="Points Reward : " + profile_manager.get_reward(i), color="03b2f8")
        webhook.add_embed(embed)
    webhook.execute()


def setCredentials(email: str, password: str):
    global profile_email
    global profile_pass
    profile_email = email
    profile_pass = password


def getMail():
    return profile_email


def getPass():
    return profile_pass


if __name__ == '__main__':
    lambda_handler(None, None)
