import customtkinter as ctk
from tkinter import messagebox
from DAO.DatabaseOperation import *
import hashlib
import re

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    # Regex kiểm tra định dạng email đơn giản
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def register_user(username, password, email):
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                           (username, hash_password(password), email))
            conn.commit()
            return True
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    finally:
        if conn and conn.is_connected():
            conn.close()
    return False

def open_register_window():
    window = ctk.CTkToplevel()
    window.title("Đăng ký")
    window.geometry("400x400")

    ctk.CTkLabel(window, text="Tạo tài khoản mới", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

    entry_username = ctk.CTkEntry(window, placeholder_text="Tên đăng nhập")
    entry_email = ctk.CTkEntry(window, placeholder_text="Email")
    entry_password = ctk.CTkEntry(window, placeholder_text="Mật khẩu", show="*")
    entry_confirm_password = ctk.CTkEntry(window, placeholder_text="Nhập lại mật khẩu", show="*")

    entry_username.pack(pady=7)
    entry_email.pack(pady=7)
    entry_password.pack(pady=7)
    entry_confirm_password.pack(pady=7)

    def register():
        username = entry_username.get().strip()
        email = entry_email.get().strip()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()

        if not username or not email or not password or not confirm_password:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        if not is_valid_email(email):
            messagebox.showwarning("Thông báo", "Email không hợp lệ.")
            return

        if password != confirm_password:
            messagebox.showwarning("Thông báo", "Mật khẩu không khớp.")
            return

        if register_user(username, password, email):
            messagebox.showinfo("Thành công", "Đăng ký thành công.")
            window.destroy()

    ctk.CTkButton(window, text="Đăng ký", command=register).pack(pady=20)
