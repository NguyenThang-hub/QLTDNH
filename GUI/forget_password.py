import customtkinter as ctk
from tkinter import messagebox
import smtplib
import random
import hashlib
from config import EMAIL_ADDRESS, EMAIL_PASSWORD
from DAO.DatabaseOperation import *
from otp_store import save_otp, load_otp, delete_otp

def send_otp(email, username):
    otp_code = str(random.randint(100000, 999999))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            message = f"Subject: Mã OTP đổi mật khẩu\n\nMã OTP của bạn là: {otp_code}"
            smtp.sendmail(EMAIL_ADDRESS, email, message.encode('utf-8'))
            save_otp(username, otp_code)
        return True
    except Exception as e:
        messagebox.showerror("Lỗi gửi email", str(e))
        return False

def update_password(username, new_password):
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            hashed = hashlib.sha256(new_password.encode()).hexdigest()
            cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed, username))
            conn.commit()
            return True
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    finally:
        if conn and conn.is_connected():
            conn.close()
    return False

def open_forget_password_window():
    window = ctk.CTkToplevel()
    window.title("Quên mật khẩu")
    window.geometry("600x500")

    ctk.CTkLabel(window, text="Khôi phục mật khẩu", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

    entry_username = ctk.CTkEntry(window, placeholder_text="Tên đăng nhập")
    entry_email = ctk.CTkEntry(window, placeholder_text="Email")
    entry_otp = ctk.CTkEntry(window, placeholder_text="Mã OTP")
    entry_new_password = ctk.CTkEntry(window, placeholder_text="Mật khẩu mới", show="*")

    entry_username.pack(pady=5)
    entry_email.pack(pady=5)

    def verify_user_and_send_otp():
        username = entry_username.get().strip()
        email = entry_email.get().strip()

        if not username or not email:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        # Kiểm tra tồn tại người dùng + email đúng
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT email FROM users WHERE username = %s", (username,))
                result = cursor.fetchone()
                if result and result[0] == email:
                    if send_otp(email, username):
                        messagebox.showinfo("Thành công", "Đã gửi OTP, hãy kiểm tra email.")
                        entry_otp.pack(pady=5)
                        entry_new_password.pack(pady=5)
                        btn_reset.pack(pady=10)
                else:
                    messagebox.showerror("Lỗi", "Tên đăng nhập hoặc email không đúng.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            if conn and conn.is_connected():
                conn.close()

    def reset_password():
        username = entry_username.get().strip()
        entered_otp = entry_otp.get().strip()
        new_password = entry_new_password.get()

        otp_data = load_otp()

        if otp_data.get("username") != username or otp_data.get("otp") != entered_otp:
            messagebox.showerror("Sai OTP", "Mã OTP không đúng hoặc hết hạn.")
            return

        if update_password(username, new_password):
            delete_otp()
            messagebox.showinfo("Thành công", "Đổi mật khẩu thành công.")
            window.destroy()

    ctk.CTkButton(window, text="Gửi OTP", command=verify_user_and_send_otp).pack(pady=10)
    btn_reset = ctk.CTkButton(window, text="Đặt lại mật khẩu", command=reset_password)
