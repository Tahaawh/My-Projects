"""
ماژول بانک داده (DataStore)
مدیریت فایل‌های JSON و اعتبارسنجی داده‌ها
"""

import json
import os
import re
from datetime import datetime


# ============================================================================
# ثابت‌ها
# ============================================================================

DEFAULT_USERS = {
    "admin": {
        "password": "Admin@123",
        "role": "admin",
        "national_id": "0123456789",
        "photo": "",
        "cart": [],
        "purchase_history": []
    }
}


# ============================================================================
# کلاس بانک داده
# ============================================================================

class DataStore:
    """کلاس مدیریت بانک داده"""
    
    def __init__(self, users_file='users.json', cars_file='cars.json', comments_file='comments.json'):
        """
        مقداردهی اولیه DataStore
        
        Args:
            users_file (str): نام فایل کاربران
            cars_file (str): نام فایل خودروها
            comments_file (str): نام فایل کامنت‌ها
        """
        self.users_file = users_file
        self.cars_file = cars_file
        self.comments_file = comments_file

    def initialize_files(self):
        """ایجاد فایل‌های JSON در صورت عدم وجود"""
        # مقداردهی فایل کاربران
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_USERS, f, ensure_ascii=False, indent=4)

        # مقداردهی فایل خودروها
        if not os.path.exists(self.cars_file):
            with open(self.cars_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        # مقداردهی فایل کامنت‌ها
        if not os.path.exists(self.comments_file):
            with open(self.comments_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

    # ============================================================================
    # عملیات کاربران
    # ============================================================================

    def load_users(self):
        """
        بارگزاری داده‌های کاربران از فایل
        
        Returns:
            dict: دیکشنری کاربران
        """
        with open(self.users_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_users(self, users):
        """
        ذخیره داده‌های کاربران در فایل
        
        Args:
            users (dict): دیکشنری کاربران
        """
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

    # ============================================================================
    # عملیات خودروها
    # ============================================================================

    def load_cars(self):
        """
        بارگزاری داده‌های خودروها از فایل
        
        Returns:
            list: لیست خودروها
        """
        with open(self.cars_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_cars(self, cars):
        """
        ذخیره داده‌های خودروها در فایل
        
        Args:
            cars (list): لیست خودروها
        """
        with open(self.cars_file, 'w', encoding='utf-8') as f:
            json.dump(cars, f, ensure_ascii=False, indent=4)

    # ============================================================================
    # عملیات کامنت‌ها
    # ============================================================================

    def load_comments(self):
        """
        بارگزاری داده‌های کامنت‌ها از فایل
        
        Returns:
            dict: دیکشنری کامنت‌ها
        """
        with open(self.comments_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_comments(self, comments):
        """
        ذخیره داده‌های کامنت‌ها در فایل
        
        Args:
            comments (dict): دیکشنری کامنت‌ها
        """
        with open(self.comments_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=4)

    # ============================================================================
    # اعتبارسنجی
    # ============================================================================

    def validate_password(self, password):
        """
        اعتبارسنجی رمز عبور
        
        شرایط:
        - حداقل 8 کاراکتر
        - شامل حداقل یک رقم
        - شامل حداقل یک حرف انگلیسی
        - شامل حداقل یک کاراکتر خاص
        
        Args:
            password (str): رمز عبور برای اعتبارسنجی
        
        Returns:
            tuple: (is_valid, message)
        """
        # بررسی طول
        if len(password) < 8:
            return False, "رمز عبور باید حداقل 8 کاراکتر باشد"
        
        # بررسی وجود رقم
        if not re.search(r'\d', password):
            return False, "رمز عبور باید شامل عدد باشد"
        
        # بررسی وجود حرف انگلیسی
        if not re.search(r'[a-zA-Z]', password):
            return False, "رمز عبور باید شامل حروف باشد"
        
        # بررسی وجود کاراکتر خاص
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            return False, "رمز عبور باید شامل کاراکتر خاص باشد"
        
        return True, "رمز عبور معتبر است"


# ============================================================================
# توابع کمکی
# ============================================================================

def now_str():
    """
    بازگرداندن زمان فعلی به شکل رشته
    
    Returns:
        str: زمان فعلی در فرمت YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
