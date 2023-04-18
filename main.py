import pdb

from webdriver import initialize
from profils import profile_manager

from prettytable import PrettyTable


def main():
    table = PrettyTable()
    table.field_names = ["Email", "Rewards"]

    result_table = []
    for i in range(0, profile_manager.get_len()):
        # Computer
        initialize.run_driver(profile_manager.get_email(i), profile_manager.get_pass(i), False)
        # Mobile
        rewards, streak = initialize.run_driver(profile_manager.get_email(i), profile_manager.get_pass(i), True)

        profile_manager.set_reward(i, rewards)
        print('[DATA]', 'Reward updated')
        print(profile_manager.get_reward(i))

        profile_manager.set_streak(i, streak)
        print('[DATA]', 'Streak updated')
        print(profile_manager.get_streak(i))


if __name__ == '__main__':
    main()
