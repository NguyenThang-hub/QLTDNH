import mysql.connector
from mysql.connector import Error
from datetime import datetime

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="userdb"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def save_order(username, total_price, items):
    conn = connect_db()
    if not conn:
        return None  # Thay False bằng None để đồng nhất với logic trả về order_id
    try:
        cursor = conn.cursor()
        # Lưu đơn hàng (thêm order_date)
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO orders (username, total_price, order_date) VALUES (%s, %s, %s)",
            (username, total_price, order_date)
        )
        order_id = cursor.lastrowid
        # Lưu chi tiết món
        for item in items:
            cursor.execute(
                "INSERT INTO order_items (order_id, item_name, quantity, price) VALUES (%s, %s, %s, %s)",
                (order_id, item["name"], item["quantity"], item["price"])
            )
        conn.commit()
        return order_id
    except Error as e:
        print(f"Error saving order: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_orders():
    conn = connect_db()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT order_date, total_price FROM orders")
        orders = cursor.fetchall()
        return orders
    except Error as e:
        print(f"Error retrieving orders: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
def get_menu_items():
    conn = connect_db()  # hoặc đường dẫn tới DB của bạn
    cursor = conn.cursor()

    cursor.execute("SELECT name, price, category FROM menu_items")
    rows = cursor.fetchall()

    conn.close()

    # Trả về list phân loại theo category
    food_items = []
    drink_items = []
    for name, price, category in rows:
        item = {"name": name, "price": price}
        if category == "food":
            food_items.append(item)
        elif category == "drink":
            drink_items.append(item)

    return food_items, drink_items
def get_items_by_category(category):
    items = []
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT name, price FROM menu_items WHERE category = %s", (category,))
            items = cursor.fetchall()
    except Error as e:
        print("Lỗi khi lấy dữ liệu:", e)
    finally:
        if conn and conn.is_connected():
            conn.close()
    return items
