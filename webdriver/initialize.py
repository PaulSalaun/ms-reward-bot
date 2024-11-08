import undetected_chromedriver as uc

from daily_requests.connexion import bingconnect
from daily_requests.connexion import bingdisconnect
from daily_requests.progress import reward_count
from daily_requests.reward import daily


# DO DAILY TASKS
def daily_tasks(driver: uc.Chrome, profil_index: int, email: str, password: str) -> tuple[str, str]:

    return rewards, streak
