import customtkinter as ctk
from tkinter import messagebox

def choose_table_window(root, callback_select_table):
    table_win = ctk.CTkToplevel(root)
    table_win.title("Chọn bàn")
    table_win.geometry("600x500")

    ctk.CTkLabel(table_win, text="Chọn bàn", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

    main_frame = ctk.CTkFrame(table_win)
    main_frame.pack(pady=10, padx=10, fill="both", expand=True)

    indoor_frame = ctk.CTkFrame(main_frame)
    outdoor_frame = ctk.CTkFrame(main_frame)

    indoor_frame.pack(side="left", expand=True, padx=10, pady=10, fill="both")
    outdoor_frame.pack(side="right", expand=True, padx=10, pady=10, fill="both")

    ctk.CTkLabel(indoor_frame, text="Trong nhà", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
    ctk.CTkLabel(outdoor_frame, text="Ngoài trời", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

    def select_table(table_number):
        callback_select_table(table_number)
        messagebox.showinfo("Bàn được chọn", f"Bạn đã chọn bàn số {table_number}")
        table_win.destroy()

    def create_table_button(parent, table_number):
        return ctk.CTkButton(
            parent,
            text=f"Bàn {table_number}",
            width=80,
            command=lambda: select_table(table_number)
        )

    for i in range(1, 13):
        create_table_button(indoor_frame, i).pack(padx=5, pady=5)

    for i in range(13, 21):
        create_table_button(outdoor_frame, i).pack(padx=5, pady=5)
