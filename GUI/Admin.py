from tkinter import messagebox
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Report import get_monthly_revenue, get_top_items, get_dish_ratings
from DAO.DatabaseOperation import add_menu_item, update_menu_item, delete_menu_item, execute_query_fetchall

class AdminMode(ctk.CTkToplevel):
    def __init__(self, master=None, refresh_menu_callback=None):
        super().__init__(master)
        self.refresh_menu_callback = refresh_menu_callback
        self.title("Chế độ quản lý")
        self.geometry("1100x700")
        self.configure(bg="white")

        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        self.main_area = ctk.CTkFrame(self, fg_color="white")
        self.main_area.pack(side="right", expand=True, fill="both", padx=5, pady=5)

        # Sidebar buttons
        ctk.CTkButton(self.sidebar, text="Thống kê", command=self.show_statistics).pack(pady=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Thêm món", command=self.open_add_window).pack(pady=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Sửa món", command=self.open_edit_window).pack(pady=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Xoá món", command=self.open_delete_window).pack(pady=10, fill="x")
        ctk.CTkButton(self.sidebar, text="❌ Thoát", command=self.destroy).pack(pady=10)


        self.show_statistics()

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def show_statistics(self):
        self.clear_main_area()

        # Monthly revenue
        frame1 = ctk.CTkFrame(self.main_area)
        frame1.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        revenue = get_monthly_revenue()
        fig1, ax1 = plt.subplots(figsize=(5, 3))
        if revenue.empty:
            ax1.text(0.5, 0.5, "Không có dữ liệu", ha="center", va="center")
        else:
            revenue.plot(kind='bar', ax=ax1, color='skyblue')
            ax1.set_title("Doanh thu theo tháng")
        canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)

        # Top items
        frame2 = ctk.CTkFrame(self.main_area)
        frame2.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        top_items = get_top_items()
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        if top_items.empty:
            ax2.text(0.5, 0.5, "Không có dữ liệu", ha="center", va="center")
        else:
            ax2.barh(top_items["item_name"], top_items["quantity"], color="orange")
            ax2.set_title("Món phổ biến")
        canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)

        # Dish quality
        frame3 = ctk.CTkFrame(self.main_area)
        frame3.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        ratings = get_dish_ratings()
        fig3, ax3 = plt.subplots(figsize=(5, 3))
        if ratings.empty:
            ax3.text(0.5, 0.5, "Không có đánh giá", ha="center", va="center")
        else:
            ax3.bar(ratings["item_name"], ratings["rating"], color="green")
            ax3.set_ylim(0, 5)
            ax3.set_title("Chất lượng món ăn")
        canvas3 = FigureCanvasTkAgg(fig3, master=frame3)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill="both", expand=True)

    def open_add_window(self):
        window = ctk.CTkToplevel(self)
        window.title("Thêm món mới")
        window.geometry("300x300")

        name_entry = ctk.CTkEntry(window, placeholder_text="Tên món")
        name_entry.pack(pady=10)
        price_entry = ctk.CTkEntry(window, placeholder_text="Giá")
        price_entry.pack(pady=10)
        category_option = ctk.CTkOptionMenu(window, values=["food", "drink"])
        category_option.pack(pady=10)

        def add():
            name = name_entry.get()
            price = price_entry.get()
            category = category_option.get()
            if name and price.isdigit():
                if add_menu_item(name, int(price), category):
                    if self.refresh_menu_callback:
                        self.refresh_menu_callback()
                    window.destroy()

        ctk.CTkButton(window, text="Thêm", command=add).pack(pady=10)

    def open_edit_window(self):
        window = ctk.CTkToplevel(self)
        window.title("Sửa món")
        window.geometry("400x400")

        items = execute_query_fetchall("SELECT id, name FROM menu_items")
        item_dict = {f"{name} (ID {id})": id for id, name in items}

        item_menu = ctk.CTkOptionMenu(window, values=list(item_dict.keys()))
        item_menu.pack(pady=10)

        name_entry = ctk.CTkEntry(window, placeholder_text="Tên mới")
        name_entry.pack(pady=10)
        price_entry = ctk.CTkEntry(window, placeholder_text="Giá mới")
        price_entry.pack(pady=10)
        category_option = ctk.CTkOptionMenu(window, values=["food", "drink"])
        category_option.pack(pady=10)

        def edit():
            selected = item_menu.get()
            item_id = item_dict[selected]
            name = name_entry.get()
            price = price_entry.get()
            category = category_option.get()
            if name and price.isdigit():
                if update_menu_item(item_id, name, int(price), category):
                    if self.refresh_menu_callback:
                        self.refresh_menu_callback()
                    window.destroy()

        ctk.CTkButton(window, text="Lưu thay đổi", command=edit).pack(pady=10)

    def open_delete_window(self):
        window = ctk.CTkToplevel(self)
        window.title("Xoá món")
        window.geometry("400x300")

        items = execute_query_fetchall("SELECT id, name FROM menu_items")
        item_dict = {f"{name} (ID {id})": id for id, name in items}

        item_menu = ctk.CTkOptionMenu(window, values=list(item_dict.keys()))
        item_menu.pack(pady=10)

        def delete():
            selected = item_menu.get()
            item_id = item_dict[selected]
            if delete_menu_item(item_id):
                if self.refresh_menu_callback:
                    self.refresh_menu_callback()
                window.destroy()

        ctk.CTkButton(window, text="Xoá", command=delete).pack(pady=10)

