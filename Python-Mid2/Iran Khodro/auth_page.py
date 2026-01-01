"""صفحات احراز هویت (ورود و ثبت نام)"""

import customtkinter as ctk
from tkinter import messagebox


class AuthPage:
    """کلاس مدیریت صفحات احراز هویت"""
    
    def __init__(self, app, datastore):
        self.app = app
        self.datastore = datastore
    
    def show_login(self, parent):
        """نمایش صفحه ورود"""
        # فریم اصلی
        main_frame = ctk.CTkFrame(parent)
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
        ctk.CTkLabel(
            login_frame,
            text="نام کاربری / کد ملی:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=10)
        username_entry = ctk.CTkEntry(
            login_frame,
            width=300,
            placeholder_text="نام کاربری یا کد ملی"
        )
        username_entry.pack(pady=5)
        
        # رمز عبور
        ctk.CTkLabel(
            login_frame,
            text="رمز عبور:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=10)
        password_entry = ctk.CTkEntry(
            login_frame,
            width=300,
            show="*",
            placeholder_text="رمز عبور"
        )
        password_entry.pack(pady=5)
        
        # تابع ورود
        def login():
            username = username_entry.get().strip()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("خطا", "لطفا تمام فیلدها را پر کنید")
                return
            
            users = self.datastore.load_users()
            
            # جستجو با username یا کد ملی
            user_found = None
            for uname, udata in users.items():
                if uname == username or udata.get('national_id') == username:
                    if udata['password'] == password:
                        user_found = (uname, udata)
                        break
            
            if user_found:
                self.app.set_current_user(user_found[0], user_found[1])
                messagebox.showinfo("موفق", f"خوش آمدید {user_found[0]}")
                
                if user_found[1]['role'] == 'admin':
                    self.app.show_admin_panel()
                else:
                    self.app.show_user_panel()
            else:
                messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است")
        
        # دکمه ورود
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
            command=self.app.show_register_page,
            fg_color="gray",
            font=ctk.CTkFont(size=14)
        ).pack(pady=5)
    
    def show_register(self, parent):
        """نمایش صفحه ثبت نام"""
        main_frame = ctk.CTkFrame(parent)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="ثبت نام کاربر جدید",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=30)
        
        register_frame = ctk.CTkFrame(main_frame)
        register_frame.pack(pady=20)
        
        # نام کاربری
        ctk.CTkLabel(
            register_frame,
            text="نام کاربری:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=5)
        username_entry = ctk.CTkEntry(register_frame, width=300)
        username_entry.pack(pady=5)
        
        # کد ملی
        ctk.CTkLabel(
            register_frame,
            text="کد ملی (10 رقم):",
            font=ctk.CTkFont(size=14)
        ).pack(pady=5)
        national_id_entry = ctk.CTkEntry(register_frame, width=300)
        national_id_entry.pack(pady=5)
        
        # رمز عبور
        ctk.CTkLabel(
            register_frame,
            text="رمز عبور:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=5)
        password_entry = ctk.CTkEntry(register_frame, width=300, show="*")
        password_entry.pack(pady=5)
        
        # تکرار رمز عبور
        ctk.CTkLabel(
            register_frame,
            text="تکرار رمز عبور:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=5)
        confirm_password_entry = ctk.CTkEntry(register_frame, width=300, show="*")
        confirm_password_entry.pack(pady=5)
        
        def register():
            username = username_entry.get().strip()
            national_id = national_id_entry.get().strip()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            
            if not all([username, national_id, password, confirm_password]):
                messagebox.showerror("خطا", "لطفا تمام فیلدها را پر کنید")
                return
            
            if len(national_id) != 10 or not national_id.isdigit():
                messagebox.showerror("خطا", "کد ملی باید 10 رقم باشد")
                return
            
            if password != confirm_password:
                messagebox.showerror("خطا", "رمز عبور و تکرار آن یکسان نیستند")
                return
            
            is_valid, msg = self.datastore.validate_password(password)
            if not is_valid:
                messagebox.showerror("خطا", msg)
                return
            
            users = self.datastore.load_users()
            
            if username in users:
                messagebox.showerror("خطا", "این نام کاربری قبلا ثبت شده است")
                return
            
            users[username] = {
                "password": password,
                "role": "user",
                "national_id": national_id,
                "photo": "",
                "cart": [],
                "purchase_history": []
            }
            
            self.datastore.save_users(users)
            messagebox.showinfo("موفق", "ثبت نام با موفقیت انجام شد")
            self.app.show_login_page()
        
        ctk.CTkButton(
            register_frame,
            text="ثبت نام",
            width=200,
            command=register,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=20)
        
        ctk.CTkButton(
            register_frame,
            text="بازگشت به ورود",
            width=200,
            command=self.app.show_login_page,
            fg_color="gray"
        ).pack(pady=5)
