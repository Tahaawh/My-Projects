"""
برنامه اصلی سیستم مدیریت ایران خودرو
تطبیق‌شده برای استفاده از CustomTkinter
"""

import customtkinter as ctk
from backend import DataStore
from auth_page import AuthPage
from admin_panel import AdminPanel
from user_panel import UserPanel


# ============================================================================
# تنظیمات تم و ظاهر برنامه
# ============================================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================================================
# کلاس اصلی برنامه
# ============================================================================

class IranKhodroApp(ctk.CTk):
    """برنامه اصلی سیستم مدیریت ایران خودرو"""
    
    # ثابت‌های پنجره
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    WINDOW_TITLE = "سیستم مدیریت ایران خودرو"
    
    def __init__(self):
        """مقداردهی اولیه برنامه"""
        super().__init__()
        
        self._setup_window()
        self._initialize_data()
        self._setup_pages()
        self._show_login_page()
    
    def _setup_window(self):
        """تنظیم پنجره اصلی"""
        self.title(self.WINDOW_TITLE)
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        
        # مرکز کردن پنجره در صفحه
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.WINDOW_WIDTH // 2)
        y = (self.winfo_screenheight() // 2) - (self.WINDOW_HEIGHT // 2)
        self.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}')
    
    def _initialize_data(self):
        """مقداردهی بانک داده و متغیرهای کاربری"""
        self.current_user = None
        
        self.datastore = DataStore()
        self.datastore.initialize_files()
    
    def _setup_pages(self):
        """ایجاد صفحات مختلف برنامه"""
        self.auth_page = AuthPage(self, self.datastore)
        self.admin_panel = AdminPanel(self, self.datastore)
        self.user_panel = UserPanel(self, self.datastore)
    
    # ============================================================================
    # متودهای مدیریت صفحات
    # ============================================================================
    
    def clear_window(self):
        """پاک کردن تمام ویجت‌های پنجره"""
        for widget in self.winfo_children():
            widget.destroy()
    
    def _show_login_page(self):
        """نمایش صفحه ورود"""
        self.current_user = None
        self.clear_window()
        self.auth_page.show_login(self)
    
    def show_login_page(self):
        """نمایش صفحه ورود (متود عمومی)"""
        self._show_login_page()
    
    def show_register_page(self):
        """نمایش صفحه ثبت‌نام"""
        self.clear_window()
        self.auth_page.show_register(self)
    
    def show_admin_panel(self):
        """نمایش پنل ادمین"""
        self.admin_panel.show(self)
    
    def show_user_panel(self):
        """نمایش پنل کاربر"""
        self.user_panel.show(self)
    
    def set_current_user(self, username, user_data):
        """
        تنظیم کاربر فعلی
        
        Args:
            username (str): نام کاربری
            user_data (dict): اطلاعات کاربر
        """
        self.current_user = {
            'username': username,
            'data': user_data
        }


# ============================================================================
# نقطه شروع برنامه
# ============================================================================

if __name__ == "__main__":
    app = IranKhodroApp()
    app.mainloop()