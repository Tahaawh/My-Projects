from menu import *
from defs import *

import os
import time
from typing import Optional


def admin_login():

    password = input("Enter admin password: ").strip()
    return password == "4321"


def test_menu():
    import time

    os.system("cls")
    tests = [
        ("Reset all data", "Reset all data", lambda: run_all_tests(single="reset")),
        ("Register user", "Register user", lambda: run_all_tests(single="register")),
        (
            "Register duplicate user",
            "Register duplicate user",
            lambda: run_all_tests(single="register_duplicate"),
        ),
        (
            "Login with wrong password",
            "Login with wrong password",
            lambda: run_all_tests(single="login_wrong"),
        ),
        (
            "Login with reset password",
            "Login with reset password",
            lambda: run_all_tests(single="login_reset"),
        ),
        (
            "Add book from Wikipedia",
            "Add book from Wikipedia",
            lambda: run_all_tests(single="add_book_wiki"),
        ),
        (
            "Add book manually",
            "Add book manually",
            lambda: run_all_tests(single="add_book_manual"),
        ),
        ("List books", "List books", lambda: run_all_tests(single="list_books")),
        (
            "Buy a book (valid)",
            "Buy a book (valid)",
            lambda: run_all_tests(single="buy_book_valid"),
        ),
        (
            "Buy a book (out of stock)",
            "Buy a book (out of stock)",
            lambda: run_all_tests(single="buy_book_out"),
        ),
        (
            "Submit ticket",
            "Submit ticket",
            lambda: run_all_tests(single="submit_ticket"),
        ),
        (
            "Show all tickets",
            "Show all tickets",
            lambda: run_all_tests(single="show_tickets"),
        ),
        ("Pin a book", "Pin a book", lambda: run_all_tests(single="pin_book")),
        (
            "Save books to Excel",
            "Save books to Excel",
            lambda: run_all_tests(single="save_excel"),
        ),
        (
            "Suggest a book",
            "Suggest a book",
            lambda: run_all_tests(single="suggest_book"),
        ),
        (
            "Filter books by count",
            "Filter books by count",
            lambda: run_all_tests(single="filter_books"),
        ),
        ("Show users", "Show users", lambda: run_all_tests(single="show_users")),
        ("Show log file", "Show log file", lambda: run_all_tests(single="show_log")),
        ("Draw chart", "Draw chart", lambda: run_all_tests(single="draw_chart")),
        (
            "Send broadcast message",
            "Send broadcast message",
            lambda: run_all_tests(single="broadcast"),
        ),
        (
            "Show broadcast messages",
            "Show broadcast messages",
            lambda: run_all_tests(single="show_broadcast"),
        ),
        (
            "Show books with multiple chapters",
            "Show books with multiple chapters",
            lambda: run_all_tests(single="show_chapters"),
        ),
        (
            "Delete account",
            "Delete account",
            lambda: run_all_tests(single="delete_account"),
        ),
    ]
    print("\n--- Library Quick Test ---\n")
    for i, (en, desc, _) in enumerate(tests, 1):
        print(f"{i}. {desc} ({en})")
    print(f"a. Run all tests (auto)")
    print(f"0. Back to main menu")
    choice = input("Test number, a, or 0: ").strip().lower()
    os.system("cls")
    if choice == "0":
        return
    elif choice == "a":
        for en, desc, func in tests:
            print(f"\n[Auto] {desc} ({en}):")
            func()
            time.sleep(2)
        input("\nAll tests completed. Enter ...")
    elif choice.isdigit() and 1 <= int(choice) <= len(tests):
        en, desc, func = tests[int(choice) - 1]
        print(f"[Single Test] {desc} ({en}):")
        func()
        input("\nTest finished. Enter ...")
    else:
        print("Invalid input!")
        time.sleep(1)


