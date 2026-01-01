import json
import os
import re
from datetime import datetime


class DataStore:
    def __init__(self, users_file='users.json', cars_file='cars.json', comments_file='comments.json'):
        self.users_file = users_file
        self.cars_file = cars_file
        self.comments_file = comments_file

    def initialize_files(self):
        if not os.path.exists(self.users_file):
            default_users = {
                "admin": {
                    "password": "Admin@123",
                    "role": "admin",
                    "national_id": "0123456789",
                    "photo": "",
                    "cart": [],
                    "purchase_history": []
                }
            }
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(default_users, f, ensure_ascii=False, indent=4)

        if not os.path.exists(self.cars_file):
            with open(self.cars_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        if not os.path.exists(self.comments_file):
            with open(self.comments_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

    # Users
    def load_users(self):
        with open(self.users_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_users(self, users):
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

    # Cars
    def load_cars(self):
        with open(self.cars_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_cars(self, cars):
        with open(self.cars_file, 'w', encoding='utf-8') as f:
            json.dump(cars, f, ensure_ascii=False, indent=4)

    # Comments
    def load_comments(self):
        with open(self.comments_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_comments(self, comments):
        with open(self.comments_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=4)

    def validate_password(self, password):
        if len(password) < 8:
            return False, "رمز عبور باید حداقل 8 کاراکتر باشد"
        if not re.search(r'\d', password):
            return False, "رمز عبور باید شامل عدد باشد"
        if not re.search(r'[a-zA-Z]', password):
            return False, "رمز عبور باید شامل حروف باشد"
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            return False, "رمز عبور باید شامل کاراکتر خاص باشد"
        return True, "رمز عبور معتبر است"


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
