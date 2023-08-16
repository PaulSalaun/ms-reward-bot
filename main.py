from webdriver import initialize
from profils import profile_manager


def main():

    for i in range(0, profile_manager.get_len()):

        rewards, streak = initialize.daily_tasks(i, profile_manager.get_email(i), profile_manager.get_pass(i))

        profile_manager.set_reward(i, rewards)
        print('[DATA]', 'Reward updated', profile_manager.get_reward(i))
        profile_manager.set_streak(i, streak)
        print('[DATA]', 'Streak updated', profile_manager.get_streak(i))

        initialize.pc_search(profile_manager.get_email(i), profile_manager.get_pass(i))
        initialize.mobie_search(profile_manager.get_email(i), profile_manager.get_pass(i))


if __name__ == '__main__':
    main()
