from menu import *
from defs import *
import os
import time


def admin_login():
    password = input("Enter admin password: ")
    return password == "4321"


def main():
    jsonFile()  # Ensure user file exists

    while True:
        choice = menu_start()

        if choice == 0:
            print("Exiting system. Goodbye!")
            time.sleep(3)
            os.system("cls" if os.name == "nt" else "clear")
            break

        elif choice == 1:  # Admin
            if not admin_login():
                print("Admin authentication failed.")
                continue

            while True:
                admin_sel = menu_admin()
                if admin_sel == 0:
                    break
                elif admin_sel == 1:
                    add_books()
                elif admin_sel == 2:
                    delete_book()
                elif admin_sel == 3:
                    show_User()
                elif admin_sel == 4:
                    Log()
                elif admin_sel == 5:
                    draw_chart()
                elif admin_sel == 6:
                    msg = input("Send message to all: ")
                    add_message_by_admin(msg)
                elif admin_sel == 7:
                    filter_books_by_count()
                elif admin_sel == 8:
                    pin_or_unpin_book()
                elif admin_sel == 9:
                    save_books_to_excel()
                elif admin_sel == 10:
                    show_all_tickets()
                elif admin_sel == 11:
                    reset_library_data()

        elif choice == 2:  # User menu
            auth_sel = menu_authentication()

            if auth_sel == 1:  # Register
                register()

            elif auth_sel == 2:  # Login
                username = login()
                if not username:
                    print("Login failed.")
                    continue

                # After login
                suggest_book()
                show_broadcast_messages()

                while True:
                    user_sel = menu_user()
                    if user_sel == 0 or user_sel == 6:  # Exit or logout
                        print("Logging out...\n")
                        break
                    elif user_sel == 1:
                        list_book_sorted()
                    elif user_sel == 2:
                        buy_book()
                    elif user_sel == 3:
                        submit_ticket(username)
                    elif user_sel == 4:
                        delete_account()
                        break
                    elif user_sel == 5:
                        suggest_book()
                    else:
                        print("Invalid option.")

        else:
            print("Unknown choice, try again.")


if __name__ == "__main__":
    main()
