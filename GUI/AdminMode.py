import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Report import get_monthly_revenue, get_top_items, get_dish_ratings

class AdminMode(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Chế độ quản lý")
        self.geometry("1100x700")
        self.configure(bg="#f5f5f5")

        self.create_layout()

    def create_layout(self):
        title = ctk.CTkLabel(self, text="Tổng quan hoạt động nhà hàng", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=15)

        # Top row - 3 small widgets
        top_frame = ctk.CTkFrame(self, fg_color="white")
        top_frame.pack(pady=10, padx=20, fill="x")

        for text in ["Tổng số đơn", "Tổng doanh thu", "Món phổ biến"]:
            box = ctk.CTkFrame(top_frame, width=200, height=100)
            box.pack(side="left", padx=15, pady=10, expand=True, fill="both")
            ctk.CTkLabel(box, text=text, font=ctk.CTkFont(size=16)).pack(pady=15)

        # Middle row - two large charts
        middle_frame = ctk.CTkFrame(self, fg_color="white")
        middle_frame.pack(padx=20, pady=10, fill="both", expand=True)

        left_chart = ctk.CTkFrame(middle_frame)
        left_chart.pack(side="left", padx=10, fill="both", expand=True)
        self.plot_monthly_revenue(left_chart)

        right_chart = ctk.CTkFrame(middle_frame)
        right_chart.pack(side="right", padx=10, fill="both", expand=True)
        self.plot_top_items(right_chart)

        # Bottom row - quality chart (fake data for now)
        bottom_frame = ctk.CTkFrame(self, fg_color="white")
        bottom_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.plot_dish_quality(bottom_frame)

    def plot_monthly_revenue(self, frame):
        revenue = get_monthly_revenue()
        fig, ax = plt.subplots(figsize=(5, 3))
        if revenue.empty:
            ax.text(0.5, 0.5, "Không có dữ liệu", ha="center", va="center")
        else:
            revenue.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title("Doanh thu theo tháng")
            ax.set_ylabel("VNĐ")
            ax.grid(True, axis='y')

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_top_items(self, frame):
        df = get_top_items()
        fig, ax = plt.subplots(figsize=(5, 3))
        if df.empty:
            ax.text(0.5, 0.5, "Không có dữ liệu", ha="center", va="center")
        else:
            ax.barh(df["item_name"], df["quantity"], color="orange")
            ax.set_title("Món ăn được chọn nhiều nhất")
            ax.set_xlabel("Số lượng")
            ax.invert_yaxis()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_dish_quality(self, frame):
        df = get_dish_ratings()
        fig, ax = plt.subplots(figsize=(6, 3))
        if df.empty:
            ax.text(0.5, 0.5, "Không có dữ liệu đánh giá", ha="center", va="center")
        else:
            ax.bar(df["item_name"], df["rating"], color="green")
            ax.set_ylim(0, 5)
            ax.set_title("Đánh giá chất lượng món ăn")
            ax.set_ylabel("Điểm (0-5)")
            ax.grid(True, axis='y')

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

# Để gọi từ MenuApp:
# from AdminMode import AdminMode
# def open_admin():
#     AdminMode()