def main():
    os.system("cls")
    jsonFile()

    users = safe_json_load("Users.json", {})
    if "001" not in users:
        users["001"] = "123"
        with open("Users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
    while True:
        try:
            os.system("cls")
            menu_start()
            user_input = input("Your choice: ").strip()
            if user_input.lower() == "t":
                test_menu()
                continue
            if user_input == "0":
                print("Exiting system.")
                time.sleep(1)
                print("Exiting system. Goodbye.")
                time.sleep(1)
                print("Exiting system. Goodbye!")
                time.sleep(1)
                os.system("cls")
                break
            elif user_input == "1":
                os.system("cls")
                if not admin_login():
                    print("Admin authentication failed.")
                    input("\nPress Enter to continue...")
                    continue
                while True:
                    try:
                        os.system("cls")
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
                        elif admin_sel == 12:
                            show_all_users_and_passwords()
                        else:
                            print("Unknown admin option.")
                        input("\nPress Enter to continue...")
                    except Exception as e:
                        print(f"[Admin Menu Error] {e}")
                        input("\nPress Enter to continue...")
            elif user_input == "2":
                os.system("cls")
                auth_sel = menu_authentication()
                if auth_sel == 1:
                    register()
                    input("\nPress Enter to continue...")
                elif auth_sel == 2:
                    username = login()
                    if not username:
                        print("Login failed.")
                        input("\nPress Enter to continue...")
                        continue
                    suggest_book()
                    show_broadcast_messages()
                    while True:
                        try:
                            os.system("cls")
                            user_sel = menu_user()
                            if user_sel == 0 or user_sel == 6:
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
                            input("\nPress Enter to continue...")
                        except Exception as e:
                            print(f"[User Menu Error] {e}")
                            input("\nPress Enter to continue...")
                else:
                    print("Unknown authentication option.")
                    input("\nPress Enter to continue...")
            else:
                print("Unknown choice, try again.")
                input("\nPress Enter to continue...")
        except Exception as e:
            print(f"[Main Menu Error] {e}")
            input("\nPress Enter to continue...")


def run_all_tests(single: Optional[str] = None):

    def test_reset():
        print("\n[TEST] Resetting all data...")
        try:
            import builtins

            input_backup = builtins.input
            builtins.input = lambda prompt="": "yes"
            reset_library_data()
            builtins.input = input_backup
        except Exception as e:
            print(f"[TEST] Error resetting data: {e}")

    def test_register():
        print("[TEST] Registering user 'testuser'...")
        try:
            import builtins

            input_backup = builtins.input
            inputs = iter(["testuser", "testpass"])
            builtins.input = lambda prompt="": next(inputs)
            register()
            builtins.input = input_backup
        except Exception as e:
            print(f"[TEST] Error registering user: {e}")

    def test_register_duplicate():
        print("[TEST] Registering duplicate user 'testuser'...")
        try:
            import builtins

            input_backup = builtins.input
            inputs = iter(["testuser", "testpass"])
            builtins.input = lambda prompt="": next(inputs)
            register()
            builtins.input = input_backup
        except Exception as e:
            print(f"[TEST] Error registering duplicate user: {e}")

    def test_login_wrong():
        print("[TEST] Logging in with wrong password...")
        try:
            import builtins

            input_backup = builtins.input
            inputs = iter(["testuser", "wrongpass", "n"])
            builtins.input = lambda prompt="": next(inputs)
            login()
            builtins.input = input_backup
        except Exception as e:
            print(f"[TEST] Error login wrong password: {e}")

    def test_login_reset():
        print("[TEST] Logging in with reset password...")
        try:
            import builtins

            input_backup = builtins.input
            inputs = iter(["testuser", "wrongpass", "y", "testpass", "testpass"])
            builtins.input = lambda prompt="": next(inputs)
            login()
            builtins.input = input_backup
        except Exception as e:
            print(f"[TEST] Error login with reset password: {e}")

    def test_add_book_wiki():
        print("[TEST] Adding a book from Wikipedia (or manual if fetch fails)...")
        try:
            import builtins

            input_backup = builtins.input
            inputs = iter(["1", "5", "3"])
            builtins.input = lambda prompt="": next(inputs)
            add_books()
            builtins.input = input_backup
        except Exception as e:
            print(f"[TEST] Error adding book from Wikipedia: {e}")

    def test_add_book_manual():
        print("[TEST] Adding a book manually...")
        try:
            import builtins

            input_backup = builtins.input
            inputs = iter(
                ["", "Manual Book", "Manual Author", "Manual Genre", "2", "2"]
            )
            builtins.input = lambda prompt="": next(inputs)
            add_books()
            builtins.input = input_backup
        except Exception as e:
            print(f"[TEST] Error adding book manually: {e}")

    def test_list_books():
        print("[TEST] Listing books...")
        try:
            list_book_sorted()
        except Exception as e:
            print(f"[TEST] Error listing books: {e}")

    def test_buy_book_valid():
        print("[TEST] Buying a book (valid)...")
        try:
            import builtins

            input_backup = builtins.input
            inputs = iter(["1"])
            builtins.input = lambda prompt="": next(inputs)
            buy_book()
            builtins.input = input_backup
        except Exception as e:
            print(f"[TEST] Error buying book: {e}")

    def test_buy_book_out():
        print("[TEST] Buying a book (out of stock)...")
        try:
            import builtins

            input_backup = builtins.input
            inputs = iter(["1"])
            builtins.input = lambda prompt="": next(inputs)
            buy_book()
            builtins.input = input_backup
        except Exception as e:
            print(f"[TEST] Error buying out of stock: {e}")

    def test_submit_ticket():
        print("[TEST] Submitting a ticket...")
        try:
            import builtins

            input_backup = builtins.input
            inputs = iter(["testuser", "This is a test ticket."])
            builtins.input = lambda prompt="": next(inputs)
            submit_ticket()
            builtins.input = input_backup
        except Exception as e:
            print(f"[TEST] Error submitting ticket: {e}")

    def test_show_tickets():
        print("[TEST] Showing all tickets...")
        try:
            show_all_tickets()
        except Exception as e:
            print(f"[TEST] Error showing tickets: {e}")

    def test_pin_book():
        print("[TEST] Pinning a book...")
        try:
            import builtins

            input_backup = builtins.input
            inputs = iter(["1"])
            builtins.input = lambda prompt="": next(inputs)
            pin_or_unpin_book()
            builtins.input = input_backup
        except Exception as e:
            print(f"[TEST] Error pinning book: {e}")

    def test_save_excel():
        print("[TEST] Saving books to Excel...")
        try:
            save_books_to_excel()
        except Exception as e:
            print(f"[TEST] Error saving to Excel: {e}")

    def test_suggest_book():
        print("[TEST] Suggesting a book...")
        try:
            suggest_book()
        except Exception as e:
            print(f"[TEST] Error suggesting book: {e}")

    def test_filter_books():
        print("[TEST] Filtering books by count...")
        try:
            import builtins

            input_backup = builtins.input
            inputs = iter(["1"])
            builtins.input = lambda prompt="": next(inputs)
            filter_books_by_count()
            builtins.input = input_backup
        except Exception as e:
            print(f"[TEST] Error filtering books: {e}")

    def test_show_users():
        print("[TEST] Showing users...")
        try:
            show_User()
        except Exception as e:
            print(f"[TEST] Error showing users: {e}")

    def test_show_log():
        print("[TEST] Showing log file...")
        try:
            Log()
        except Exception as e:
            print(f"[TEST] Error showing log: {e}")

    def test_draw_chart():
        print("[TEST] Drawing chart...")
        try:
            draw_chart()
        except Exception as e:
            print(f"[TEST] Error drawing chart: {e}")

    def test_broadcast():
        print("[TEST] Sending broadcast message...")
        try:
            import builtins

            input_backup = builtins.input
            inputs = iter(["Test broadcast message"])
            builtins.input = lambda prompt="": next(inputs)
            add_message_by_admin(input())
            builtins.input = input_backup
        except Exception as e:
            print(f"[TEST] Error sending broadcast: {e}")

    def test_show_broadcast():
        print("[TEST] Showing broadcast messages...")
        try:
            show_broadcast_messages()
        except Exception as e:
            print(f"[TEST] Error showing broadcast: {e}")

    def test_show_chapters():
        print("[TEST] Showing books with multiple chapters...")
        try:
            show_books_with_multiple_chapters()
        except Exception as e:
            print(f"[TEST] Error showing books with multiple chapters: {e}")

    def test_delete_account():
        print("[TEST] Deleting account...")
        try:
            import builtins

            input_backup = builtins.input
            inputs = iter(["testuser", "testpass"])
            builtins.input = lambda prompt="": next(inputs)
            delete_account()
            builtins.input = input_backup
        except Exception as e:
            print(f"[TEST] Error deleting account: {e}")

    tests = {
        "reset": test_reset,
        "register": test_register,
        "register_duplicate": test_register_duplicate,
        "login_wrong": test_login_wrong,
        "login_reset": test_login_reset,
        "add_book_wiki": test_add_book_wiki,
        "add_book_manual": test_add_book_manual,
        "list_books": test_list_books,
        "buy_book_valid": test_buy_book_valid,
        "buy_book_out": test_buy_book_out,
        "submit_ticket": test_submit_ticket,
        "show_tickets": test_show_tickets,
        "pin_book": test_pin_book,
        "save_excel": test_save_excel,
        "suggest_book": test_suggest_book,
        "filter_books": test_filter_books,
        "show_users": test_show_users,
        "show_log": test_show_log,
        "draw_chart": test_draw_chart,
        "broadcast": test_broadcast,
        "show_broadcast": test_show_broadcast,
        "show_chapters": test_show_chapters,
        "delete_account": test_delete_account,
    }
    if single:
        if single in tests:
            tests[single]()
        else:
            print("No such test.")
        return

    for func in tests.values():
        func()
    print("[TEST] All tests completed.\n")


if __name__ == "__main__":
    main()
