import customtkinter as ctk
from tkinter import messagebox
from DAO.DatabaseOperation import *
from Bill import BillManager
from Report import show_monthly_report
from Table import choose_table_window

class MenuApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Thực đơn nhà hàng")
        self.root.geometry("900x700")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        self.food_items = get_items_by_category("food")
        self.drink_items = get_items_by_category("drink")
        self.food_quantities = {}
        self.drink_quantities = {}

        # === Giao diện chính chia 2 phần ===
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(fill="both", expand=True)

        # === Sidebar bên trái ===
        sidebar = ctk.CTkFrame(main_frame, width=200, corner_radius=10)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(sidebar, text="Chức năng", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 20))

        ctk.CTkButton(sidebar, text="🪑 Chọn bàn", command=self.open_table_window).pack(pady=10)
        self.label_selected = ctk.CTkLabel(sidebar, text="Chưa chọn bàn")
        self.label_selected.pack(pady=10)
        ctk.CTkButton(sidebar, text="🛠️ Quản lý", command=self.admin_mode).pack(pady=10)
        ctk.CTkButton(sidebar, text="❌ Thoát", command=root.quit).pack(pady=10)

        # === Khu vực nội dung cuộn được ===
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        canvas = ctk.CTkCanvas(content_frame)
        scrollbar = ctk.CTkScrollbar(content_frame, command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # === Nội dung: tiêu đề ===
        ctk.CTkLabel(scrollable_frame, text="Thực đơn", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        # === Món ăn ===
        ctk.CTkLabel(scrollable_frame, text="🍽️ Món ăn", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        for item in self.food_items:
            frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
            frame.pack(padx=10, pady=5, fill="x")
            ctk.CTkLabel(frame, text=f"{item['name']} ({item['price']:,} VNĐ)", font=ctk.CTkFont(size=13)).pack(side="left", padx=10, pady=5)
            spin = ctk.CTkComboBox(frame, values=[str(i) for i in range(11)], width=60)
            spin.set("0")
            spin.pack(side="right", padx=10)
            self.food_quantities[item['name']] = spin

        # === Đồ uống ===
        ctk.CTkLabel(scrollable_frame, text="🥤 Đồ uống", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(15, 5))
        for item in self.drink_items:
            frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
            frame.pack(padx=10, pady=5, fill="x")
            ctk.CTkLabel(frame, text=f"{item['name']} ({item['price']:,} VNĐ)", font=ctk.CTkFont(size=13)).pack(side="left", padx=10, pady=5)
            spin = ctk.CTkComboBox(frame, values=[str(i) for i in range(11)], width=60)
            spin.set("0")
            spin.pack(side="right", padx=10)
            self.drink_quantities[item['name']] = spin

        # === Xác nhận và báo cáo ===
        btn_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="✅ Xác nhận đơn", command=self.confirm_order, width=200).pack(pady=5)
        ctk.CTkButton(btn_frame, text="📈 Báo cáo doanh thu", command=show_monthly_report, width=200).pack(pady=5)

    def confirm_order(self):
        order_items = []
        total_price = 0
        summary = "Món ăn:\n"
        has_order = False

        for item in self.food_items:
            quantity = int(self.food_quantities[item['name']].get())
            if quantity > 0:
                price = item['price'] * quantity
                summary += f"{item['name']}: {quantity} x {item['price']:,} = {price:,} VNĐ\n"
                total_price += price
                order_items.append({"name": item['name'], "quantity": quantity, "price": item['price']})
                has_order = True

        summary += "\nĐồ uống:\n"
        for item in self.drink_items:
            quantity = int(self.drink_quantities[item['name']].get())
            if quantity > 0:
                price = item['price'] * quantity
                summary += f"{item['name']}: {quantity} x {item['price']:,} = {price:,} VNĐ\n"
                total_price += price
                order_items.append({"name": item['name'], "quantity": quantity, "price": item['price']})
                has_order = True

        if not has_order:
            messagebox.showwarning("Thông báo", "Vui lòng chọn ít nhất một món.")
            return

        summary += f"\nTổng cộng: {total_price:,} VNĐ"
        order_id = save_order(self.username, total_price, order_items)
        if order_id:
            bill_window = BillManager(self.root)
            bill_window.show_invoice(summary, total_price, order_id, self.username)
        else:
            messagebox.showerror("Lỗi", "Không thể lưu đơn hàng.")

    def open_table_window(self):
        choose_table_window(self.root, self.set_selected_table)

    def set_selected_table(self, table_number):
        self.selected_table = table_number
        self.label_selected.configure(text=f"Bàn đã chọn: {table_number}")

    def admin_mode(self):
        messagebox.showinfo("Quản lý", "Chuyển sang chế độ quản lý: thêm/sửa/xoá món ăn (chức năng chưa hoàn thiện).")
