import customtkinter as ctk
from tkinter import messagebox
from DAO.DatabaseOperation import *
from Bill import BillManager
from Report import show_monthly_report

class MenuApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Thực đơn nhà hàng")
        self.root.geometry("500x700")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")


        self.food_items = get_items_by_category("food")
        self.drink_items = get_items_by_category("drink")
        self.food_quantities = {}
        self.drink_quantities = {}


        main_frame = ctk.CTkFrame(root, corner_radius=20)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(main_frame, text="Thực đơn", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=10)

        # === Món ăn ===
        food_label = ctk.CTkLabel(main_frame, text="🍽️ Món ăn", font=ctk.CTkFont(size=16, weight="bold"))
        food_label.pack(anchor="w", padx=10, pady=(10, 5))

        for item in self.food_items:
            frame = ctk.CTkFrame(main_frame, corner_radius=10)
            frame.pack(padx=10, pady=5, fill="x")

            name_label = ctk.CTkLabel(frame, text=f"{item['name']} ({item['price']:,} VNĐ)",
                                      font=ctk.CTkFont(size=13), anchor="w")
            name_label.pack(side="left", padx=10, pady=5)

            spin = ctk.CTkComboBox(frame, values=[str(i) for i in range(11)], width=60)
            spin.set("0")
            spin.pack(side="right", padx=10)
            self.food_quantities[item['name']] = spin

        # === Đồ uống ===
        drink_label = ctk.CTkLabel(main_frame, text="🥤 Đồ uống", font=ctk.CTkFont(size=16, weight="bold"))
        drink_label.pack(anchor="w", padx=10, pady=(15, 5))

        for item in self.drink_items:
            frame = ctk.CTkFrame(main_frame, corner_radius=10)
            frame.pack(padx=10, pady=5, fill="x")

            name_label = ctk.CTkLabel(frame, text=f"{item['name']} ({item['price']:,} VNĐ)",
                                      font=ctk.CTkFont(size=13), anchor="w")
            name_label.pack(side="left", padx=10, pady=5)

            spin = ctk.CTkComboBox(frame, values=[str(i) for i in range(11)], width=60)
            spin.set("0")
            spin.pack(side="right", padx=10)
            self.drink_quantities[item['name']] = spin

        # === Nút xác nhận và báo cáo ===
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        confirm_btn = ctk.CTkButton(btn_frame, text="Xác nhận đơn", command=self.confirm_order, width=200)
        confirm_btn.pack(pady=5)

        report_btn = ctk.CTkButton(btn_frame, text="Báo cáo doanh thu", command=show_monthly_report, width=200)
        report_btn.pack(pady=5)

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

