import sys
import os
import json
import re
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

# ensure parent folder is on sys.path so backend.py can be imported when running
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend import DataStore

# تنظیمات اولیه CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class IranKhodroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # تنظیمات پنجره اصلی
        self.title("سیستم مدیریت ایران خودرو")
        self.geometry("1280x720")
        
        # مرکز کردن پنجره در صفحه
        self.update_idletasks()
        width = 1280
        height = 720
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # متغیرهای کاربری
        self.current_user = None
        self.users_file = "users.json"
        self.cars_file = "cars.json"
        self.comments_file = "comments.json"
        
        # backend datastore
        self.datastore = DataStore(self.users_file, self.cars_file, self.comments_file)
        self.datastore.initialize_files()

        # bind datastore methods for compatibility with existing code
        self.load_users = self.datastore.load_users
        self.save_users = self.datastore.save_users
        self.load_cars = self.datastore.load_cars
        self.save_cars = self.datastore.save_cars
        self.load_comments = self.datastore.load_comments
        self.save_comments = self.datastore.save_comments
        self.validate_password = self.datastore.validate_password
        
        # نمایش صفحه ورود
        self.show_login_page()
    
    def clear_window(self):
        """پاک کردن تمام ویجت‌های پنجره"""
        for widget in self.winfo_children():
            widget.destroy()
    
    
    # ==================== صفحه ورود ====================
    def show_login_page(self):
        """نمایش صفحه ورود"""
        self.clear_window()
        
        # فریم اصلی
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # عنوان
        title_label = ctk.CTkLabel(
            main_frame,
            text="خوش آمدید به سیستم ایران خودرو",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=30)
        
        # فریم ورود
        login_frame = ctk.CTkFrame(main_frame)
        login_frame.pack(pady=20)
        
        # نام کاربری / کد ملی
        ctk.CTkLabel(login_frame, text="نام کاربری / کد ملی:", font=ctk.CTkFont(size=14)).pack(pady=10)
        username_entry = ctk.CTkEntry(login_frame, width=300, placeholder_text="نام کاربری یا کد ملی")
        username_entry.pack(pady=5)
        
        # رمز عبور
        ctk.CTkLabel(login_frame, text="رمز عبور:", font=ctk.CTkFont(size=14)).pack(pady=10)
        password_entry = ctk.CTkEntry(login_frame, width=300, show="*", placeholder_text="رمز عبور")
        password_entry.pack(pady=5)
        
        # دکمه ورود
        def login():
            username = username_entry.get().strip()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("خطا", "لطفا تمام فیلدها را پر کنید")
                return
            
            users = self.load_users()
            
            # جستجو با username یا کد ملی
            user_found = None
            for uname, udata in users.items():
                if uname == username or udata.get('national_id') == username:
                    if udata['password'] == password:
                        user_found = (uname, udata)
                        break
            
            if user_found:
                self.current_user = {
                    'username': user_found[0],
                    'data': user_found[1]
                }
                messagebox.showinfo("موفق", f"خوش آمدید {user_found[0]}")
                
                if user_found[1]['role'] == 'admin':
                    self.show_admin_panel()
                else:
                    self.show_user_panel()
            else:
                messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است")
        
        ctk.CTkButton(
            login_frame,
            text="ورود",
            width=200,
            command=login,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=20)
        
        # دکمه ثبت نام
        ctk.CTkButton(
            login_frame,
            text="ثبت نام",
            width=200,
            command=self.show_register_page,
            fg_color="gray",
            font=ctk.CTkFont(size=14)
        ).pack(pady=5)

    # ==================== پنل ادمین ====================
    def show_admin_panel(self):
        """نمایش پنل ادمین"""
        self.clear_window()
        
        # فریم اصلی
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # هدر
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text=f"پنل مدیریت - خوش آمدید {self.current_user['username']}",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            header_frame,
            text="خروج",
            command=self.show_login_page,
            fg_color="red",
            width=100
        ).pack(side="right", padx=10)
        
        # منوی تب‌ها
        tabview = ctk.CTkTabview(main_frame)
        tabview.pack(expand=True, fill="both", padx=10, pady=10)
        
        # تب مدیریت ماشین‌ها
        tabview.add("مدیریت ماشین‌ها")
        # تب مدیریت کاربران
        tabview.add("مدیریت کاربران")
        
        self.setup_cars_management_tab(tabview.tab("مدیریت ماشین‌ها"))
        self.setup_users_management_tab(tabview.tab("مدیریت کاربران"))
    
    def setup_cars_management_tab(self, parent):
        """تنظیم تب مدیریت ماشین‌ها"""
        # دکمه اضافه کردن ماشین
        ctk.CTkButton(
            parent,
            text="➕ اضافه کردن ماشین جدید",
            command=self.add_car_dialog,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)
        
        # لیست ماشین‌ها
        cars_frame = ctk.CTkScrollableFrame(parent)
        cars_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.refresh_cars_list(cars_frame)
    
    def refresh_cars_list(self, parent):
        """به‌روزرسانی لیست ماشین‌ها"""
        for widget in parent.winfo_children():
            widget.destroy()
        
        cars = self.load_cars()
        
        if not cars:
            ctk.CTkLabel(parent, text="هیچ ماشینی ثبت نشده است", font=ctk.CTkFont(size=14)).pack(pady=20)
            return
        
        for idx, car in enumerate(cars):
            car_frame = ctk.CTkFrame(parent)
            car_frame.pack(fill="x", padx=10, pady=5)
            
            info_text = f"{car['name']} - {car['model']} - قیمت: {car['price']:,} تومان"
            ctk.CTkLabel(car_frame, text=info_text, font=ctk.CTkFont(size=13)).pack(side="left", padx=10)
            
            ctk.CTkButton(
                car_frame,
                text="🗑️ حذف",
                command=lambda i=idx: self.delete_car(i, parent),
                fg_color="red",
                width=80
            ).pack(side="right", padx=5)
    
    def add_car_dialog(self):
        """پنجره اضافه کردن ماشین"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("اضافه کردن ماشین")
        dialog.geometry("400x500")
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="نام ماشین:", font=ctk.CTkFont(size=12)).pack(pady=5)
        name_entry = ctk.CTkEntry(dialog, width=300)
        name_entry.pack(pady=5)
        
        ctk.CTkLabel(dialog, text="مدل:", font=ctk.CTkFont(size=12)).pack(pady=5)
        model_entry = ctk.CTkEntry(dialog, width=300)
        model_entry.pack(pady=5)
        
        ctk.CTkLabel(dialog, text="قیمت (تومان):", font=ctk.CTkFont(size=12)).pack(pady=5)
        price_entry = ctk.CTkEntry(dialog, width=300)
        price_entry.pack(pady=5)
        
        ctk.CTkLabel(dialog, text="توضیحات:", font=ctk.CTkFont(size=12)).pack(pady=5)
        description_entry = ctk.CTkTextbox(dialog, width=300, height=100)
        description_entry.pack(pady=5)
        
        def save_car():
            name = name_entry.get().strip()
            model = model_entry.get().strip()
            price = price_entry.get().strip()
            description = description_entry.get("1.0", "end").strip()
            
            if not all([name, model, price]):
                messagebox.showerror("خطا", "لطفا تمام فیلدها را پر کنید")
                return
            
            try:
                price = int(price)
            except ValueError:
                messagebox.showerror("خطا", "قیمت باید عدد باشد")
                return
            
            cars = self.load_cars()
            cars.append({
                "id": len(cars) + 1,
                "name": name,
                "model": model,
                "price": price,
                "description": description
            })
            self.save_cars(cars)
            
            messagebox.showinfo("موفق", "ماشین با موفقیت اضافه شد")
            dialog.destroy()
            self.show_admin_panel()
        
        ctk.CTkButton(dialog, text="ذخیره", command=save_car, width=200).pack(pady=20)
    
    def delete_car(self, index, parent):
        """حذف ماشین"""
        if messagebox.askyesno("تایید", "آیا مطمئن هستید؟"):
            cars = self.load_cars()
            del cars[index]
            self.save_cars(cars)
            self.refresh_cars_list(parent)
    
    def setup_users_management_tab(self, parent):
        """تنظیم تب مدیریت کاربران"""
        users_frame = ctk.CTkScrollableFrame(parent)
        users_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        users = self.load_users()
        
        for username, data in users.items():
            if username == "admin":
                continue
            
            user_frame = ctk.CTkFrame(users_frame)
            user_frame.pack(fill="x", padx=10, pady=5)
            
            info_text = f"👤 {username} - کد ملی: {data['national_id']} - نقش: {data['role']}"
            ctk.CTkLabel(user_frame, text=info_text, font=ctk.CTkFont(size=12)).pack(side="left", padx=10)
            
            ctk.CTkButton(
                user_frame,
                text="🗑️ حذف",
                command=lambda u=username: self.delete_user(u),
                fg_color="red",
                width=80
            ).pack(side="right", padx=5)
            
            ctk.CTkButton(
                user_frame,
                text="⭐ ارتقا",
                command=lambda u=username: self.promote_user(u),
                fg_color="green",
                width=80
            ).pack(side="right", padx=5)
    
    def delete_user(self, username):
        """حذف کاربر"""
        if messagebox.askyesno("تایید", f"آیا از حذف کاربر {username} مطمئن هستید؟"):
            users = self.load_users()
            del users[username]
            self.save_users(users)
            messagebox.showinfo("موفق", "کاربر حذف شد")
            self.show_admin_panel()
    
    def promote_user(self, username):
        """ارتقا کاربر"""
        users = self.load_users()
        users[username]['role'] = 'vip'
        self.save_users(users)
        messagebox.showinfo("موفق", f"کاربر {username} به VIP ارتقا یافت")
        self.show_admin_panel()
    
    # ==================== پنل کاربر ====================
    def show_user_panel(self):
        """نمایش پنل کاربر"""
        self.clear_window()
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # هدر
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text=f"خوش آمدید {self.current_user['username']}",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            header_frame,
            text="خروج",
            command=self.show_login_page,
            fg_color="red",
            width=100
        ).pack(side="right", padx=10)
        
        # منوی تب‌ها
        tabview = ctk.CTkTabview(main_frame)
        tabview.pack(expand=True, fill="both", padx=10, pady=10)
        
        tabview.add("خودروها")
        tabview.add("سبد خرید")
        tabview.add("پروفایل")
        
        self.setup_cars_tab(tabview.tab("خودروها"))
        self.setup_cart_tab(tabview.tab("سبد خرید"))
        self.setup_profile_tab(tabview.tab("پروفایل"))
    
    def setup_cars_tab(self, parent):
        """تنظیم تب خودروها"""
        cars_frame = ctk.CTkScrollableFrame(parent)
        cars_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        cars = self.load_cars()
        
        if not cars:
            ctk.CTkLabel(cars_frame, text="هیچ خودرویی موجود نیست", font=ctk.CTkFont(size=14)).pack(pady=20)
            return
        
        for car in cars:
            car_frame = ctk.CTkFrame(cars_frame)
            car_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(
                car_frame,
                text=f"{car['name']} - {car['model']}",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="w", padx=10, pady=5)
            
            ctk.CTkLabel(
                car_frame,
                text=f"قیمت: {car['price']:,} تومان",
                font=ctk.CTkFont(size=14)
            ).pack(anchor="w", padx=10)
            
            ctk.CTkLabel(
                car_frame,
                text=f"توضیحات: {car['description']}",
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w", padx=10, pady=5)
            
            button_frame = ctk.CTkFrame(car_frame, fg_color="transparent")
            button_frame.pack(fill="x", pady=5)
            
            ctk.CTkButton(
                button_frame,
                text="🛒 افزودن به سبد خرید",
                command=lambda c=car: self.add_to_cart(c),
                fg_color="green",
                width=180
            ).pack(side="left", padx=10)
            
            ctk.CTkButton(
                button_frame,
                text="💬 مشاهده کامنت‌ها",
                command=lambda c=car: self.show_comments(c),
                fg_color="blue",
                width=180
            ).pack(side="left", padx=10)
    
    def add_to_cart(self, car):
        """افزودن به سبد خرید"""
        users = self.load_users()
        users[self.current_user['username']]['cart'].append(car)
        self.save_users(users)
        self.current_user['data'] = users[self.current_user['username']]
        messagebox.showinfo("موفق", "خودرو به سبد خرید اضافه شد")
    
    def setup_cart_tab(self, parent):
        """تنظیم تب سبد خرید"""
        cart_frame = ctk.CTkScrollableFrame(parent)
        cart_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        cart = self.current_user['data']['cart']
        
        if not cart:
            ctk.CTkLabel(cart_frame, text="سبد خرید شما خالی است", font=ctk.CTkFont(size=14)).pack(pady=20)
            return
        
        total = 0
        for idx, car in enumerate(cart):
            car_frame = ctk.CTkFrame(cart_frame)
            car_frame.pack(fill="x", padx=10, pady=5)
            
            info = f"{car['name']} - {car['model']} - {car['price']:,} تومان"
            ctk.CTkLabel(car_frame, text=info, font=ctk.CTkFont(size=13)).pack(side="left", padx=10)
            
            ctk.CTkButton(
                car_frame,
                text="❌ حذف",
                command=lambda i=idx: self.remove_from_cart(i),
                fg_color="red",
                width=80
            ).pack(side="right", padx=5)
            
            total += car['price']
        
        ctk.CTkLabel(
            cart_frame,
            text=f"جمع کل: {total:,} تومان",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        ctk.CTkButton(
            cart_frame,
            text="💳 خرید",
            command=self.purchase_cart,
            fg_color="green",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)
    
    def remove_from_cart(self, index):
        """حذف از سبد خرید"""
        users = self.load_users()
        del users[self.current_user['username']]['cart'][index]
        self.save_users(users)
        self.current_user['data'] = users[self.current_user['username']]
        self.show_user_panel()
    
    def purchase_cart(self):
        """خرید سبد"""
        if messagebox.askyesno("تایید خرید", "آیا از خرید مطمئن هستید؟"):
            users = self.load_users()
            cart = users[self.current_user['username']]['cart']
            
            purchase = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "items": cart,
                "total": sum(car['price'] for car in cart)
            }
            
            users[self.current_user['username']]['purchase_history'].append(purchase)
            users[self.current_user['username']]['cart'] = []
            self.save_users(users)
            self.current_user['data'] = users[self.current_user['username']]
            
            messagebox.showinfo("موفق", "خرید با موفقیت انجام شد")
            self.show_user_panel()
    
    def setup_profile_tab(self, parent):
        """تنظیم تب پروفایل"""
        profile_frame = ctk.CTkScrollableFrame(parent)
        profile_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        user_data = self.current_user['data']
        
        ctk.CTkLabel(profile_frame, text="نام کاربری:", font=ctk.CTkFont(size=14)).pack(pady=5)
        ctk.CTkLabel(
            profile_frame,
            text=self.current_user['username'],
            font=ctk.CTkFont(size=13)
        ).pack(pady=5)
        
        ctk.CTkLabel(profile_frame, text="کد ملی:", font=ctk.CTkFont(size=14)).pack(pady=5)
        national_id_entry = ctk.CTkEntry(profile_frame, width=300)
        national_id_entry.insert(0, user_data['national_id'])
        national_id_entry.pack(pady=5)
        
        ctk.CTkLabel(profile_frame, text="رمز عبور جدید:", font=ctk.CTkFont(size=14)).pack(pady=5)
        password_entry = ctk.CTkEntry(profile_frame, width=300, show="*")
        password_entry.pack(pady=5)
        
        def save_profile():
            new_national_id = national_id_entry.get().strip()
            new_password = password_entry.get()
            
            users = self.load_users()
            
            if new_national_id:
                users[self.current_user['username']]['national_id'] = new_national_id
            
            if new_password:
                is_valid, msg = self.validate_password(new_password)
                if not is_valid:
                    messagebox.showerror("خطا", msg)
                    return
                users[self.current_user['username']]['password'] = new_password
            
            self.save_users(users)
            self.current_user['data'] = users[self.current_user['username']]
            messagebox.showinfo("موفق", "پروفایل با موفقیت به‌روزرسانی شد")
        
        ctk.CTkButton(
            profile_frame,
            text="💾 ذخیره تغییرات",
            command=save_profile,
            fg_color="green",
            width=200
        ).pack(pady=20)
        
        # نمایش تاریخچه خرید
        ctk.CTkLabel(
            profile_frame,
            text="تاریخچه خرید:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        history_frame = ctk.CTkScrollableFrame(profile_frame, height=200)
        history_frame.pack(fill="x", padx=10, pady=10)
        
        if user_data['purchase_history']:
            for purchase in user_data['purchase_history']:
                purchase_frame = ctk.CTkFrame(history_frame)
                purchase_frame.pack(fill="x", padx=5, pady=5)
                
                ctk.CTkLabel(
                    purchase_frame,
                    text=f"📅 {purchase['date']} - جمع: {purchase['total']:,} تومان",
                    font=ctk.CTkFont(size=12)
                ).pack(anchor="w", padx=10, pady=5)
        else:
            ctk.CTkLabel(
                history_frame,
                text="هیچ خریدی ثبت نشده است",
                font=ctk.CTkFont(size=12)
            ).pack(pady=10)
    
    # ==================== سیستم کامنت ====================
    def show_comments(self, car):
        """نمایش پنجره کامنت‌ها"""
        comments_window = ctk.CTkToplevel(self)
        comments_window.title(f"کامنت‌های {car['name']}")
        comments_window.geometry("700x600")
        comments_window.grab_set()
        
        # هدر
        header_frame = ctk.CTkFrame(comments_window)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text=f"💬 کامنت‌های {car['name']} - {car['model']}",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        # لیست کامنت‌ها
        comments_frame = ctk.CTkScrollableFrame(comments_window, height=350)
        comments_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_comments(comments_frame, car)
        
        # فرم اضافه کردن کامنت
        add_comment_frame = ctk.CTkFrame(comments_window)
        add_comment_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            add_comment_frame,
            text="کامنت جدید:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=10, pady=5)
        
        comment_entry = ctk.CTkTextbox(add_comment_frame, height=80)
        comment_entry.pack(fill="x", padx=10, pady=5)
        
        def add_comment():
            comment_text = comment_entry.get("1.0", "end").strip()
            
            if not comment_text:
                messagebox.showerror("خطا", "لطفا متن کامنت را وارد کنید")
                return
            
            comments = self.load_comments()
            car_id = str(car['id'])
            
            if car_id not in comments:
                comments[car_id] = []
            
            new_comment = {
                "id": len(comments[car_id]) + 1,
                "username": self.current_user['username'],
                "text": comment_text,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            comments[car_id].append(new_comment)
            self.save_comments(comments)
            
            comment_entry.delete("1.0", "end")
            self.refresh_comments(comments_frame, car)
            messagebox.showinfo("موفق", "کامنت با موفقیت ثبت شد")
        
        ctk.CTkButton(
            add_comment_frame,
            text="➕ ثبت کامنت",
            command=add_comment,
            fg_color="green",
            width=150
        ).pack(pady=10)
    
    def refresh_comments(self, parent, car):
        """به‌روزرسانی لیست کامنت‌ها"""
        for widget in parent.winfo_children():
            widget.destroy()
        
        comments = self.load_comments()
        car_id = str(car['id'])
        
        if car_id not in comments or not comments[car_id]:
            ctk.CTkLabel(
                parent,
                text="هنوز کامنتی ثبت نشده است",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return
        
        for comment in comments[car_id]:
            comment_frame = ctk.CTkFrame(parent)
            comment_frame.pack(fill="x", padx=10, pady=8)
            
            # هدر کامنت (نام کاربر و تاریخ)
            header = ctk.CTkFrame(comment_frame, fg_color="transparent")
            header.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(
                header,
                text=f"👤 {comment['username']}",
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(side="left")
            
            ctk.CTkLabel(
                header,
                text=f"📅 {comment['date']}",
                font=ctk.CTkFont(size=11),
                text_color="gray"
            ).pack(side="right")
            
            # متن کامنت
            ctk.CTkLabel(
                comment_frame,
                text=comment['text'],
                font=ctk.CTkFont(size=12),
                wraplength=600,
                justify="right"
            ).pack(anchor="w", padx=10, pady=5)
            
            # دکمه حذف (فقط برای صاحب کامنت)
            if comment['username'] == self.current_user['username']:
                ctk.CTkButton(
                    comment_frame,
                    text="🗑️ حذف",
                    command=lambda c=comment, cf=car: self.delete_comment(c, cf, parent),
                    fg_color="red",
                    width=80,
                    height=25
                ).pack(anchor="e", padx=10, pady=5)
    
    def delete_comment(self, comment, car, parent):
        """حذف کامنت"""
        if messagebox.askyesno("تایید", "آیا از حذف این کامنت مطمئن هستید؟"):
            comments = self.load_comments()
            car_id = str(car['id'])
            
            comments[car_id] = [c for c in comments[car_id] if c['id'] != comment['id']]
            self.save_comments(comments)
            
            self.refresh_comments(parent, car)
            messagebox.showinfo("موفق", "کامنت حذف شد")


if __name__ == "__main__":
    app = IranKhodroApp()
    app.mainloop()