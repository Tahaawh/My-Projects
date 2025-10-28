import re
import os
import json
import random
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from bs4 import BeautifulSoup


# json create
def jsonFile():
    try:
        with open("Users.json", "r") as myFile:
            pass
    except:
        with open("Users.json", "w") as myFile:
            json.dump({}, myFile)


# Log
def Log():
    try:
        with open("Log.txt", "r", encoding="utf-8") as myFile:
            print("Log file content:")
            for Logs in myFile:
                print(Logs.strip())
    except FileNotFoundError:
        print("Not founded any Log File !")


# Login DateTime
def Log_info(Username, action):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Log_line = f"{time} - {Username} - {action}\n"

    try:
        with open("Log.txt", "a", encoding="utf-8") as myFile:
            myFile.write(Log_line)
    except:
        print("Has a problem to Logging file.")


# new User
def register():
    Username = input("Choose a Username: ").strip()
    Password = input("Choose a Password: ").strip()

    try:
        with open("Users.json", "r") as myFile:
            content = myFile.read().strip()
            Users = json.loads(content) if content else {}
    except (FileNotFoundError, json.JSONDecodeError):
        Users = {}

    if Username in Users:
        print("Username already taken. Please choose a different username.")
        return None
    else:
        Users[Username] = Password
        with open("Users.json", "w") as myFile:
            json.dump(Users, myFile, indent=4)
        Log_info(Username, "registered")
        print("Registration successful.")
        return Username


# Login
def login():
    Username = input("Enter your Username: ").strip()

    try:
        with open("Users.json", "r") as myFile:
            Users = json.load(myFile)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No users found. Please register first.")
        return None

    if Username not in Users:
        print("Username not found.")
        return None

    Password = input("Enter your Password: ").strip()
    if Users[Username] == Password:
        print("WELCOME")
        return Username
    else:
        print("Password incorrect.")
        reset = input("Do you want to reset your password? (y/n): ").strip().lower()
        if reset == "y":
            reset_password(Username, Users)
            # Now prompt for password again after reset
            Password = input("Enter your new password to login: ").strip()
            if Users[Username] == Password:
                print("WELCOME")
                return Username
            else:
                print("Login failed with new password.")
                return None
        else:
            print("Login aborted.")
            return None


# reset password


def reset_password(username, users_dict):
    new_password = input("Enter new password: ").strip()
    users_dict[username] = new_password
    with open("Users.json", "w") as myFile:
        json.dump(users_dict, myFile, indent=4)
    print(f"Password reset successful for user '{username}'.")
    Log_info(username, "password reset")


# get the top selling books
def get_books():
    url = "https://en.wikipedia.org/wiki/List_of_best-selling_books"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "wikitable"})
    books = []
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) >= 5:
            title = cols[0].get_text(strip=True)
            author = cols[1].get_text(strip=True)
            genre = cols[5].get_text(strip=True) if len(cols) > 5 else "Unknown"
            books.append({"name": title, "author": author, "genre": genre})
    return books


