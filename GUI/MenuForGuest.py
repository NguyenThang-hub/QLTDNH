import customtkinter as ctk
from tkinter import messagebox
from DAO.DatabaseOperation import *
from Bill import BillManager
from Table import choose_table_window

class MenuForGuest:
    def __init__(self, root, username="Guest"):  # Thêm giá trị mặc định cho username
        self.root = root
        self.username = username
        self.root.title("Thực đơn nhà hàng")
        self.root.geometry("900x700")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        self.selected_table = None
        self.table_orders = {}
        self.temp_quantities = {}  # Từ điển tạm để lưu số lượng

        # Tải dữ liệu món ăn và đồ uống từ database
        self.food_items, self.drink_items = get_menu_items()

        # Main frame
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(fill="both", expand=True)

        # Sidebar
        sidebar = ctk.CTkFrame(main_frame, width=200, corner_radius=10)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(sidebar, text="Danh mục", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 20))
        ctk.CTkButton(sidebar, text="🪑 Chọn bàn", command=self.open_table_window).pack(pady=5, fill="x", padx=10)
        self.label_selected = ctk.CTkLabel(sidebar, text="Chưa chọn bàn")
        self.label_selected.pack(pady=5)
        ctk.CTkButton(sidebar, text="📋 Thực đơn", command=self.show_all_categories).pack(pady=5, fill="x", padx=10)

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

        # Mặc định hiển thị danh mục "Thực đơn"
        self.show_all_categories()

    def show_all_categories(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.scrollable_frame, text="Thực đơn", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10, fill="x", padx=10)

        # Xóa các từ điển số lượng trước khi hiển thị tất cả danh mục
        self.food_quantities = {}
        self.drink_quantities = {}

        # Món chính
        ctk.CTkLabel(self.scrollable_frame, text="🍽️ Món ăn", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5), fill="x")
        for item in self.food_items:
            frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
            frame.pack(padx=10, pady=5, fill="x")
            ctk.CTkLabel(frame, text=f"{item['name']} ({item['price']:,} VNĐ)", font=ctk.CTkFont(size=13), wraplength=400).pack(side="left", padx=10, pady=5, fill="x", expand=True)
            spin = ctk.CTkComboBox(master=frame, values=[str(i) for i in range(11)], width=60)
            # Khôi phục số lượng từ temp_quantities nếu có
            current_quantity = self.temp_quantities.get(item['name'], "0")
            spin.set(current_quantity)
            spin.pack(side="right", padx=10)
            self.food_quantities[item['name']] = spin

        # Đồ uống
        ctk.CTkLabel(self.scrollable_frame, text="🥤 Đồ uống", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(15, 5), fill="x")
        for item in self.drink_items:
            frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
            frame.pack(padx=10, pady=5, fill="x")
            ctk.CTkLabel(frame, text=f"{item['name']} ({item['price']:,} VNĐ)", font=ctk.CTkFont(size=13), wraplength=400).pack(side="left", padx=10, pady=5, fill="x", expand=True)
            spin = ctk.CTkComboBox(master=frame, values=[str(i) for i in range(11)], width=60)
            # Khôi phục số lượng từ temp_quantities nếu có
            current_quantity = self.temp_quantities.get(item['name'], "0")
            spin.set(current_quantity)
            spin.pack(side="right", padx=10)
            self.drink_quantities[item['name']] = spin

        btn_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        btn_frame.pack(pady=20, fill="x", padx=10)
        ctk.CTkButton(btn_frame, text="✅ Xác nhận đơn", command=self.confirm_order, width=200).pack(pady=5)

        # Lưu số lượng hiện tại vào temp_quantities
        for name, spin in self.food_quantities.items():
            self.temp_quantities[name] = spin.get()
        for name, spin in self.drink_quantities.items():
            self.temp_quantities[name] = spin.get()

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
            quantity = int(self.food_quantities.get(item['name'], ctk.CTkComboBox(master=self.scrollable_frame, values=["0"])).get())
            if quantity > 0:
                table_data[item['name']] = quantity
                has_order = True

        for item in self.drink_items:
            quantity = int(self.drink_quantities.get(item['name'], ctk.CTkComboBox(master=self.scrollable_frame, values=["0"])).get())
            if quantity > 0:
                table_data[item['name']] = quantity
                has_order = True

        if not has_order:
            messagebox.showwarning("Thông báo", "Vui lòng chọn ít nhất một món.")
            return

        self.table_orders[self.selected_table] = table_data

        # Cập nhật trạng thái bàn thành 'occupied'
        if update_table_status(self.selected_table, 'occupied'):
            print(f"Bàn {self.selected_table} đã được đặt.")
        else:
            print(f"Không thể cập nhật trạng thái bàn {self.selected_table}.")

        # Tạo summary và lưu đơn hàng
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
            # Hiển thị thông báo cảm ơn
            messagebox.showinfo("Cảm ơn", "Cảm ơn quý khách đã đặt hàng!")
            # Reset số lượng về 0
            for name, spin in self.food_quantities.items():
                spin.set("0")
            for name, spin in self.drink_quantities.items():
                spin.set("0")
            # Xóa đơn hàng tạm từ table_orders
            del self.table_orders[self.selected_table]
            # Cập nhật trạng thái bàn thành 'available' sau khi hoàn tất
            if update_table_status(self.selected_table, 'available'):
                print(f"Bàn {self.selected_table} đã được giải phóng.")
            else:
                print(f"Không thể cập nhật trạng thái bàn {self.selected_table}.")
            self.show_all_categories()  # Làm mới giao diện với "Thực đơn"
        else:
            messagebox.showerror("Lỗi", "Không thể lưu đơn hàng.")

    def open_table_window(self):
        choose_table_window(self.root, self.set_selected_table)

    def set_selected_table(self, table_number):
        self.selected_table = table_number
        table_info = get_table_by_id(table_number)
        if table_info and table_info[1] == 'occupied':
            messagebox.showwarning("Thông báo", f"Bàn {table_number} hiện đang bận. Vui lòng chọn bàn khác.")
            self.selected_table = None
        else:
            self.label_selected.configure(text=f"Bàn đã chọn: {table_number}")
            self.show_all_categories()  # Cập nhật giao diện với "Thực đơn"

if __name__ == "__main__":
    root = ctk.CTk()
    app = MenuForGuest(root)
    root.mainloop()