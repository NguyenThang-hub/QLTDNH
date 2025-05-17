import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
from db import get_orders


def show_monthly_report():
    # Lấy dữ liệu đơn hàng
    orders = get_orders()
    if not orders:
        messagebox.showinfo("Thông báo", "Chưa có đơn hàng nào!")
        return

    # Pandas: Chuyển dữ liệu thành DataFrame và ép kiểu total_price thành float
    df = pd.DataFrame(orders, columns=['order_date', 'total_price'])
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['total_price'] = pd.to_numeric(df['total_price'],
                                      errors='coerce')  # Ép kiểu thành float, bỏ giá trị không hợp lệ

    # Kiểm tra nếu không có dữ liệu số hợp lệ
    if df['total_price'].isna().all() or df['total_price'].empty:
        messagebox.showinfo("Thông báo", "Dữ liệu doanh thu không hợp lệ hoặc không có giá trị số!")
        return

    # Pandas: Nhóm theo năm-tháng và tính tổng doanh thu
    df['year_month'] = df['order_date'].dt.to_period('M')
    monthly_revenue = df.groupby('year_month')['total_price'].sum()

    # NumPy: Tính trung bình doanh thu mỗi tháng
    avg_revenue = np.mean(monthly_revenue)

    # Chuẩn bị báo cáo văn bản
    report = "Báo cáo doanh thu theo tháng:\n\n"
    for period, revenue in monthly_revenue.items():
        report += f"{period}: {revenue:,.0f} VNĐ\n"

    # Kiểm tra nếu chỉ có dữ liệu một tháng
    if len(monthly_revenue) == 1:
        report += "\nLưu ý: Chỉ có dữ liệu cho một tháng, không thể so sánh với các tháng khác."
    else:
        report += f"\nTrung bình doanh thu mỗi tháng: {avg_revenue:,.0f} VNĐ"

    # Hiển thị báo cáo văn bản
    messagebox.showinfo("Báo cáo doanh thu", report)

    # Matplotlib: Vẽ biểu đồ cột
    plt.figure(figsize=(8, 5))
    monthly_revenue.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Doanh thu theo tháng', fontsize=14, fontweight='bold')
    plt.xlabel('Tháng', fontsize=12)
    plt.ylabel('Doanh thu (VNĐ)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Thêm đường trung bình nếu có nhiều hơn một tháng
    if len(monthly_revenue) > 1:
        plt.axhline(y=avg_revenue, color='red', linestyle='--', label=f'Trung bình: {avg_revenue:,.0f} VNĐ')
        plt.legend()

    plt.tight_layout()

    # Hiển thị biểu đồ
    plt.show()