# adding books
def add_books():
    scraped_books = get_books()
    print("\nTop Selling Books:")
    for i, book in enumerate(scraped_books[:10], start=1):
        print(f"{i}. {book['name']} - {book['author']}")

    choice = input(
        "\nSelect a book to add by number (or press Enter to skip): "
    ).strip()

    def get_positive_int(prompt):
        while True:
            val = input(prompt).strip()
            if val.isdigit() and int(val) > 0:
                return int(val)
            else:
                print("Please enter a valid positive number.")

    if choice.isdigit() and 1 <= int(choice) <= len(scraped_books[:10]):
        selected = scraped_books[int(choice) - 1]
        available_copies = get_positive_int("Enter available copies for this book: ")
        chapters = get_positive_int("Enter chapters: ")
        new_book = {
            "name": selected["name"],
            "author": selected["author"],
            "genre": selected.get("genre", ""),
            "available_copies": available_copies,
            "chapters": chapters,
        }
    elif choice == "":
        name = input("Enter book name: ").strip()
        author = input("Enter author name: ").strip()
        genre = input("Enter genre: ").strip()
        available_copies = get_positive_int("Available copies: ")
        chapters = get_positive_int("Enter chapters: ")
        new_book = {
            "name": name,
            "author": author,
            "genre": genre,
            "available_copies": available_copies,
            "chapters": chapters,
        }
    else:
        print("Invalid choice. Operation cancelled.")
        return

    # Load existing books
    if os.path.exists("books.json"):
        with open("books.json", "r", encoding="utf-8") as myFile:
            content = myFile.read().strip()
            books = json.loads(content) if content else []
    else:
        books = []

    books.append(new_book)

    # Save updated books to JSON
    with open("books.json", "w", encoding="utf-8") as myFile:
        json.dump(books, myFile, indent=4, ensure_ascii=False)

    # Save to Excel (optional)
    try:
        df = pd.DataFrame(books)
        df = df.sort_values(by="name")
        df.to_excel("books.xlsx", index=False)
    except Exception as e:
        print(f"Warning: Could not save to Excel. {e}")

    print("Book added successfully.")


