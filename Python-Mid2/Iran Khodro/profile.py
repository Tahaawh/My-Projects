"""
ماژول تب پروفایل کاربر
مدیریت اطلاعات پروفایل، عکس، و تاریخچه خریدها
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
try:
    from PIL import Image
except ImportError:
    Image = None
import os
import shutil


class ProfileTab:
    """کلاس مدیریت تب پروفایل"""
    
    def __init__(self, app, datastore):
        """
        مقداردهی اولیه
        
        Args:
            app: برنامه اصلی
            datastore: بانک داده
        """
        self.app = app
        self.datastore = datastore
        self.profile_image_label = None
        self.selected_photo_path = None
        self.profile_photos_dir = "profile_photos"
        
        # ایجاد پوشه عکس‌های پروفایل
        if not os.path.exists(self.profile_photos_dir):
            try:
                os.makedirs(self.profile_photos_dir)
            except Exception as e:
                print(f"خطا در ایجاد پوشه: {e}")
    
    def setup(self, parent):
        """تنظیم تب پروفایل"""
        if not self.app.current_user:
            return
        
        profile_frame = ctk.CTkScrollableFrame(parent)
        profile_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        user_data = self.app.current_user['data']
        
        # ============================================================================
        # بخش عکس پروفایل
        # ============================================================================
        
        photo_frame = ctk.CTkFrame(profile_frame, fg_color="#2b2b2b")
        photo_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            photo_frame,
            text="📸 عکس پروفایل",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15)
        
        
        # نمایش عکس
        photo_display_frame = ctk.CTkFrame(photo_frame, width=200, height=200, fg_color="#1a1a1a")
        photo_display_frame.pack(pady=10)
        photo_display_frame.pack_propagate(False)
        
        self.profile_image_label = ctk.CTkLabel(photo_display_frame, text="")
        self.profile_image_label.pack(expand=True)
        
        # بارگذاری عکس فعلی
        self.load_profile_photo(user_data.get('photo', ''))
        
        # دکمه انتخاب عکس
        ctk.CTkButton(
            photo_frame,
            text="📁 انتخاب عکس",
            command=self.select_photo,
            width=200,
            height=40,
            fg_color="#1976d2",
            hover_color="#0d47a1",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)
        
        # بخش اطلاعات کاربری
        info_frame = ctk.CTkFrame(profile_frame, fg_color="#2b2b2b")
        info_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="👤 اطلاعات کاربری",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15, padx=20)
        
        # نام کاربری (غیرقابل تغییر)
        username_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        username_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            username_frame,
            text="نام کاربری:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkLabel(
            username_frame,
            text=self.app.current_user['username'],
            font=ctk.CTkFont(size=14),
            text_color="#66bb6a"
        ).pack(side="left")
        
        ctk.CTkLabel(
            username_frame,
            text="(غیرقابل تغییر)",
            font=ctk.CTkFont(size=11),
            text_color="gray60"
        ).pack(side="left", padx=5)
        
        # نقش کاربر
        role_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        role_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            role_frame,
            text="نقش:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10)
        
        role = user_data.get('role', 'user')
        role_color = "#ff9800" if role == 'vip' else "#2196f3"
        role_text = "⭐ VIP" if role == 'vip' else "👤 کاربر عادی"
        
        ctk.CTkLabel(
            role_frame,
            text=role_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=role_color
        ).pack(side="left")
        
        # کد ملی
        ctk.CTkLabel(
            info_frame,
            text="کد ملی:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=8, padx=20, anchor="w")
        
        national_id_entry = ctk.CTkEntry(
            info_frame,
            width=400,
            height=40,
            font=ctk.CTkFont(size=13)
        )
        national_id_entry.insert(0, user_data['national_id'])
        national_id_entry.pack(pady=5, padx=20)
        
        # رمز عبور جدید
        ctk.CTkLabel(
            info_frame,
            text="رمز عبور جدید (در صورت تمایل به تغییر):",
            font=ctk.CTkFont(size=14)
        ).pack(pady=8, padx=20, anchor="w")
        
        password_entry = ctk.CTkEntry(
            info_frame,
            width=400,
            height=40,
            show="*",
            placeholder_text="رمز عبور جدید",
            font=ctk.CTkFont(size=13)
        )
        password_entry.pack(pady=5, padx=20)
        
        def save_profile():
            if not self.app.current_user:
                return
            
            new_national_id = national_id_entry.get().strip()
            new_password = password_entry.get()
            
            users = self.datastore.load_users()
            username = self.app.current_user['username']
            
            # ذخیره عکس
            if self.selected_photo_path:
                try:
                    file_ext = os.path.splitext(self.selected_photo_path)[1]
                    new_photo_path = os.path.join(self.profile_photos_dir, f"{username}{file_ext}")
                    
                    shutil.copy2(self.selected_photo_path, new_photo_path)
                    users[username]['photo'] = new_photo_path
                except Exception as e:
                    messagebox.showerror("خطا", f"خطا در ذخیره عکس: {str(e)}")
                    return
            
            # ذخیره کد ملی
            if new_national_id:
                users[username]['national_id'] = new_national_id
            
            # ذخیره رمز عبور
            if new_password:
                is_valid, msg = self.datastore.validate_password(new_password)
                if not is_valid:
                    messagebox.showerror("خطا", msg)
                    return
                users[username]['password'] = new_password
            
            self.datastore.save_users(users)
            self.app.current_user['data'] = users[username]
            
            messagebox.showinfo("موفق", "✅ پروفایل با موفقیت به‌روزرسانی شد")
            self.app.show_user_panel()
        
        ctk.CTkButton(
            info_frame,
            text="💾 ذخیره تغییرات",
            command=save_profile,
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            width=250,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=25)
        
        # بخش تاریخچه خرید
        history_frame = ctk.CTkFrame(profile_frame, fg_color="#2b2b2b")
        history_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            history_frame,
            text="📋 تاریخچه خرید",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15, padx=20)
        
        purchases_frame = ctk.CTkScrollableFrame(history_frame, height=250)
        purchases_frame.pack(fill="x", padx=20, pady=10)
        
        if user_data['purchase_history']:
            for idx, purchase in enumerate(user_data['purchase_history'], 1):
                purchase_frame = ctk.CTkFrame(purchases_frame, fg_color="#1a1a1a")
                purchase_frame.pack(fill="x", padx=10, pady=8)
                
                header = ctk.CTkFrame(purchase_frame, fg_color="transparent")
                header.pack(fill="x", padx=15, pady=10)
                
                ctk.CTkLabel(
                    header,
                    text=f"🛒 خرید #{idx}",
                    font=ctk.CTkFont(size=14, weight="bold")
                ).pack(side="left")
                
                ctk.CTkLabel(
                    header,
                    text=f"📅 {purchase['date']}",
                    font=ctk.CTkFont(size=12),
                    text_color="gray60"
                ).pack(side="right")
                
                # لیست آیتم‌ها
                items_text = ", ".join([f"{item['name']}" for item in purchase['items']])
                ctk.CTkLabel(
                    purchase_frame,
                    text=f"📦 {items_text}",
                    font=ctk.CTkFont(size=12),
                    wraplength=700
                ).pack(anchor="w", padx=15, pady=5)
                
                ctk.CTkLabel(
                    purchase_frame,
                    text=f"💰 مبلغ کل: {purchase['total']:,} تومان",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color="#66bb6a"
                ).pack(anchor="w", padx=15, pady=8)
        else:
            ctk.CTkLabel(
                purchases_frame,
                text="هیچ خریدی ثبت نشده است",
                font=ctk.CTkFont(size=14),
                text_color="gray60"
            ).pack(pady=30)
    
    def load_profile_photo(self, photo_path):
        """بارگذاری و نمایش عکس پروفایل"""
        if self.profile_image_label is None:
            return
        
        try:
            if photo_path and os.path.exists(photo_path):
                if Image is None:
                    raise ImportError("PIL/Pillow نصب نیست")
                
                img = Image.open(photo_path)
                img = img.resize((180, 180), Image.Resampling.LANCZOS)
                
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(180, 180))
                self.profile_image_label.configure(image=photo, text="")
                self.profile_image_label._image = photo
            else:
                # عکس پیش‌فرض
                self.profile_image_label.configure(
                    text="👤\n\nعکس پروفایل",
                    font=ctk.CTkFont(size=40),
                    text_color="gray60"
                )
        except Exception as e:
            self.profile_image_label.configure(
                text="❌\n\nخطا در بارگذاری",
                font=ctk.CTkFont(size=14),
                text_color="red"
            )
            print(f"خطا در بارگذاری عکس: {e}")
    
    def select_photo(self):
        """انتخاب عکس از کامپیوتر"""
        if Image is None:
            messagebox.showerror("خطا", "PIL/Pillow نصب نیست. لطفا اجرا کنید:\npip install Pillow")
            return
        
        file_types = [
            ("تصاویر", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("تمام فایل‌ها", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="انتخاب عکس پروفایل",
            filetypes=file_types
        )
        
        if file_path:
            try:
                # بررسی فرمت عکس
                img = Image.open(file_path)
                # بررسی اعتبار عکس با بارگذاری کامل
                img.load()
                
                # نمایش پیش‌نمایش
                self.selected_photo_path = file_path
                self.load_profile_photo(file_path)
                
                messagebox.showinfo(
                    "موفق",
                    "عکس انتخاب شد. برای ذخیره دکمه 'ذخیره تغییرات' را بزنید"
                )
            except Exception as e:
                messagebox.showerror(
                    "خطا",
                    f"فایل انتخاب شده معتبر نیست\n{str(e)}"
                )