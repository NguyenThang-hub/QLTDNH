import tkinter as tk
from tkinter import ttk, messagebox
from db import save_order
from Bill import BillManager
from Report import show_monthly_report
from datetime import datetime

class MenuApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Restaurant Menu")
        self.root.geometry("500x750")
        self.root.configure(bg="#f0f4f8")

        # Style cho ttk widgets
        style = ttk.Style()
        style.configure("TLabel", background="#f0f4f8", font=("Helvetica", 12))
        style.configure("TFrame", background="#f0f4f8")
        style.configure("TButton", font=("Helvetica", 12, "bold"))
        style.map("TButton",
                  background=[("active", "#28a745"), ("!active", "#34c759")],
                  foreground=[("active", "white"), ("!active", "white")])

        # Danh sách món ăn và đồ uống với giá (VNĐ)
        self.food_items = [
            {"name": "Pizza", "price": 50000},
            {"name": "Burger", "price": 40000},
            {"name": "Mì ý", "price": 45000},
            {"name": "Salad", "price": 30000}
        ]
        self.drink_items = [
            {"name": "Coca", "price": 15000},
            {"name": "Nước ép", "price": 20000},
            {"name": "Nước suối", "price": 10000},
            {"name": "Trà giải nhiệt", "price": 12000}
        ]

        # Dictionary để lưu số lượng
        self.food_quantities = {}
        self.drink_quantities = {}

        # Tiêu đề
        title_label = tk.Label(
            root,
            text="Thực đơn nhà hàng",
            font=("Helvetica", 20, "bold"),
            bg="#f0f4f8",
            fg="#333333"
        )
        title_label.pack(pady=20)

        # Frame chính
        main_frame = ttk.Frame(root)
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Frame cho Món ăn
        food_label = tk.Label(
            main_frame,
            text="🍽️ Món ăn",
            font=("Helvetica", 14, "bold"),
            bg="#f0f4f8",
            fg="#2c3e50"
        )
        food_label.pack(anchor="w", pady=(10, 5))

        food_container = ttk.Frame(main_frame)
        food_container.pack(fill="x", pady=5)

        # Tạo các mục món ăn
        for food in self.food_items:
            frame = tk.Frame(
                food_container,
                bg="#ffffff",
                bd=1,
                relief="solid"
            )
            frame.pack(fill="x", pady=5, padx=10)

            tk.Label(
                frame,
                text=f"{food['name']} ({food['price']:,} VNĐ)",
                font=("Helvetica", 12),
                bg="#ffffff",
                fg="#333333",
                width=25
            ).pack(side="left", padx=10, pady=5)

            spinbox = ttk.Spinbox(
                frame,
                from_=0,
                to=10,
                width=5,
                font=("Helvetica", 12)
            )
            spinbox.delete(0, tk.END)
            spinbox.insert(0, "0")
            spinbox.pack(side="right", padx=10)
            self.food_quantities[food['name']] = spinbox

        # Frame cho Đồ uống
        drink_label = tk.Label(
            main_frame,
            text="🥤 Đồ uống",
            font=("Helvetica", 14, "bold"),
            bg="#f0f4f8",
            fg="#2c3e50"
        )
        drink_label.pack(anchor="w", pady=(20, 5))

        drink_container = ttk.Frame(main_frame)
        drink_container.pack(fill="x", pady=5)

        # Tạo các mục đồ uống
        for drink in self.drink_items:
            frame = tk.Frame(
                drink_container,
                bg="#ffffff",
                bd=1,
                relief="solid"
            )
            frame.pack(fill="x", pady=5, padx=10)

            tk.Label(
                frame,
                text=f"{drink['name']} ({drink['price']:,} VNĐ)",
                font=("Helvetica", 12),
                bg="#ffffff",
                fg="#333333",
                width=25
            ).pack(side="left", padx=10, pady=5)

            spinbox = ttk.Spinbox(
                frame,
                from_=0,
                to=10,
                width=5,
                font=("Helvetica", 12)
            )
            spinbox.delete(0, tk.END)
            spinbox.insert(0, "0")
            spinbox.pack(side="right", padx=10)
            self.drink_quantities[drink['name']] = spinbox

        # Nút Xác nhận
        confirm_button = ttk.Button(
            main_frame,
            text="Xác nhận",
            command=self.confirm_order,
            style="TButton"
        )
        confirm_button.pack(pady=10)

        # Nút Xem báo cáo doanh thu
        report_button = ttk.Button(
            main_frame,
            text="Xem báo cáo doanh thu",
            command=show_monthly_report,
            style="TButton"
        )
        report_button.pack(pady=10)

    def confirm_order(self):
        order_items = []
        total_price = 0
        order_summary = "Món ăn:\n"
        has_order = False

        # Kiểm tra món ăn
        for food in self.food_items:
            value = self.food_quantities[food['name']].get().strip()
            quantity = int(value) if value else 0
            if quantity > 0:
                item_price = food['price'] * quantity
                order_summary += f"{food['name']}: {quantity} x {food['price']:,} VNĐ = {item_price:,} VNĐ\n"
                order_items.append({
                    "name": food['name'],
                    "quantity": quantity,
                    "price": food['price']
                })
                total_price += item_price
                has_order = True

        order_summary += "\nĐồ uống:\n"
        # Kiểm tra đồ uống
        for drink in self.drink_items:
            value = self.drink_quantities[drink['name']].get().strip()
            quantity = int(value) if value else 0
            if quantity > 0:
                item_price = drink['price'] * quantity
                order_summary += f"{drink['name']}: {quantity} x {drink['price']:,} VNĐ = {item_price:,} VNĐ\n"
                order_items.append({
                    "name": drink['name'],
                    "quantity": quantity,
                    "price": drink['price']
                })
                total_price += item_price
                has_order = True

        if not has_order:
            messagebox.showwarning("Thông báo", "Vui lòng chọn ít nhất một món!")
            return

        order_summary += f"\nTổng cộng: {total_price:,} VNĐ"

        # Lưu đơn hàng vào database và lấy order_id
        order_id = save_order(self.username, total_price, order_items)
        if order_id is not None:
            bill_manager = BillManager(self.root)
            bill_manager.show_invoice(order_summary, total_price, order_id, self.username)
        else:
            messagebox.showerror("Lỗi", "Không thể lưu đơn hàng vào database.")