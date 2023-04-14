from webdriver import initialize
from profils import profile_manager

from prettytable import PrettyTable


def main():
    table = PrettyTable()
    table.field_names = ["Email", "Rewards"]

    result_table = []
    for i in range(0, profile_manager.get_len()):
        email = profile_manager.get_email(i)
        rewards = initialize.run_driver(profile_manager.get_email(i), profile_manager.get_pass(i))

        result_table.append((email, rewards))
        for row in result_table:
            table.add_row(row)
        print(table)


if __name__ == '__main__':
    main()
