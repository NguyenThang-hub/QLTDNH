import customtkinter as ctk
from tkinter import messagebox
from DAO.DatabaseOperation import *
from Bill import BillManager
from Table import choose_table_window
from Admin import AdminMode

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
        self.selected_table = None

        # Lưu món đã chọn theo từng bàn
        self.table_orders = {}

        self.food_quantities = {}
        self.drink_quantities = {}

        main_frame = ctk.CTkFrame(root)
        main_frame.pack(fill="both", expand=True)

        sidebar = ctk.CTkFrame(main_frame, width=200, corner_radius=10)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(sidebar, text="Chức năng", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 20))
        ctk.CTkButton(sidebar, text="🪑 Chọn bàn", command=self.open_table_window).pack(pady=10)
        self.label_selected = ctk.CTkLabel(sidebar, text="Chưa chọn bàn")
        self.label_selected.pack(pady=10)
        ctk.CTkButton(sidebar, text="🛠️ Quản lý", command=self.admin_mode).pack(pady=10)
        ctk.CTkButton(sidebar, text="❌ Thoát", command=root.quit).pack(pady=10)

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

        self.build_menu_ui()

    def build_menu_ui(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.scrollable_frame, text="Thực đơn", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        self.food_quantities = {}
        self.drink_quantities = {}

        ctk.CTkLabel(self.scrollable_frame, text="🍽️ Món ăn", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        for item in self.food_items:
            frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
            frame.pack(padx=10, pady=5, fill="x")
            ctk.CTkLabel(frame, text=f"{item['name']} ({item['price']:,} VNĐ)", font=ctk.CTkFont(size=13)).pack(side="left", padx=10, pady=5)
            spin = ctk.CTkComboBox(frame, values=[str(i) for i in range(11)], width=60)
            spin.set("0")
            spin.pack(side="right", padx=10)
            self.food_quantities[item['name']] = spin

        ctk.CTkLabel(self.scrollable_frame, text="🥤 Đồ uống", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(15, 5))
        for item in self.drink_items:
            frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
            frame.pack(padx=10, pady=5, fill="x")
            ctk.CTkLabel(frame, text=f"{item['name']} ({item['price']:,} VNĐ)", font=ctk.CTkFont(size=13)).pack(side="left", padx=10, pady=5)
            spin = ctk.CTkComboBox(frame, values=[str(i) for i in range(11)], width=60)
            spin.set("0")
            spin.pack(side="right", padx=10)
            self.drink_quantities[item['name']] = spin

        btn_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="✅ Xác nhận đơn", command=self.confirm_order, width=200).pack(pady=5)
        ctk.CTkButton(btn_frame, text="💵 Thanh toán", command=self.pay_order, width=200).pack(pady=5)

        # Nếu đã chọn bàn và có dữ liệu => load lại
        if self.selected_table in self.table_orders:
            data = self.table_orders[self.selected_table]
            for name, spin in self.food_quantities.items():
                spin.set(str(data.get(name, 0)))
            for name, spin in self.drink_quantities.items():
                spin.set(str(data.get(name, 0)))

    def confirm_order(self):
        if not self.selected_table:
            messagebox.showwarning("Thông báo", "Vui lòng chọn bàn trước khi gọi món.")
            return

        table_data = {}
        has_order = False

        for item in self.food_items:
            quantity = int(self.food_quantities[item['name']].get())
            if quantity > 0:
                table_data[item['name']] = quantity
                has_order = True

        for item in self.drink_items:
            quantity = int(self.drink_quantities[item['name']].get())
            if quantity > 0:
                table_data[item['name']] = quantity
                has_order = True

        if not has_order:
            messagebox.showwarning("Thông báo", "Vui lòng chọn ít nhất một món.")
            return

        self.table_orders[self.selected_table] = table_data
        messagebox.showinfo("Xác nhận đơn", f"Đơn hàng cho bàn {self.selected_table} đã được lưu tạm.")

    def pay_order(self):
        if not self.selected_table or self.selected_table not in self.table_orders:
            messagebox.showwarning("Thông báo", "Không có đơn nào để thanh toán.")
            return

        table_data = self.table_orders[self.selected_table]
        order_items = []
        total_price = 0
        summary = f"Bàn số: {self.selected_table}\nMón ăn:\n"

        for item in self.food_items + self.drink_items:
            name = item['name']
            if name in table_data and table_data[name] > 0:
                quantity = table_data[name]
                price = quantity * item['price']
                summary += f"{name}: {quantity} x {item['price']:,} = {price:,} VNĐ\n"
                total_price += price
                order_items.append({"name": name, "quantity": quantity, "price": item['price']})

        summary += f"\nTổng cộng: {total_price:,} VNĐ"

        order_id = save_order(self.username, total_price, order_items, table_id=self.selected_table)
        if order_id:
            bill_window = BillManager(self.root)
            bill_window.show_invoice(summary, total_price, order_id, self.username)
            # Reset sau khi in hóa đơn
            del self.table_orders[self.selected_table]
            self.build_menu_ui()
        else:
            messagebox.showerror("Lỗi", "Không thể lưu đơn hàng.")

    def load_menu_items(self):
        self.food_items, self.drink_items = get_menu_items()

    def open_table_window(self):
        choose_table_window(self.root, self.set_selected_table)

    def set_selected_table(self, table_number):
        self.selected_table = table_number
        self.label_selected.configure(text=f"Bàn đã chọn: {table_number}")
        self.build_menu_ui()

    def admin_mode(self):
        window = ctk.CTkToplevel(self.root)
        window.title("Chế độ quản lý!")
        window.geometry("400x300")

        title = ctk.CTkLabel(window, text="Xác nhận đăng nhập", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=(60, 30))

        mk = ctk.CTkEntry(window, placeholder_text="Mật khẩu", width=250, show="*")
        mk.pack(padx=15, pady=10)

        def check_password():
            if mk.get() == "4321":
                window.destroy()
                AdminMode(refresh_menu_callback=self.load_menu_items)  # Gọi AdminMode và truyền callback
            else:
                ctk.CTkLabel(window, text="Sai mật khẩu!", text_color="red").pack()

        btn = ctk.CTkButton(window, text="Xác nhận", command=check_password)
        btn.pack(pady=20)

