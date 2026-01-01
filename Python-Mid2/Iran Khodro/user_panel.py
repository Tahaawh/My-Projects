"""پنل کاربری"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from profile import ProfileTab


class UserPanel:
    """کلاس مدیریت پنل کاربری"""
    
    def __init__(self, app, datastore):
        self.app = app
        self.datastore = datastore
        self.profile_tab = ProfileTab(app, datastore)
    
    def show(self, parent):
        """نمایش پنل کاربر"""
        if self.app.current_user is None:
            messagebox.showerror("خطا", "ابتدا وارد شوید")
            self.app.show_login_page()
            return
        
        parent.clear_window()
        
        main_frame = ctk.CTkFrame(parent)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # هدر
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text=f"خوش آمدید {self.app.current_user['username']}",
            font=ctk.CTkFont(size=18, weight="bold")
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
        
        tabview.add("خودروها")
        tabview.add("سبد خرید")
        tabview.add("پروفایل")
        
        self._setup_cars_tab(tabview.tab("خودروها"))
        self._setup_cart_tab(tabview.tab("سبد خرید"))
        self.profile_tab.setup(tabview.tab("پروفایل"))
    
    def _setup_cars_tab(self, parent):
        """تنظیم تب خودروها"""
        cars_frame = ctk.CTkScrollableFrame(parent)
        cars_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        cars = self.datastore.load_cars()
        
        if not cars:
            ctk.CTkLabel(
                cars_frame,
                text="هیچ خودرویی موجود نیست",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
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
                command=lambda c=car: self._add_to_cart(c),
                fg_color="green",
                width=180
            ).pack(side="left", padx=10)
            
            ctk.CTkButton(
                button_frame,
                text="💬 مشاهده کامنت‌ها",
                command=lambda c=car: self._show_comments(c),
                fg_color="blue",
                width=180
            ).pack(side="left", padx=10)
    
    def _add_to_cart(self, car):
        """افزودن به سبد خرید"""
        if self.app.current_user is None:
            messagebox.showerror("خطا", "ابتدا وارد شوید")
            self.app.show_login_page()
            return
        
        users = self.datastore.load_users()
        users[self.app.current_user['username']]['cart'].append(car)
        self.datastore.save_users(users)
        self.app.current_user['data'] = users[self.app.current_user['username']]
        messagebox.showinfo("موفق", "خودرو به سبد خرید اضافه شد")
    
    def _setup_cart_tab(self, parent):
        """تنظیم تب سبد خرید"""
        if self.app.current_user is None:
            messagebox.showerror("خطا", "ابتدا وارد شوید")
            self.app.show_login_page()
            return
        
        cart_frame = ctk.CTkScrollableFrame(parent)
        cart_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        cart = self.app.current_user['data']['cart']
        
        if not cart:
            ctk.CTkLabel(
                cart_frame,
                text="سبد خرید شما خالی است",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return
        
        total = 0
        for idx, car in enumerate(cart):
            car_frame = ctk.CTkFrame(cart_frame)
            car_frame.pack(fill="x", padx=10, pady=5)
            
            info = f"{car['name']} - {car['model']} - {car['price']:,} تومان"
            ctk.CTkLabel(
                car_frame,
                text=info,
                font=ctk.CTkFont(size=13)
            ).pack(side="left", padx=10)
            
            ctk.CTkButton(
                car_frame,
                text="❌ حذف",
                command=lambda i=idx: self._remove_from_cart(i),
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
            command=self._purchase_cart,
            fg_color="green",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)
    
    def _remove_from_cart(self, index):
        """حذف از سبد خرید"""
        if self.app.current_user is None:
            messagebox.showerror("خطا", "ابتدا وارد شوید")
            self.app.show_login_page()
            return
        
        users = self.datastore.load_users()
        del users[self.app.current_user['username']]['cart'][index]
        self.datastore.save_users(users)
        self.app.current_user['data'] = users[self.app.current_user['username']]
        self.app.show_user_panel()
    
    def _purchase_cart(self):
        """خرید سبد"""
        if self.app.current_user is None:
            messagebox.showerror("خطا", "ابتدا وارد شوید")
            self.app.show_login_page()
            return
        
        if messagebox.askyesno("تایید خرید", "آیا از خرید مطمئن هستید؟"):
            users = self.datastore.load_users()
            cart = users[self.app.current_user['username']]['cart']
            
            purchase = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "items": cart,
                "total": sum(car['price'] for car in cart)
            }
            
            users[self.app.current_user['username']]['purchase_history'].append(purchase)
            users[self.app.current_user['username']]['cart'] = []
            self.datastore.save_users(users)
            self.app.current_user['data'] = users[self.app.current_user['username']]
            
            messagebox.showinfo("موفق", "خرید با موفقیت انجام شد")
            self.app.show_user_panel()
    
    def _show_comments(self, car):
        """نمایش پنجره کامنت‌ها"""
        if self.app.current_user is None:
            messagebox.showerror("خطا", "ابتدا وارد شوید")
            self.app.show_login_page()
            return
        
        comments_window = ctk.CTkToplevel(self.app)
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
        
        self._refresh_comments(comments_frame, car)
        
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
            if self.app.current_user is None:
                messagebox.showerror("خطا", "ابتدا وارد شوید")
                return
            
            comment_text = comment_entry.get("1.0", "end").strip()
            
            if not comment_text:
                messagebox.showerror("خطا", "لطفا متن کامنت را وارد کنید")
                return
            
            comments = self.datastore.load_comments()
            car_id = str(car['id'])
            
            if car_id not in comments:
                comments[car_id] = []
            
            new_comment = {
                "id": len(comments[car_id]) + 1,
                "username": self.app.current_user['username'],
                "text": comment_text,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            comments[car_id].append(new_comment)
            self.datastore.save_comments(comments)
            
            comment_entry.delete("1.0", "end")
            self._refresh_comments(comments_frame, car)
            messagebox.showinfo("موفق", "کامنت با موفقیت ثبت شد")
        
        ctk.CTkButton(
            add_comment_frame,
            text="➕ ثبت کامنت",
            command=add_comment,
            fg_color="green",
            width=150
        ).pack(pady=10)
    
    def _refresh_comments(self, parent, car):
        """به‌روزرسانی لیست کامنت‌ها"""
        if self.app.current_user is None:
            return
        
        for widget in parent.winfo_children():
            widget.destroy()
        
        comments = self.datastore.load_comments()
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
            if comment['username'] == self.app.current_user['username']:
                ctk.CTkButton(
                    comment_frame,
                    text="🗑️ حذف",
                    command=lambda c=comment: self._delete_comment(c, car, parent),
                    fg_color="red",
                    width=80,
                    height=25
                ).pack(anchor="e", padx=10, pady=5)
    
    def _delete_comment(self, comment, car, parent):
        """حذف کامنت"""
        if self.app.current_user is None:
            messagebox.showerror("خطا", "ابتدا وارد شوید")
            return
        
        if messagebox.askyesno("تایید", "آیا از حذف این کامنت مطمئن هستید؟"):
            comments = self.datastore.load_comments()
            car_id = str(car['id'])
            
            comments[car_id] = [c for c in comments[car_id] if c['id'] != comment['id']]
            self.datastore.save_comments(comments)
            
            self._refresh_comments(parent, car)
            messagebox.showinfo("موفق", "کامنت حذف شد")
