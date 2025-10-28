

import re
import os
import json
import random
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from bs4 import BeautifulSoup


from typing import Any


def safe_json_load(filename: str, default: Any) -> Any:
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return default
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                print(f"Warning: {filename} is corrupted. Resetting to default.")
                with open(filename, "w", encoding="utf-8") as fw:
                    json.dump(default, fw, indent=4, ensure_ascii=False)
                return default
            if not isinstance(data, type(default)):
                print(f"Warning: {filename} corrupted, resetting.")
                with open(filename, "w", encoding="utf-8") as fw:
                    json.dump(default, fw, indent=4, ensure_ascii=False)
                return default
            return data
    except FileNotFoundError:
        return default
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return default


def jsonFile():
    
    if not os.path.exists("Users.json"):
        with open("Users.json", "w", encoding="utf-8") as myFile:
            json.dump({}, myFile)


def Log():
    
    try:
        with open("Log.txt", "r", encoding="utf-8") as myFile:
            print("Log file content:")
            for Logs in myFile:
                print(Logs.strip())
    except FileNotFoundError:
        print("No Log File found!")


def Log_info(Username: str, action: str):
    
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Log_line = f"{time} - {Username} - {action}\n"

    try:
        with open("Log.txt", "a", encoding="utf-8") as myFile:
            myFile.write(Log_line)
    except Exception:
        print("Has a problem to Logging file.")


def register():
    
    while True:
        Username = input("Choose a Username: ").strip()
        if not Username:
            print("Username cannot be empty.")
            continue
        break
    while True:
        Password = input("Choose a Password: ").strip()
        if not Password:
            print("Password cannot be empty.")
            continue
        break
    Users = safe_json_load("Users.json", {})
    if not isinstance(Users, dict):
        print("Users file was corrupted. Resetting to default user.")
        Users = {"001": "123"}
        with open("Users.json", "w", encoding="utf-8") as myFile:
            json.dump(Users, myFile, indent=4)
    if Username in Users:
        print("Username already taken. Please choose a different username.")
        return None
    else:
        Users[Username] = Password
        try:
            with open("Users.json", "w", encoding="utf-8") as myFile:
                json.dump(Users, myFile, indent=4)
        except Exception as e:
            print(f"Error saving user: {e}")
            return None
        Log_info(Username, "registered")
        print("Registration successful.")
        return Username


def login():
    
    Username = input("Enter your Username: ").strip()
    Users = safe_json_load("Users.json", {})
    if not Users:
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


def reset_password(username: str, users_dict: dict[str, str]):
    
    new_password = input("Enter new password: ").strip()
    users_dict[username] = new_password
    try:
        with open("Users.json", "w", encoding="utf-8") as myFile:
            json.dump(users_dict, myFile, indent=4)
        print(f"Password reset successful for user '{username}'.")
        Log_info(username, "password reset")
    except Exception as e:
        print(f"Error resetting password: {e}")


def get_books():
    
    url = "https://en.wikipedia.org/wiki/List_of_best-selling_books"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "wikitable"})
        books = []
        from bs4.element import Tag

        if table is not None and isinstance(table, Tag):
            for row in table.find_all("tr")[1:]:
                if not isinstance(row, Tag):
                    continue
                cols = row.find_all("td")
                if len(cols) >= 5:
                    title = cols[0].get_text(strip=True)
                    author = cols[1].get_text(strip=True)
                    genre = cols[5].get_text(strip=True) if len(cols) > 5 else "Unknown"
                    books.append({"name": title, "author": author, "genre": genre})
        else:
            print("Could not find the expected table on Wikipedia page.")
        return books
    except Exception as e:
        print(f"Error fetching books from Wikipedia: {e}")
        return []


