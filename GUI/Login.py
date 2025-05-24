import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import hashlib
from DAO.DatabaseOperation import *
from MenuApp import MenuApp

# === Hàm hash và kiểm tra đăng nhập ===
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                           (username, hash_password(password)))
            return cursor.fetchone()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    finally:
        if conn and conn.is_connected():
            conn.close()
    return None

def handle_login(entry_username, entry_password, root):
    username = entry_username.get().strip()
    password = entry_password.get()
    if not username or not password:
        messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin.")
        return
    if check_credentials(username, password):
        messagebox.showinfo("Thành công", "Đăng nhập thành công!")
        root.destroy()
        menu_root = tk.Tk()
        MenuApp(menu_root, username)
        menu_root.mainloop()
    else:
        messagebox.showerror("Thất bại", "Sai tài khoản hoặc mật khẩu.")

# === Cài đặt theme và giao diện ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Phục Vụ Đăng Nhập")
root.geometry("500x350")
root.resizable(False, False)

# === Frame trung tâm ===
frame = ctk.CTkFrame(master=root, width=500, height=400, corner_radius=20)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# === Các widget ===
title = ctk.CTkLabel(frame, text="Đăng nhập", font=ctk.CTkFont(size=18, weight="bold"))
title.pack(pady=(20, 10))

entry_username = ctk.CTkEntry(frame, placeholder_text="Tên đăng nhập", width=200)
entry_username.pack(padx = 10, pady=10)

entry_password = ctk.CTkEntry(frame, placeholder_text="Mật khẩu", show="*", width=200)
entry_password.pack(padx = 10,pady=10)

login_button = ctk.CTkButton(frame, text="Đăng nhập", width=150,
                                 command=lambda: handle_login(entry_username, entry_password, root))
login_button.pack(pady=(15, 10))

# === Chạy ứng dụng ===
root.mainloop()