# deleteing a book
def delete_book():
    if not os.path.exists("books.json"):
        print("No books found.")
        return

    with open("books.json", "r", encoding="utf-8") as file:
        content = file.read().strip()
        books = json.loads(content) if content else []

    if not books:
        print("No books to delete.")
        return

    print("\nBooks in Library:")
    for i, book in enumerate(books, start=1):
        print(f"{i}. {book.get('name', 'Unknown')} - {book.get('author', 'Unknown')}")

    choice = input(
        "\nEnter the number of the book to delete (or press Enter to cancel): "
    ).strip()

    if not choice.isdigit() or not (1 <= int(choice) <= len(books)):
        print("Invalid choice. No book deleted.")
        return

    removed = books.pop(int(choice) - 1)

    with open("books.json", "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)

    print(f"Book '{removed.get('name')}' deleted successfully.")


# chart
def draw_chart():
    try:
        with open("books.json", "r") as myFile:
            books = json.load(myFile)
    except FileNotFoundError:
        return "books file not found"
    names = [book["name"] for book in books]
    counts = [book.get("available_copies", 0) for book in books]
    plt.bar(names, counts, color="red")
    plt.style.use("ggplot")
    plt.xlabel("books")
    plt.ylabel("equity")
    plt.title("books equity chart")
    plt.xticks(rotation=45)
    plt.ylim(0, max(counts) + 10)
    plt.tight_layout()
    plt.show()


# Users list
def show_User():
    try:
        with open("Users.json", "r") as myFile:
            Users = json.load(myFile)
    except FileNotFoundError:
        print(" No Users have registered yet.")
        return

    if not Users:
        return " The User list is empty."

    print("Registered Users:")
    for Username in Users:
        print("-" + Username)


#


def add_message_by_admin(message):
    try:
        with open("broadcast.json", "r") as myFile:
            data = json.load(myFile)
    except FileNotFoundError:
        data = []

    data.append(
        {"message": message, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    )

    with open("broadcast.json", "w") as myFile:
        json.dump(data, myFile, indent=4)

    print("message sent")


#


def show_broadcast_messages():
    try:
        with open("broadcast.json", "r") as myFile:
            messages = json.load(myFile)
    except FileNotFoundError:
        return

    print("admins message :")
    for m in messages[-3:]:
        print(f"- {m['message']}  ({m['time']})")


#


# --- Buy Book ---
def buy_book():
    # Load books from JSON (source of truth)
    if not os.path.exists("books.json"):
        print("No books available.")
        return

    with open("books.json", "r") as file:
        books = json.load(file)

    if not books:
        print("No books available.")
        return

    print("Available Books:")
    for i, book in enumerate(books, 1):
        print(
            f"{i}. {book['name']} - {book['author']} - {book.get('available_copies', 0)} copies"
        )

    choice = input("Enter book name or number to buy: ").strip()

    # Find the selected book
    book = None
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(books):
            book = books[idx]
        else:
            print("Invalid book number.")
            return
    else:
        for b in books:
            if b["name"].lower() == choice.lower():
                book = b
                break
        if not book:
            print("Book not found.")
            return

    if book.get("available_copies", 0) > 0:
        book["available_copies"] -= 1
        print(
            f"Book purchased: {book['name']}. Remaining copies: {book['available_copies']}"
        )
    else:
        print("Out of stock.")
        return

    # Save updated books to JSON
    with open("books.json", "w") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)

    # Update Excel file
    try:
        df = pd.DataFrame(books)
        df = df.sort_values(by="name")
        df.to_excel("books.xlsx", index=False)
    except Exception as e:
        print(f"Warning: Could not save to Excel. {e}")


# --- Save Books to Excel ---
def save_books_to_excel():
    try:
        with open("books.json", "r") as file:
            books = json.load(file)
    except FileNotFoundError:
        print("books.json not found.")
        return

    df = pd.DataFrame(books)
    df.to_excel("books.xlsx", index=False)
    print("Saved to books.xlsx")


# --- Ticketing System ---
def submit_ticket(username=None):
    if username is None:
        username = input("Enter your username: ")
    message = input("Write your message => ")

    try:
        with open("tickets.json", "r") as file:
            content = file.read().strip()
            tickets = json.loads(content) if content else {}
            if not isinstance(tickets, dict):
                print("Warning: tickets.json corrupted, resetting tickets data.")
                tickets = {}
    except FileNotFoundError:
        tickets = {}

    if username not in tickets:
        tickets[username] = []

    tickets[username].append(
        {"message": message, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    )

    with open("tickets.json", "w") as file:
        json.dump(tickets, file, indent=4)

    print("Ticket sent to admin.")


# --- Delete Account ---
def delete_account():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    try:
        with open("Users.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        print("No user exists.")
        return

    if username in users and users[username] == password:
        users.pop(username)
        with open("Users.json", "w") as file:
            json.dump(users, file, indent=4)
        print("Account deleted successfully.")
    else:
        print("Username or password incorrect.")


# --- Suggest a Book ---
def suggest_book():
    try:
        with open("books.json", "r") as file:
            content = file.read().strip()
            books = json.loads(content) if content else []
    except FileNotFoundError:
        print("Book list not found.")
        return

    if not books:
        print("No books available to suggest.")
        return

    suggested = random.choice(books)
    print(f"Suggested book to read: \"{suggested['name']}\" by {suggested['author']}")


# --- Show Books with Multiple Chapters ---
def show_books_with_multiple_chapters():
    try:
        with open("books.json", "r") as file:
            books = json.load(file)
    except FileNotFoundError:
        print("books.json not found.")
        return

    for book in books:
        chapters = book.get("chapters")

        if isinstance(chapters, int):
            if chapters > 1:
                print(f"{book['name']} has {chapters} chapters")

        elif isinstance(chapters, list):
            if len(chapters) > 1:
                print(f"{book['name']} has {len(chapters)} chapters")

        elif isinstance(chapters, str):
            matches = re.findall(r"chapter", chapters.lower())
            if len(matches) > 1:
                print(f"{book['name']} has {len(matches)} chapters")


# --- Filter Books by Count ---
def filter_books_by_count():
    try:
        with open("books.json", "r") as file:
            books = json.load(file)
    except FileNotFoundError:
        print("books.json not found.")
        return

    while True:
        min_count = input("Enter minimum quantity: ").strip()
        if min_count.isdigit():
            min_count = int(min_count)
            break
        else:
            print("Please enter a valid positive integer.")

    for book in books:
        if book.get("available_copies", 0) >= min_count:
            print(f"{book['name']} - {book['available_copies']}")


#


def list_book_sorted():
    try:
        df = pd.read_excel("books.xlsx")
    except FileNotFoundError:
        print("books.xlsx not found.")
        return []

    if df.empty:
        print("No books available.")
        return []

    if "pinned" not in df.columns:
        df["pinned"] = False

    df = df.sort_values(by=["pinned", "name"], ascending=[False, True])

    print("\nAvailable Books:")
    for i, (_, row) in enumerate(df.iterrows(), 1):
        pin = "📌 " if row.get("pinned", False) else "   "
        print(
            f"{i}. {pin}{row['name']} - {row['author']} - {row['genre']} - {row['available_copies']} copies - {row['chapters']} chapters"
        )

    return df.to_dict(orient="records")


# --- Pin Book ---
# --- Pin or Unpin a Book ---
def pin_or_unpin_book():
    if not os.path.exists("books.json"):
        print("books.json not found.")
        return

    with open("books.json", "r", encoding="utf-8") as file:
        content = file.read().strip()
        books = json.loads(content) if content else []

    if not books:
        print("No books available.")
        return

    print("\nYour Book List:")
    for i, book in enumerate(books, start=1):
        pin_status = "📌" if book.get("pinned", False) else "   "
        print(f"{i}. {pin_status} {book['name']} - {book['author']}")

    choice = input(
        "\nEnter the number of the book to pin/unpin (or press Enter to cancel): "
    ).strip()

    if not choice.isdigit() or not (1 <= int(choice) <= len(books)):
        print("Invalid selection. Operation cancelled.")
        return

    index = int(choice) - 1
    books[index]["pinned"] = not books[index].get("pinned", False)

    with open("books.json", "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)

    # Also update Excel
    try:
        df = pd.DataFrame(books)
        df.to_excel("books.xlsx", index=False)
    except Exception as e:
        print(f"Warning: Could not update Excel. {e}")

    action = "Pinned" if books[index]["pinned"] else "Unpinned"
    print(f"{action} '{books[index]['name']}' successfully.")


# --- Save Books to Excel ---
def save_books_to_excel():
    try:
        with open("books.json", "r") as file:
            books = json.load(file)
    except FileNotFoundError:
        print("books.json not found.")
        return

    try:
        df = pd.DataFrame(books)
        df.to_excel("books.xlsx", index=False)
        print("Saved to books.xlsx")
    except Exception as e:
        print(f"Failed to save to Excel: {e}")


# --- Show All Tickets ---
def show_all_tickets():
    if not os.path.exists("tickets.json"):
        print("No tickets found.")
        return

    with open("tickets.json", "r") as file:
        content = file.read().strip()
        tickets = json.loads(content) if content else {}

    if not tickets:
        print("No tickets to display.")
        return

    print("\n--- All User Tickets ---")
    for username, msgs in tickets.items():
        print(f"\nUser: {username}")
        for msg in msgs:
            print(f"  - {msg['message']}  ({msg['time']})")


def reset_library_data():
    # Confirm before resetting
    confirm = (
        input("⚠️ Are you sure you want to reset all library data? (yes/no): ")
        .strip()
        .lower()
    )
    if confirm != "yes":
        print("Reset cancelled.")
        return

    # Files to reset (you can add/remove based on your project)
    files_to_clear = {
        "books.json": [],
        "Users.json": {},
        "Log.txt": "",
        "tickets.json": [],
        "messages.json": [],
    }

    for filename, empty_content in files_to_clear.items():
        try:
            with open(filename, "w", encoding="utf-8") as f:
                if filename.endswith(".json"):
                    json.dump(empty_content, f, indent=4, ensure_ascii=False)
                else:
                    f.write(empty_content)
            print(f"{filename} has been reset.")
        except Exception as e:
            print(f"Error resetting {filename}: {e}")

    print("✅ All library data has been reset.")
