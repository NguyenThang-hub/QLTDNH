import pandas as pd
import numpy as np
from DAO.DatabaseOperation import *

# Trả về Series doanh thu theo tháng
def get_monthly_revenue():
    orders = get_orders()
    if not orders:
        return pd.Series(dtype='float64')

    df = pd.DataFrame(orders, columns=['order_date', 'total_price'])
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce')

    if df['total_price'].isna().all():
        return pd.Series(dtype='float64')

    df['year_month'] = df['order_date'].dt.to_period('M')
    monthly_revenue = df.groupby('year_month')['total_price'].sum()
    return monthly_revenue

# Trả về DataFrame món gọi nhiều nhất
def get_top_items():
    conn = connect_db()
    if not conn:
        return pd.DataFrame(columns=["item_name", "quantity"])

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT item_name, SUM(quantity) FROM order_items GROUP BY item_name")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=["item_name", "quantity"])
        return df.sort_values(by="quantity", ascending=False)
    except Exception as e:
        print("Lỗi:", e)
        return pd.DataFrame(columns=["item_name", "quantity"])
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Nếu bạn có bảng đánh giá món, bạn có thể làm tương tự
def get_dish_ratings():
    # Ví dụ giả định
    return pd.DataFrame({
        "item_name": ["Phở", "Bún bò", "Cơm sườn", "Trà đào"],
        "rating": [4.5, 4.2, 4.8, 3.9]
    })
