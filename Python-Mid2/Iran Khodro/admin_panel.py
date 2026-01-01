"""پنل مدیریت (ادمین)"""

import customtkinter as ctk
from tkinter import messagebox


class AdminPanel:
    """کلاس مدیریت پنل ادمین"""
    
    def __init__(self, app, datastore):
        self.app = app
        self.datastore = datastore
    
    def show(self, parent):
        """نمایش پنل ادمین"""
        if self.app.current_user is None:
            messagebox.showerror("خطا", "ابتدا وارد شوید")
            self.app.show_login_page()
            return
        
        parent.clear_window()
        
        # فریم اصلی
        main_frame = ctk.CTkFrame(parent)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # هدر
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text=f"پنل مدیریت - خوش آمدید {self.app.current_user['username']}",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            header_frame,
            text="خروج",
            command=self.app.show_login_page,
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
        
        self._setup_cars_management_tab(tabview.tab("مدیریت ماشین‌ها"))
        self._setup_users_management_tab(tabview.tab("مدیریت کاربران"))
    
    def _setup_cars_management_tab(self, parent):
        """تنظیم تب مدیریت ماشین‌ها"""
        # دکمه اضافه کردن ماشین
        ctk.CTkButton(
            parent,
            text="➕ اضافه کردن ماشین جدید",
            command=self._add_car_dialog,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)
        
        # لیست ماشین‌ها
        cars_frame = ctk.CTkScrollableFrame(parent)
        cars_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        self._refresh_cars_list(cars_frame)
    
    def _refresh_cars_list(self, parent):
        """به‌روزرسانی لیست ماشین‌ها"""
        for widget in parent.winfo_children():
            widget.destroy()
        
        cars = self.datastore.load_cars()
        
        if not cars:
            ctk.CTkLabel(
                parent,
                text="هیچ ماشینی ثبت نشده است",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return
        
        for idx, car in enumerate(cars):
            car_frame = ctk.CTkFrame(parent)
            car_frame.pack(fill="x", padx=10, pady=5)
            
            info_text = f"{car['name']} - {car['model']} - قیمت: {car['price']:,} تومان"
            ctk.CTkLabel(
                car_frame,
                text=info_text,
                font=ctk.CTkFont(size=13)
            ).pack(side="left", padx=10)
            
            ctk.CTkButton(
                car_frame,
                text="🗑️ حذف",
                command=lambda i=idx: self._delete_car(i, parent),
                fg_color="red",
                width=80
            ).pack(side="right", padx=5)
    
    def _add_car_dialog(self):
        """پنجره اضافه کردن ماشین"""
        dialog = ctk.CTkToplevel(self.app)
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
            
            cars = self.datastore.load_cars()
            cars.append({
                "id": len(cars) + 1,
                "name": name,
                "model": model,
                "price": price,
                "description": description
            })
            self.datastore.save_cars(cars)
            
            messagebox.showinfo("موفق", "ماشین با موفقیت اضافه شد")
            dialog.destroy()
            self.app.show_admin_panel()
        
        ctk.CTkButton(dialog, text="ذخیره", command=save_car, width=200).pack(pady=20)
    
    def _delete_car(self, index, parent):
        """حذف ماشین"""
        if messagebox.askyesno("تایید", "آیا مطمئن هستید؟"):
            cars = self.datastore.load_cars()
            del cars[index]
            self.datastore.save_cars(cars)
            self._refresh_cars_list(parent)
    
    def _setup_users_management_tab(self, parent):
        """تنظیم تب مدیریت کاربران"""
        users_frame = ctk.CTkScrollableFrame(parent)
        users_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        users = self.datastore.load_users()
        
        for username, data in users.items():
            if username == "admin":
                continue
            
            user_frame = ctk.CTkFrame(users_frame)
            user_frame.pack(fill="x", padx=10, pady=5)
            
            info_text = f"👤 {username} - کد ملی: {data['national_id']} - نقش: {data['role']}"
            ctk.CTkLabel(
                user_frame,
                text=info_text,
                font=ctk.CTkFont(size=12)
            ).pack(side="left", padx=10)
            
            ctk.CTkButton(
                user_frame,
                text="🗑️ حذف",
                command=lambda u=username: self._delete_user(u),
                fg_color="red",
                width=80
            ).pack(side="right", padx=5)
            
            ctk.CTkButton(
                user_frame,
                text="⭐ ارتقا",
                command=lambda u=username: self._promote_user(u),
                fg_color="green",
                width=80
            ).pack(side="right", padx=5)
    
    def _delete_user(self, username):
        """حذف کاربر"""
        if messagebox.askyesno("تایید", f"آیا از حذف کاربر {username} مطمئن هستید؟"):
            users = self.datastore.load_users()
            del users[username]
            self.datastore.save_users(users)
            messagebox.showinfo("موفق", "کاربر حذف شد")
            self.app.show_admin_panel()
    
    def _promote_user(self, username):
        """ارتقا کاربر"""
        users = self.datastore.load_users()
        users[username]['role'] = 'vip'
        self.datastore.save_users(users)
        messagebox.showinfo("موفق", f"کاربر {username} به VIP ارتقا یافت")
        self.app.show_admin_panel()
