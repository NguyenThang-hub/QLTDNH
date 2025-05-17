import tkinter as tk
from tkinter import messagebox
import hashlib
from db import connect_db
from Menu import MenuApp

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login(entry_username, entry_password, root):
    username = entry_username.get().strip()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin.")
        return
    # thử kết nối database
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            hashed_pwd = hash_password(password)
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                           (username, hashed_pwd))
            result = cursor.fetchone()
            if result:
                messagebox.showinfo("Thành công", "Đăng nhập thành công!")
                root.destroy()
                menu_root = tk.Tk()
                # Truyền username đã kiểm tra
                MenuApp(menu_root, username)
                menu_root.mainloop()
            else:
                messagebox.showerror("Thất bại", "Sai tài khoản hoặc mật khẩu.")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    finally:
        if conn and conn.is_connected():
            conn.close()

# ===== Giao diện Login =====
root = tk.Tk()
root.title("Phục Vụ Đăng Nhập")
root.geometry("400x300")
root.resizable(False, False)
root.configure(bg="#f0f4f8")

tk.Label(root, text="Đăng nhập của Phục Vụ", font=("Helvetica", 16, "bold"), bg="#f0f4f8", fg="#333333").pack(pady=10)

tk.Label(root, text="Tên đăng nhập", font=("Helvetica", 12), bg="#f0f4f8").pack()
entry_username = tk.Entry(root, font=("Helvetica", 12))
entry_username.pack(pady=5)

tk.Label(root, text="Mật khẩu", font=("Helvetica", 12), bg="#f0f4f8").pack()
entry_password = tk.Entry(root, show="*", font=("Helvetica", 12))
entry_password.pack(pady=5)

tk.Button(root, text="Đăng nhập", command=lambda: login(entry_username, entry_password, root),
          font=("Helvetica", 12), bg="#34c759", fg="white", activebackground="#28a745").pack(pady=15)

root.mainloop()