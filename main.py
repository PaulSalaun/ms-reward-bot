from webdriver import initialize
from profils import profile_manager

if __name__ == '__main__':

    for i in range(0, profile_manager.get_len()):

        initialize.run_driver(profile_manager.get_email(i), profile_manager.get_pass(i))




