import customtkinter as ctk
from tkinter import messagebox, Menu
from DAO.DatabaseOperation import *
from Bill import BillManager
from Table import choose_table_window
from Admin import AdminMode

class MenuForGuest:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Thực đơn nhà hàng")
        self.root.geometry("900x700")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Lấy dữ liệu món ăn từ database (sẽ được làm mới khi cần)
        self.load_menu_items()

        self.selected_table = None
        self.table_orders = {}

        self.main_quantities = {}
        self.side_quantities = {}
        self.accomp_quantities = {}
        self.drink_quantities = {}

        # Main frame
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(fill="both", expand=True)

        # Sidebar
        sidebar = ctk.CTkFrame(main_frame, width=200, corner_radius=10)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(sidebar, text="Danh mục", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 20))
        ctk.CTkButton(sidebar, text="🪑 Chọn bàn", command=self.open_table_window).pack(pady=10)

        ctk.CTkButton(sidebar, text="🍽️ Món chính", command=lambda: self.show_category("main_dish")).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(sidebar, text="🥗 Món phụ", command=lambda: self.show_category("side_dish")).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(sidebar, text="🍟 Món ăn kèm", command=lambda: self.show_category("accompaniment")).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(sidebar, text="🥤 Đồ uống", command=lambda: self.show_category("drink")).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(sidebar, text="📋 Xem tất cả", command=self.show_all_categories).pack(pady=5, fill="x", padx=10)

        # Content frame
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        canvas = ctk.CTkCanvas(content_frame)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ctk.CTkScrollbar(content_frame, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.scrollable_frame = ctk.CTkFrame(canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=content_frame.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)

        # Cập nhật chiều rộng khi content_frame thay đổi kích thước
        content_frame.bind("<Configure>", lambda e: canvas.itemconfig(canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw"), width=e.width))

        # Mặc định hiển thị danh mục đầu tiên (Món chính)
        self.show_category("main_dish")

    def load_menu_items(self):
        """Tải lại dữ liệu món ăn từ database"""
        self.main_dishes = get_items_by_category("main_dish")
        self.side_dishes = get_items_by_category("side_dish")
        self.accompaniments = get_items_by_category("accompaniment")
        self.drinks = get_items_by_category("drink")

    def show_category(self, category):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.scrollable_frame, text="Thực đơn", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10, fill="x", padx=10)

        # Xóa các từ điển số lượng trước khi hiển thị danh mục mới
        self.main_quantities = {}
        self.side_quantities = {}
        self.accomp_quantities = {}
        self.drink_quantities = {}

        # Chọn danh mục để hiển thị
        if category == "main_dish":
            items = self.main_dishes
            title = "🍽️ Món chính"
            quantities_dict = self.main_quantities
        elif category == "side_dish":
            items = self.side_dishes
            title = "🥗 Món phụ"
            quantities_dict = self.side_quantities
        elif category == "accompaniment":
            items = self.accompaniments
            title = "🍟 Món ăn kèm"
            quantities_dict = self.accomp_quantities
        else:  # category == "drink"
            items = self.drinks
            title = "🥤 Đồ uống"
            quantities_dict = self.drink_quantities

        ctk.CTkLabel(self.scrollable_frame, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5), fill="x")
        for item in items:
            frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
            frame.pack(padx=10, pady=5, fill="x")
            ctk.CTkLabel(frame, text=f"{item['name']} ({item['price']:,} VNĐ)", font=ctk.CTkFont(size=13), wraplength=400).pack(side="left", padx=10, pady=5, fill="x", expand=True)
            spin = ctk.CTkComboBox(frame, values=[str(i) for i in range(11)], width=60)
            spin.set("0")
            spin.pack(side="right", padx=10)
            quantities_dict[item['name']] = spin

        btn_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        btn_frame.pack(pady=20, fill="x", padx=10)
        ctk.CTkButton(btn_frame, text="✅ Xác nhận đơn", command=self.confirm_order, width=200).pack(pady=5)

        # Nếu đã chọn bàn và có dữ liệu => load lại
        if self.selected_table in self.table_orders:
            data = self.table_orders[self.selected_table]
            for name, spin in quantities_dict.items():
                spin.set(str(data.get(name, 0)))

    def show_all_categories(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.scrollable_frame, text="Thực đơn", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10, fill="x", padx=10)

        # Xóa các từ điển số lượng trước khi hiển thị tất cả danh mục
        self.main_quantities = {}
        self.side_quantities = {}
        self.accomp_quantities = {}
        self.drink_quantities = {}

        # Món chính
        ctk.CTkLabel(self.scrollable_frame, text="🍽️ Món chính", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5), fill="x")
        for item in self.main_dishes:
            frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
            frame.pack(padx=10, pady=5, fill="x")
            ctk.CTkLabel(frame, text=f"{item['name']} ({item['price']:,} VNĐ)", font=ctk.CTkFont(size=13), wraplength=400).pack(side="left", padx=10, pady=5, fill="x", expand=True)
            spin = ctk.CTkComboBox(frame, values=[str(i) for i in range(11)], width=60)
            spin.set("0")
            spin.pack(side="right", padx=10)
            self.main_quantities[item['name']] = spin

        # Món phụ
        ctk.CTkLabel(self.scrollable_frame, text="🥗 Món phụ", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(15, 5), fill="x")
        for item in self.side_dishes:
            frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
            frame.pack(padx=10, pady=5, fill="x")
            ctk.CTkLabel(frame, text=f"{item['name']} ({item['price']:,} VNĐ)", font=ctk.CTkFont(size=13), wraplength=400).pack(side="left", padx=10, pady=5, fill="x", expand=True)
            spin = ctk.CTkComboBox(frame, values=[str(i) for i in range(11)], width=60)
            spin.set("0")
            spin.pack(side="right", padx=10)
            self.side_quantities[item['name']] = spin

        # Món ăn kèm
        ctk.CTkLabel(self.scrollable_frame, text="🍟 Món ăn kèm", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(15, 5), fill="x")
        for item in self.accompaniments:
            frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
            frame.pack(padx=10, pady=5, fill="x")
            ctk.CTkLabel(frame, text=f"{item['name']} ({item['price']:,} VNĐ)", font=ctk.CTkFont(size=13), wraplength=400).pack(side="left", padx=10, pady=5, fill="x", expand=True)
            spin = ctk.CTkComboBox(frame, values=[str(i) for i in range(11)], width=60)
            spin.set("0")
            spin.pack(side="right", padx=10)
            self.accomp_quantities[item['name']] = spin

        # Đồ uống
        ctk.CTkLabel(self.scrollable_frame, text="🥤 Đồ uống", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(15, 5), fill="x")
        for item in self.drinks:
            frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
            frame.pack(padx=10, pady=5, fill="x")
            ctk.CTkLabel(frame, text=f"{item['name']} ({item['price']:,} VNĐ)", font=ctk.CTkFont(size=13), wraplength=400).pack(side="left", padx=10, pady=5, fill="x", expand=True)
            spin = ctk.CTkComboBox(frame, values=[str(i) for i in range(11)], width=60)
            spin.set("0")
            spin.pack(side="right", padx=10)
            self.drink_quantities[item['name']] = spin

        btn_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        btn_frame.pack(pady=20, fill="x", padx=10)
        ctk.CTkButton(btn_frame, text="✅ Xác nhận đơn", command=self.confirm_order, width=200).pack(pady=5)

        # Nếu đã chọn bàn và có dữ liệu => load lại
        if self.selected_table in self.table_orders:
            data = self.table_orders[self.selected_table]
            for name, spin in self.main_quantities.items():
                spin.set(str(data.get(name, 0)))
            for name, spin in self.side_quantities.items():
                spin.set(str(data.get(name, 0)))
            for name, spin in self.accomp_quantities.items():
                spin.set(str(data.get(name, 0)))
            for name, spin in self.drink_quantities.items():
                spin.set(str(data.get(name, 0)))

    def confirm_order(self):
        if not self.selected_table:
            messagebox.showwarning("Thông báo", "Vui lòng chọn bàn trước khi gọi món.")
            return

        table_data = {}
        has_order = False

        for item in self.main_dishes:
            quantity = int(self.main_quantities.get(item['name'], ctk.CTkComboBox(values=["0"])).get())
            if quantity > 0:
                table_data[item['name']] = quantity
                has_order = True

        for item in self.side_dishes:
            quantity = int(self.side_quantities.get(item['name'], ctk.CTkComboBox(values=["0"])).get())
            if quantity > 0:
                table_data[item['name']] = quantity
                has_order = True

        for item in self.accompaniments:
            quantity = int(self.accomp_quantities.get(item['name'], ctk.CTkComboBox(values=["0"])).get())
            if quantity > 0:
                table_data[item['name']] = quantity
                has_order = True

        for item in self.drinks:
            quantity = int(self.drink_quantities.get(item['name'], ctk.CTkComboBox(values=["0"])).get())
            if quantity > 0:
                table_data[item['name']] = quantity
                has_order = True

        if not has_order:
            messagebox.showwarning("Thông báo", "Vui lòng chọn ít nhất một món.")
            return

        self.table_orders[self.selected_table] = table_data
        messagebox.showinfo("Xác nhận đơn", f"Đơn hàng cho bàn {self.selected_table} đã được lưu tạm.")

        table_data = self.table_orders[self.selected_table]
        order_items = []
        total_price = 0
        summary = f"Bàn số: {self.selected_table}\nMón ăn:\n"

        for item in self.main_dishes + self.side_dishes + self.accompaniments + self.drinks:
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
            del self.table_orders[self.selected_table]
            self.show_category("main_dish")  # Quay lại danh mục mặc định
        else:
            messagebox.showerror("Lỗi", "Không thể lưu đơn hàng.")

    def load_menu_items(self):
        """Tải lại dữ liệu món ăn từ database"""
        self.main_dishes = get_items_by_category("main_dish")
        self.side_dishes = get_items_by_category("side_dish")
        self.accompaniments = get_items_by_category("accompaniment")
        self.drinks = get_items_by_category("drink")

    def open_table_window(self):
        choose_table_window(self.root, self.set_selected_table)

    def set_selected_table(self, table_number):
        self.selected_table = table_number
        self.show_category("main_dish")  # Cập nhật danh mục mặc định

    def admin_mode(self):
        window = ctk.CTkToplevel(self.root)
        window.title("Chế độ quản lý!")
        window.geometry("400x300")

        title = ctk.CTkLabel(window, text="Xác nhận đăng nhập", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=(60, 30))

        mk = ctk.CTkEntry(window, placeholder_text="Mật khẩu", width=250, show="*")
        mk.pack(padx=15, pady=10)
        mk.focus()

        error_label = ctk.CTkLabel(window, text="", text_color="red")
        error_label.pack(pady=5)

        def check_password(event=None):
            if mk.get() == "4321":
                window.destroy()
                AdminMode(refresh_menu_callback=self.load_menu_items)
            else:
                error_label.configure(text="Sai mật khẩu!")

        btn = ctk.CTkButton(window, text="Xác nhận", command=check_password)
        btn.pack(pady=20)

        mk.bind("<Return>", check_password)

if __name__ == "__main__":
    root = ctk.CTk()
    app = MenuForGuest(root, "KhachHang01")
    root.mainloop()