def add_books():
    
    scraped_books = get_books()
    if scraped_books:
        print("\nTop Selling Books:")
        for i, book in enumerate(scraped_books[:10], start=1):
            print(f"{i}. {book['name']} - {book['author']}")
    else:
        print("No books fetched from Wikipedia.")
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

    books = safe_json_load("books.json", [])
    if "pinned" not in new_book:
        new_book["pinned"] = False
    books.append(new_book)
    try:
        with open("books.json", "w", encoding="utf-8") as myFile:
            json.dump(books, myFile, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving books: {e}")
        return

    try:
        df = pd.DataFrame(books)
        for col in [
            "name",
            "author",
            "genre",
            "available_copies",
            "chapters",
            "pinned",
        ]:
            if col not in df.columns:
                df[col] = None
        df = df.sort_values(by="name")
        df.to_excel("books.xlsx", index=False)
    except Exception as e:
        print(f"Warning: Could not save to Excel. {e}")
        return

    print("Book added successfully.")


def delete_book():
    
    books = safe_json_load("books.json", [])
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


def draw_chart():
    
    books = safe_json_load("books.json", [])
    if not books:
        print("books file not found")
        return
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


def show_User():
    
    Users = safe_json_load("Users.json", {})
    if not Users:
        print("No Users have registered yet.")
        return

    print("Registered Users:")
    for Username in Users:
        print("-" + Username)


def add_message_by_admin(message):
    
    data = safe_json_load("broadcast.json", [])
    data.append(
        {"message": message, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    )
    with open("broadcast.json", "w", encoding="utf-8") as myFile:
        json.dump(data, myFile, indent=4)
    print("message sent")


def show_broadcast_messages():
    
    messages = safe_json_load("broadcast.json", [])
    if not messages:
        print("No broadcast messages.")
        return
    print("admins message :")
    for m in messages[-3:]:
        print(f"- {m['message']}  ({m['time']})")


def buy_book():
    
    # Load books from JSON (source of truth)
    books = safe_json_load("books.json", [])
    if not books:
        print("No books available.")
        return

    print("Available Books:")
    for i, book in enumerate(books, 1):
        print(
            f"{i}. {book['name']} - {book['author']} - {book.get('available_copies', 0)} copies"
        )

    choice = input("Enter book name or number to buy: ")

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


# --- Save Books to Excel (Legacy) ---
def save_books_to_excel_legacy():
    
    books = safe_json_load("books.json", [])
    if not books:
        print("books.json not found or empty.")
        return
    df = pd.DataFrame(books)
    df.to_excel("books.xlsx", index=False)
    print("Saved to books.xlsx")


# --- Ticketing System ---
def submit_ticket(username=None):
    
    if username is None:
        username = input("Enter your username: ")
    message = input("Write your message => ")
    tickets = safe_json_load("tickets.json", {})
    if username not in tickets:
        tickets[username] = []
    tickets[username].append(
        {"message": message, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    )
    with open("tickets.json", "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)
    print("Ticket sent to admin.")


# --- Delete Account ---
def delete_account():
    
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    users = safe_json_load("Users.json", {})
    if not users:
        print("No user exists.")
        return
    if username in users and users[username] == password:
        users.pop(username)
        with open("Users.json", "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4)
        print("Account deleted successfully.")
    else:
        print("Username or password incorrect.")


# --- Suggest a Book ---
def suggest_book():
    
    books = safe_json_load("books.json", [])
    if not books:
        print("No books available to suggest.")
        return
    suggested = random.choice(books)
    print(f"Suggested book to read: \"{suggested['name']}\" by {suggested['author']}")


# --- Show Books with Multiple Chapters ---
def show_books_with_multiple_chapters():
    
    books = safe_json_load("books.json", [])
    if not books:
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
    
    books = safe_json_load("books.json", [])
    if not books:
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


import pandas as pd
import numpy as np
from typing import List, Dict, Any, Iterator


def list_book_sorted() -> List[Dict[str, Any]]:
    
    try:
        df: pd.DataFrame = pd.read_excel("books.xlsx")
    except FileNotFoundError:
        print("books.xlsx not found.")
        return []
    except Exception as e:
        print(f"Error reading books.xlsx: {e}")
        return []
    if df.empty:
        print("No books available.")
        return []
    if "pinned" not in df.columns:
        df["pinned"] = False
    df = df.sort_values(by=["pinned", "name"], ascending=[False, True])
    print("\nAvailable Books:")
    for i, (_, row) in enumerate(df.iterrows(), 1):
        row: pd.Series = row  # Explicit type annotation for static analysis
        pin: str = "📌 " if bool(row["pinned"]) else "   "
        name_val: Any = row["name"]
        name: str = (
            str(name_val)
            if isinstance(name_val, str) and pd.notna(name_val)
            else "Unknown"
        )
        author_val: Any = row["author"]
        author: str = (
            str(author_val)
            if isinstance(author_val, str) and pd.notna(author_val)
            else "Unknown"
        )
        genre_val: Any = row["genre"]
        genre: str = (
            str(genre_val)
            if isinstance(genre_val, str) and pd.notna(genre_val)
            else "Unknown"
        )
        copies_val: Any = row["available_copies"]
        available_copies: str = (
            str(copies_val)
            if (isinstance(copies_val, (int, float, str)) and pd.notna(copies_val))
            else "?"
        )
        chapters_val: Any = row["chapters"]
        chapters: str = (
            str(chapters_val)
            if (isinstance(chapters_val, (int, float, str)) and pd.notna(chapters_val))
            else "?"
        )
        print(
            f"{i}. {pin}{name} - {author} - {genre} - {available_copies} copies - {chapters} chapters"
        )
    # Convert DataFrame to List[Dict[str, Any]] with string keys
    records: List[Dict[str, Any]] = [
        dict((str(k), v) for k, v in row.items()) for _, row in df.iterrows()
    ]
    return records


# --- Pin Book ---
# --- Pin or Unpin a Book ---
def pin_or_unpin_book():
    
    books = safe_json_load("books.json", [])
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
    
    tickets = safe_json_load("tickets.json", {})
    if not tickets:
        print("No tickets to display.")
        return

    print("\n--- All User Tickets ---")
    for username, msgs in tickets.items():
        print(f"\nUser: {username}")
        for msg in msgs:
            print(f"  - {msg['message']}  ({msg['time']})")


def reset_library_data():
    
    print("\n--- Library Data Reset ---")
    print("1 - Delete all data files")
    print("2 - Re-create all data files (with default users)")
    print("0 - Cancel")
    step = input("Choose an option: ").strip()
    if step == "1":
        files_to_reset = [
            "books.json",
            "Users.json",
            "Log.txt",
            "tickets.json",
            "messages.json",
            "broadcast.json",
            "books.xlsx",
        ]
        for filename in files_to_reset:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"{filename} deleted.")
            except Exception as e:
                print(f"Error deleting {filename}: {e}")
        print("All data files deleted.")
    elif step == "2":
        # Re-create JSON and TXT files with empty content, and add ONLY default user 001/123
        json_files = {
            "books.json": [],
            "Users.json": {"001": "123"},
            "tickets.json": [],
            "messages.json": [],
            "broadcast.json": [],
        }
        for filename, empty_content in json_files.items():
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(empty_content, f, indent=4, ensure_ascii=False)
                print(f"{filename} created/reset.")
            except Exception as e:
                print(f"Error creating {filename}: {e}")
        # Re-create Log.txt as empty
        try:
            with open("Log.txt", "w", encoding="utf-8") as f:
                f.write("")
            print("Log.txt created/reset.")
        except Exception as e:
            print(f"Error creating Log.txt: {e}")
        # Re-create books.xlsx as empty Excel file with correct columns
        try:
            df = pd.DataFrame(
                columns=[
                    "name",
                    "author",
                    "genre",
                    "available_copies",
                    "chapters",
                    "pinned",
                ]
            )
            df.to_excel("books.xlsx", index=False)
            print("books.xlsx created/reset.")
        except Exception as e:
            print(f"Error creating books.xlsx: {e}")
        print("All library data files have been re-created. Default user: 001/123")
    else:
        print("Reset cancelled.")


# Show all users and passwords (admin only)
def show_all_users_and_passwords():
    
    users = safe_json_load("Users.json", {})
    if not users:
        print("No users found.")
        return
    print("\n--- User List (username : password) ---")
    for username, password in users.items():
        print(f"{username} : {password}")
    print("--- End of list ---")


def ensure_default_admin():
    
    users = safe_json_load("Users.json", {})
    if users != {"001": "123"}:
        users = {"001": "123"}
        with open("Users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
        print("Default admin user created: 001/123")
