import customtkinter as ctk
from tkinter import messagebox

def choose_table_window(root, callback_select_table):
    table_win = ctk.CTkToplevel(root)
    table_win.title("Chọn bàn")
    table_win.geometry("700x500")  # Kích thước gọn gàng cho bố cục dọc
    table_win.transient(root)  # Liên kết với cửa sổ chính
    table_win.grab_set()  # Chặn tương tác với cửa sổ chính

    # Thiết lập giao diện đơn giản
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Tiêu đề chính
    ctk.CTkLabel(
        table_win,
        text="🍽️ Chọn bàn nhà hàng",
        font=ctk.CTkFont(family="Arial", size=22, weight="bold")
    ).pack(pady=15)

    # Khung chính chứa các khu vực
    main_frame = ctk.CTkFrame(table_win, fg_color="transparent")
    main_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Hàm tạo nút bàn (di chuyển lên trước)
    def create_table_button(parent, table_number):
        button = ctk.CTkButton(
            parent,
            text=f"Bàn {table_number}",
            width=100,
            height=40,
            font=ctk.CTkFont(family="Arial", size=14),
            corner_radius=8,
            fg_color="#4CAF50" if table_number <= 12 else "#0288D1",
            hover_color="#388E3C" if table_number <= 12 else "#0277BD",
            command=lambda: select_table(table_number)
        )
        return button

    # Hàm chọn bàn
    def select_table(table_number):
        callback_select_table(table_number)
        messagebox.showinfo("Bàn được chọn", f"Bạn đã chọn bàn số {table_number}")
        table_win.destroy()

    # === Khu vực Trong nhà (phía trên) ===
    indoor_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="#F5F5F5")
    indoor_frame.pack(fill="x", padx=10, pady=10)

    # Tiêu đề khu vực Trong nhà
    ctk.CTkLabel(
        indoor_frame,
        text="🏠 Trong nhà",
        font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
        text_color="#2E7D32"
    ).pack(pady=10)

    # Bố trí nút theo lưới 3x4 cho Trong nhà
    indoor_button_frame = ctk.CTkFrame(indoor_frame, fg_color="transparent")
    indoor_button_frame.pack(pady=5)
    for i in range(1, 13):
        row = (i - 1) // 4
        col = (i - 1) % 4
        button = create_table_button(indoor_button_frame, i)
        button.grid(row=row, column=col, padx=8, pady=6, sticky="nsew")
    # Cân bằng lưới
    for col in range(4):
        indoor_button_frame.grid_columnconfigure(col, weight=1, uniform="indoor")
    for row in range(3):
        indoor_button_frame.grid_rowconfigure(row, weight=1)

    # === Khu vực Ngoài trời (phía dưới) ===
    outdoor_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="#F5F5F5")
    outdoor_frame.pack(fill="x", padx=10, pady=10)

    # Tiêu đề khu vực Ngoài trời
    ctk.CTkLabel(
        outdoor_frame,
        text="🌳 Ngoài trời",
        font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
        text_color="#0288D1"
    ).pack(pady=10)

    # Bố trí nút theo lưới 2x4 cho Ngoài trời
    outdoor_button_frame = ctk.CTkFrame(outdoor_frame, fg_color="transparent")
    outdoor_button_frame.pack(pady=5)
    for i in range(13, 21):
        row = (i - 13) // 4
        col = (i - 13) % 4
        button = create_table_button(outdoor_button_frame, i)
        button.grid(row=row, column=col, padx=8, pady=6, sticky="nsew")
    # Cân bằng lưới
    for col in range(4):
        outdoor_button_frame.grid_columnconfigure(col, weight=1, uniform="outdoor")
    for row in range(2):
        outdoor_button_frame.grid_rowconfigure(row, weight=1)