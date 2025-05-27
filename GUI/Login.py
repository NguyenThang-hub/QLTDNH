import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import hashlib
from DAO.DatabaseOperation import *
from MenuApp import MenuApp
from register import open_register_window
from forget_password import open_forget_password_window
from PIL import Image

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
root.geometry("800x600")
root.resizable(False, False)

# === Chia giao diện thành 2 nửa: trái và phải ===
left_frame = ctk.CTkFrame(master=root, width=600, height=600, corner_radius=0)
left_frame.pack(side="left", fill="both", expand=False)

right_frame = ctk.CTkFrame(master=root, width=200, height=600, corner_radius=0)
right_frame.pack(side="right", fill="both", expand=False)

# === Ảnh hoặc nền bên trái ===
image = ctk.CTkImage(light_image=Image.open("asset/Chilling.png"), size=(600, 600))
image_label = ctk.CTkLabel(left_frame, image=image, text="")
image_label.pack(expand=True, fill="both")

# === Form đăng nhập bên phải ===
title = ctk.CTkLabel(right_frame, text="Đăng nhập", font=ctk.CTkFont(size=24, weight="bold"))
title.pack(pady=(60, 30))

entry_username = ctk.CTkEntry(right_frame, placeholder_text="Tên đăng nhập", width=250)
entry_username.bind("<Return>", lambda event: entry_password.focus())
entry_username.pack(padx= 15,pady=10)

entry_password = ctk.CTkEntry(right_frame, placeholder_text="Mật khẩu", show="*", width=250)
entry_password.bind("<Return>", lambda event: handle_login(entry_username, entry_password, root))
entry_password.pack(padx= 15, pady=10)

login_button = ctk.CTkButton(right_frame, text="Đăng nhập", width=200,
                             command=lambda: handle_login(entry_username, entry_password, root))
login_button.pack(padx=15, pady=(20, 10))

ctk.CTkButton(right_frame, text="Đăng ký", command=open_register_window, width=200).pack(padx=15, pady=10)
ctk.CTkButton(right_frame, text="Quên mật khẩu?", command=open_forget_password_window, width=200).pack(padx=15, pady=10)

# === Chạy ứng dụng ===
root.mainloop()