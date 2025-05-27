import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random
import string
import qrcode
from PIL import Image, ImageTk

class QRCode:
    def __init__(self, parent, order_id, username, total_price, card_button, qr_button, cash_button):
        self.parent = parent
        self.order_id = order_id
        self.username = username
        self.total_price = total_price
        self.card_button = card_button
        self.qr_button = qr_button
        self.cash_button = cash_button
        self.show_qr_window()

    def show_qr_window(self):
        qr_window = tk.Toplevel(self.parent)
        qr_window.title("Thanh Toán QR")
        qr_window.geometry("600x800")
        qr_window.configure(bg="#f0f4f8")

        ttk.Label(
            qr_window,
            text="Quét Mã QR Để Thanh Toán",
            font=("Helvetica", 16, "bold"),
            foreground="#2c3e50",
            background="#f0f4f8"
        ).pack(pady=(10, 5))

        # Tạo mã QR thực tế
        qr_data = f"Payment: {self.order_id}, {self.username}, {self.total_price:,.0f} VNĐ"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_photo = ImageTk.PhotoImage(qr_img)
        qr_label = ttk.Label(qr_window, image=qr_photo)
        qr_label.pack(pady=20)
        qr_window.qr_photo = qr_photo  # Giữ tham chiếu để tránh garbage collection

        # Hiển thị thông tin thanh toán
        ttk.Label(
            qr_window,
            text=f"Mã đơn hàng: #{self.order_id}\nSố tiền: {self.total_price:,.0f} VNĐ",
            font=("Helvetica", 12),
            foreground="#333333",
            background="#f0f4f8"
        ).pack(pady=10)

        def confirm_payment():
            messagebox.showinfo("Thanh Toán", "Thanh toán bằng QR đã được xác nhận!")
            with open(f"payment_{self.order_id}.txt", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {self.username}: Paid {self.total_price:,.0f} VNĐ via QR\n")
            self.card_button.configure(state="disabled")
            self.qr_button.configure(state="disabled")
            self.cash_button.configure(state="disabled")
            qr_window.destroy()

        ttk.Button(
            qr_window,
            text="Xác Nhận Thanh Toán",
            command=confirm_payment,
            style="TButton"
        ).pack(pady=10)

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=6)
        style.map("TButton",
                  background=[("active", "#45a049")],
                  foreground=[("active", "#ffffff")])
