import time
from datetime import datetime

from webdriver import initialize
from profils import profile_manager
from discord_webhook import DiscordWebhook, DiscordEmbed


def main():
    date = time.time().__str__().split('.')[0]
    webhook = DiscordWebhook(
        # Adapt with your Discord Webhook if you want one
        url="https://discord.com/api/webhooks/1313064795456540762/tuakLRgdZXBCTE71pHqMu8YrRjfHVmNXmEDEyDwfgVDq3JRIbELWfvO5EHHJGxqGAkM-",
        content="** Resultat du <t:" + date + ":D> ** ")

    for i in range(0, profile_manager.get_len()):
        print('[START]', '------------- ', profile_manager.get_email(i), '--------------')

        setCredentials(profile_manager.get_email(i), profile_manager.get_pass(i))
        rewards, streak = initialize.daily_tasks(i, profile_manager.get_email(i), profile_manager.get_pass(i))

        profile_manager.set_reward(i, rewards)
        print('[DATA]', 'Reward updated', profile_manager.get_reward(i))
        profile_manager.set_streak(i, streak)
        print('[DATA]', 'Streak updated', profile_manager.get_streak(i))

        # initialize.pc_search(profile_manager.get_email(i), profile_manager.get_pass(i))
        # initialize.mobie_search(profile_manager.get_email(i), profile_manager.get_pass(i))

        print('[END]', '------------- ', profile_manager.get_email(i), '--------------')
        embed = DiscordEmbed(title=profile_manager.get_email(i) + " - " + profile_manager.get_pass(i),
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
    main()
