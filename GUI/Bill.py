import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from QRCode import QRCode

class BillManager:
    def __init__(self, root):
        self.root = root

    def show_invoice(self, order_summary, total_price, order_id, username):
        invoice_window = tk.Toplevel(self.root)
        invoice_window.title("Hóa Đơn - Nhà Hàng Kiểu Pháp")
        invoice_window.geometry("800x1000")  # Tăng kích thước để chứa phần thanh toán
        invoice_window.configure(bg="#f0f4f8")

        # Frame chính để chứa nội dung
        main_frame = ttk.Frame(invoice_window, padding=10)
        main_frame.pack(fill="both", expand=True)

        # Thông tin nhà hàng
        ttk.Label(
            main_frame,
            text="Nhà Hàng Kiểu Pháp",
            font=("Helvetica", 18, "bold"),
            foreground="#2c3e50",
            background="#f0f4f8"
        ).pack(pady=(10, 5))

        ttk.Label(
            main_frame,
            text="Địa chỉ: 123 Đường VKU, TP. Đà Nẵng",
            font=("Helvetica", 12),
            foreground="#333333",
            background="#f0f4f8"
        ).pack()

        ttk.Label(
            main_frame,
            text="Số điện thoại: 0123 456 789",
            font=("Helvetica", 12),
            foreground="#333333",
            background="#f0f4f8"
        ).pack(pady=(0, 10))

        # Đường kẻ phân cách
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.pack(fill="x", padx=20, pady=10)

        # Tiêu đề hóa đơn
        ttk.Label(
            main_frame,
            text="Hóa Đơn Chi Tiết",
            font=("Helvetica", 16, "bold"),
            foreground="#2c3e50",
            background="#f0f4f8"
        ).pack(pady=(5, 10))

        # Frame cho chi tiết đơn hàng
        details_frame = ttk.Frame(main_frame, relief="solid", borderwidth=1, style="Details.TFrame")
        details_frame.pack(padx=20, pady=10, fill="both")

        ttk.Label(
            details_frame,
            text=f"Mã đơn hàng: #{order_id}",
            font=("Helvetica", 12),
            foreground="#333333",
            background="#ffffff"
        ).pack(anchor="w", padx=10, pady=(10, 5))

        ttk.Label(
            details_frame,
            text=f"Người dùng: {username}",
            font=("Helvetica", 12),
            foreground="#333333",
            background="#ffffff"
        ).pack(anchor="w", padx=10, pady=5)

        ttk.Label(
            details_frame,
            text=f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            font=("Helvetica", 12),
            foreground="#333333",
            background="#ffffff"
        ).pack(anchor="w", padx=10, pady=(5, 10))

        # Hiển thị tóm tắt đơn hàng
        ttk.Label(
            details_frame,
            text=order_summary,
            font=("Helvetica", 12),
            foreground="#333333",
            background="#ffffff",
            justify="left",
            wraplength=450
        ).pack(anchor="w", padx=10, pady=10)

     # Đường kẻ phân cách
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.pack(fill="x", padx=20, pady=10)

        # Frame cho phần thanh toán
        payment_frame = ttk.Frame(main_frame, relief="solid", borderwidth=1, style="Details.TFrame")
        payment_frame.pack(padx=20, pady=10, fill="both")

        ttk.Label(
            payment_frame,
            text="Chọn Phương Thức Thanh Toán",
            font=("Helvetica", 14, "bold"),
            foreground="#333333",
            background="#ffffff"
        ).pack(anchor="w", padx=10, pady=(10, 5))


        payment_method = tk.StringVar(value="Cash")

        def process_payment(method):
                if method == "Card":
                    messagebox.showinfo("Thanh Toán", "Đã xử lý thanh toán bằng thẻ!")
                    card_button.configure(state="disabled")
                    qr_button.configure(state="disabled")
                    cash_button.configure(state="disabled")
                elif method == "QR":
                    QRCode(invoice_window, order_id, username, total_price, card_button, qr_button, cash_button)
                elif method == "Cash":
                    messagebox.showinfo("Thanh Toán", "Thanh toán bằng tiền mặt đã được ghi nhận!")
                    card_button.configure(state="disabled")
                    qr_button.configure(state="disabled")
                    cash_button.configure(state="disabled")

        # Frame cho các nút thanh toán
        payment_button_frame = ttk.Frame(payment_frame)
        payment_button_frame.pack(pady=5)

        # Nút chọn thanh toán bằng Card
        card_button = ttk.Button(
            payment_button_frame,
            text="Thẻ",
            command=lambda: [payment_method.set("Card"), process_payment('Card')],
            style="TButton"
        )
        card_button.pack(side="left", padx=5)

        # Nút chọn thanh toán bằng QR
        qr_button = ttk.Button(
            payment_button_frame,
            text="QR",
            command=lambda: [payment_method.set("QR"), process_payment('QR')],
            style="TButton"
        )
        qr_button.pack(side="left", padx=5)

        # Nút chọn thanh toán bằng Cash
        cash_button = ttk.Button(
            payment_button_frame,
            text="Tiền Mặt",
            command=lambda: [payment_method.set("Cash"), process_payment('Cash')],
            style="TButton"
        )
        cash_button.pack(side="left", padx=5)

        # Đường kẻ phân cách
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.pack(fill="x", padx=20, pady=10)

        # Frame cho phần feedback
        feedbacks_frame = ttk.Frame(main_frame, relief="solid", borderwidth=1, style="Details.TFrame")
        feedbacks_frame.pack(padx=20, pady=10, fill="both", expand=True)

        ttk.Label(
            feedbacks_frame,
            text="Phản Hồi Của Khách Hàng",
            font=("Helvetica", 14, "bold"),
            foreground="#333333",
            background="#ffffff"
        ).pack(anchor="w", padx=10, pady=(10, 5))

        # Ô nhập phản hồi
        ttk.Label(
            feedbacks_frame,
            text="Nhập phản hồi của bạn:",
            font=("Helvetica", 12),
            foreground="#333333",
            background="#ffffff"
        ).pack(anchor="w", padx=10, pady=(5, 5))

        feedback_text = tk.Text(
            feedbacks_frame,
            height=4,
            width=50,
            font=("Helvetica", 12),
            relief="solid",
            bd=1
        )
        feedback_text.pack(padx=10, pady=5)

        # Frame cho các nút trong phần feedback
        button_frame = ttk.Frame(feedbacks_frame)
        button_frame.pack(pady=10)

        def submit_feedback():
            feedback = feedback_text.get("1.0", tk.END).strip()
            if feedback:
                messagebox.showinfo("Thông báo", "Cảm ơn bạn đã gửi phản hồi!")
                feedback_text.delete("1.0", tk.END)
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập phản hồi trước khi gửi!")

        ttk.Button(
            button_frame,
            text="Gửi Phản Hồi",
            command=submit_feedback,
            style="TButton"
        ).pack(side="left", padx=5)

        # Tùy chỉnh style cho giao diện
        style = ttk.Style()
        style.configure("Details.TFrame", background="#ffffff")
        style.configure("TButton", font=("Helvetica", 12), padding=6)
        style.map("TButton",
                  background=[("active", "#45a049")],
                  foreground=[("active", "#ffffff")])
