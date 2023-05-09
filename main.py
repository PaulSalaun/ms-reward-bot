import pdb

from webdriver import initialize
from profils import profile_manager

from prettytable import PrettyTable


def main():
    table = PrettyTable()
    table.field_names = ["Email", "Rewards"]

    # Set start time
    profile_manager.time_started()
    # Set all task to False
    profile_manager.tasks_false()

    for i in range(0, profile_manager.get_len()):
        # Computer
        initialize.run_driver(i, profile_manager.get_email(i), profile_manager.get_pass(i), False)
        # Mobile
        rewards, streak = initialize.run_driver(i, profile_manager.get_email(i), profile_manager.get_pass(i), True)

        profile_manager.set_reward(i, rewards)
        print('[DATA]', 'Reward updated', profile_manager.get_reward(i))

        profile_manager.set_streak(i, streak)
        print('[DATA]', 'Streak updated', profile_manager.get_streak(i))

    profile_manager.time_ended()


if __name__ == '__main__':
    main()

