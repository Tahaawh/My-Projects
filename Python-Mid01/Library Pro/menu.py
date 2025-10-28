def menu_start():
    print("\n=== Welcome to Smart Library ===")
    print("1 - Admin")
    print("2 - User Register/Login")
    print("0 - Exit")


def menu_admin():
    while True:
        print("\n--- Admin Menu ---")
        print("1 - Add a book")
        print("2 - Delete a book")
        print("3 - View registered users")
        print("4 - View logs")
        print("5 - View book inventory chart")
        print("6 - Send broadcast message")
        print("7 - Filter books by quantity")
        print("8 - Pin or Unpin a book")
        print("9 - Save books to Excel")
        print("10 - Show all user tickets")
        print("11 - Reset all library data ( ⚠️  testing only)")
        print("12 - Show all usernames and passwords (admin)")
        print("0 - Back")
        choice = input("Your choice: ").strip()
        if choice in [str(i) for i in range(13)]:
            return int(choice)
        print("Invalid input. Please enter a number from 0 to 12.")


def menu_authentication():
    while True:
        print("\n--- Authentication Menu ---")
        print("1 - Register")
        print("2 - Login")
        print("0 - Back")
        choice = input("Your choice: ").strip()
        if choice in ["1", "2", "0"]:
            return int(choice)
        print("Invalid input. Please enter 1, 2, or 0.")


def menu_user():
    while True:
        print("\n--- User Menu ---")
        print("1 - Show book list")
        print("2 - Buy a book")
        print("3 - Submit a ticket to admin")
        print("4 - Delete my account")
        print("5 - Suggest a book")
        print("6 - Log out")
        print("0 - Exit program")
        choice = input("Select an option (0-6): ").strip()
        if choice in [str(i) for i in range(7)]:
            return int(choice)
        print("Invalid input. Please enter a number from 0 to 6.")
