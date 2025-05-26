import customtkinter as ctk
from tkinter import messagebox
from DAO.DatabaseOperation import get_items_by_category, add_item, update_item, delete_item

class ItemManager(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.title("Quản lý món ăn")
        self.geometry("800x600")

        self.food_items = []
        self.drink_items = []

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.refresh_data()

        ctk.CTkButton(self, text="↩️ Quay lại thống kê", command=self.back_to_admin).pack(pady=10)

    def back_to_admin(self):
        self.destroy()
        if self.parent:
            self.parent.deiconify()  # Hiện lại AdminMode

    def refresh_data(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.food_items = get_items_by_category("food")
        self.drink_items = get_items_by_category("drink")

        ctk.CTkLabel(self.main_frame, text="🍽️ Món ăn", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 5))
        for item in self.food_items:
            self.create_item_row(item)

        ctk.CTkLabel(self.main_frame, text="🥤 Đồ uống", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(15, 5))
        for item in self.drink_items:
            self.create_item_row(item)

        ctk.CTkButton(self.main_frame, text="➕ Thêm món", command=self.add_item_popup).pack(pady=10)

    def create_item_row(self, item):
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", pady=5)

        ctk.CTkLabel(frame, text=item['name'], width=200).pack(side="left", padx=5)
        ctk.CTkLabel(frame, text=f"{item['price']:,} VNĐ", width=100).pack(side="left", padx=5)
        ctk.CTkLabel(frame, text=item['category'], width=80).pack(side="left", padx=5)

        ctk.CTkButton(frame, text="✏️ Sửa", width=80, command=lambda: self.edit_item_popup(item)).pack(side="right", padx=5)
        ctk.CTkButton(frame, text="🗑️ Xoá", width=80, command=lambda: self.delete_item(item)).pack(side="right", padx=5)

    def add_item_popup(self):
        self.item_popup("Thêm món", on_confirm=add_item)

    def edit_item_popup(self, item):
        def update_func(name, price, category):
            update_item(item['id'], name, price, category)
        self.item_popup("Sửa món", item=item, on_confirm=update_func)

    def item_popup(self, title, item=None, on_confirm=None):
        popup = ctk.CTkToplevel(self)
        popup.title(title)
        popup.geometry("300x250")

        name_var = ctk.StringVar(value=item['name'] if item else "")
        price_var = ctk.StringVar(value=str(item['price']) if item else "")
        category_var = ctk.StringVar(value=item['category'] if item else "food")

        ctk.CTkLabel(popup, text="Tên món").pack(pady=5)
        name_entry = ctk.CTkEntry(popup, textvariable=name_var)
        name_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Giá (VNĐ)").pack(pady=5)
        price_entry = ctk.CTkEntry(popup, textvariable=price_var)
        price_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Loại").pack(pady=5)
        category_combo = ctk.CTkComboBox(popup, values=["food", "drink"], variable=category_var)
        category_combo.pack(pady=5)

        def confirm():
            name = name_var.get()
            try:
                price = int(price_var.get())
                category = category_var.get()
                if name and category in ["food", "drink"]:
                    on_confirm(name, price, category)
                    messagebox.showinfo("Thành công", f"{title} thành công!")
                    popup.destroy()
                    self.refresh_data()
                else:
                    messagebox.showwarning("Lỗi", "Dữ liệu không hợp lệ.")
            except ValueError:
                messagebox.showwarning("Lỗi", "Giá phải là số.")

        ctk.CTkButton(popup, text="✅ Xác nhận", command=confirm).pack(pady=10)

    def delete_item(self, item):
        confirm = messagebox.askyesno("Xác nhận xoá", f"Bạn có chắc muốn xoá {item['name']}?")
        if confirm:
            delete_item(item['id'])
            self.refresh_data()
