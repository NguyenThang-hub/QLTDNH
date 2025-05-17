import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class BillManager:
    def __init__(self, root):
        self.root = root

    def show_invoice(self, order_summary, total_price, order_id, username):
        invoice_window = tk.Toplevel(self.root)
        invoice_window.title("Hóa đơn")
        invoice_window.geometry("450x600")
        invoice_window.configure(bg="#f0f4f8")

        # Thông tin nhà hàng
        tk.Label(
            invoice_window,
            text="Nhà hàng THẮNG",
            font=("Helvetica", 16, "bold"),
            bg="#f0f4f8",
            fg="#333333"
        ).pack(pady=10)

        tk.Label(
            invoice_window,
            text="Địa chỉ: 123 Đường VKU, TP.Đà Nẵng",
            font=("Helvetica", 12),
            bg="#f0f4f8",
            fg="#333333"
        ).pack()

        tk.Label(
            invoice_window,
            text="Số điện thoại: 0123 456 789",
            font=("Helvetica", 12),
            bg="#f0f4f8",
            fg="#333333"
        ).pack(pady=(0, 10))

        # Đường kẻ phân cách
        separator = tk.Frame(invoice_window, height=2, bd=1, relief="sunken", bg="#333333")
        separator.pack(fill="x", padx=20, pady=5)

        # Tiêu đề hóa đơn
        tk.Label(
            invoice_window,
            text="Hóa đơn chi tiết",
            font=("Helvetica", 14, "bold"),
            bg="#f0f4f8",
            fg="#2c3e50"
        ).pack(pady=10)

        # Chi tiết đơn hàng
        tk.Label(
            invoice_window,
            text=f"Mã đơn hàng: #{order_id}",
            font=("Helvetica", 12),
            bg="#f0f4f8",
            fg="#333333"
        ).pack(anchor="w", padx=20)

        tk.Label(
            invoice_window,
            text=f"Người dùng: {username}",
            font=("Helvetica", 12),
            bg="#f0f4f8",
            fg="#333333"
        ).pack(anchor="w", padx=20, pady=(5, 0))

        tk.Label(
            invoice_window,
            text=f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            font=("Helvetica", 12),
            bg="#f0f4f8",
            fg="#333333"
        ).pack(anchor="w", padx=20, pady=(0, 10))

        # Frame cho chi tiết món
        items_frame = tk.Frame(invoice_window, bg="#ffffff", bd=1, relief="solid")
        items_frame.pack(padx=20, pady=10, fill="both")

        tk.Label(
            items_frame,
            text=order_summary,
            font=("Helvetica", 12),
            bg="#ffffff",
            fg="#333333",
            justify="left"
        ).pack(padx=10, pady=10)

        # Đường kẻ phân cách
        separator = tk.Frame(invoice_window, height=2, bd=1, relief="sunken", bg="#333333")
        separator.pack(fill="x", padx=20, pady=5)

        # Tự động in hóa đơn và đóng cửa sổ
        # self.show_invoice(order_id, order_summary, total_price)
        # invoice_window.destroy()

    # def print_invoice(self, order_id, order_summary, total_price):
    #     # Lưu hóa đơn thành file text
    #     filename = f"invoice_{order_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    #     try:
    #         with open(filename, "w", encoding="utf-8") as f:
    #             f.write("========== NHÀ HÀNG XYZ ==========\n")
    #             f.write("Địa chỉ: 123 Đường Ẩm Thực, TP. HCM\n")
    #             f.write("Số điện thoại: 0123 456 789\n")
    #             f.write("==================================\n\n")
    #             f.write(f"HÓA ĐƠN CHI TIẾT\n")
    #             f.write(f"Mã đơn hàng: #{order_id}\n")
    #             f.write(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    #             f.write(order_summary + "\n")
    #             f.write("==================================\n")
    #             f.write("Cảm ơn quý khách!\n")
    #         messagebox.showinfo("Thành công", f"Hóa đơn đã được lưu vào {filename}")
    #     except Exception as e:
    #         messagebox.showerror("Lỗi", f"Không thể lưu hóa đơn: {str(e)}")