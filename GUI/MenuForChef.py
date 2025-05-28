import customtkinter as ctk
from tkinter import messagebox
from DAO.DatabaseOperation import *

class MenuChef:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Giao diện đầu bếp")
        self.root.geometry("1000x700")  # Compact widt2 for right-side placement
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Main frame
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Sidebar
        sidebar = ctk.CTkFrame(main_frame, width=150, corner_radius=10)  # Reduced width for compactness
        sidebar.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(sidebar, text="Chức năng", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 20))
        ctk.CTkButton(sidebar, text="📑 Xem đơn hàng", command=self.show_orders, width=120).pack(pady=10, fill="x", padx=10)
        ctk.CTkButton(sidebar, text="❌ Thoát", command=root.quit, width=120).pack(pady=10, fill="x", padx=10)

        # Content frame with canvas and scrollbar
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        canvas = ctk.CTkCanvas(content_frame)
        scrollbar = ctk.CTkScrollbar(content_frame, command=canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.table_orders = {}  # To store orders
        self.load_orders()  # Load existing orders
        self.show_orders()

    def load_orders(self):
        # Placeholder: Load orders from database
        # Implement based on your DatabaseOperation module
        pass

    def show_orders(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.scrollable_frame, text="Danh sách đơn hàng", font=ctk.CTkFont(size=20, weight="bold")).pack(
            pady=10)

        orders = get_all_orders_with_items()
        if not orders:
            ctk.CTkLabel(self.scrollable_frame, text="Chưa có đơn hàng nào.", font=ctk.CTkFont(size=14)).pack(pady=10)
            return

        for order in orders:
            order_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
            order_frame.pack(padx=10, pady=5, fill="x")

            table_number = order['table_id']  # bạn có thể đổi thành order['table_number'] nếu cột là table_number

            ctk.CTkLabel(order_frame, text=f"Bàn số: {table_number}", font=ctk.CTkFont(size=16, weight="bold")).pack(
                anchor="w", padx=10, pady=5)

            summary = "Món ăn:\n"
            total_price = 0
            order_items = []

            for item in order['items']:
                name = item['name']
                quantity = item['quantity']
                price = item['price']
                item_total = quantity * price

                summary += f"{name}: {quantity} x {price:,} = {item_total:,} VNĐ\n"
                total_price += item_total
                order_items.append({"name": name, "quantity": quantity, "price": price})

            summary += f"\nTổng cộng: {total_price:,} VNĐ"

            ctk.CTkLabel(order_frame, text=summary, font=ctk.CTkFont(size=13), wraplength=600, justify="left").pack(
                anchor="w", padx=10, pady=5)

            # Button frame for Confirm and Cancel buttons
            btn_frame = ctk.CTkFrame(order_frame, fg_color="transparent")
            btn_frame.pack(pady=5, fill="x", padx=10)

            ctk.CTkButton(
                btn_frame,
                text="✅ Xác nhận đơn",
                command=lambda tn=table_number: self.confirm_order(tn),
                width=120
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                btn_frame,
                text="❌ Hủy đơn",
                command=lambda tn=table_number: self.cancel_order(tn),
                width=120
            ).pack(side="right", padx=5)

    def confirm_order(self, table_number):
        messagebox.showinfo("Xác nhận", f"Đơn hàng cho bàn {table_number} đã được xác nhận.")
        self.show_orders()  # Refresh UI

    def cancel_order(self, table_number):
        if messagebox.askyesno("Hủy đơn", f"Bạn có chắc muốn hủy đơn hàng cho bàn {table_number}?"):
            if table_number in self.table_orders:
                del self.table_orders[table_number]
                messagebox.showinfo("Hủy đơn", f"Đơn hàng cho bàn {table_number} đã được hủy.")
                self.show_orders()