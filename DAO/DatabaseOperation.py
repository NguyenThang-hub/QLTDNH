import mysql.connector
from mysql.connector import Error
from datetime import datetime

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Thang@12345",
            database="userdb"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def save_order(username, total_price, items, table_number):
    conn = connect_db()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        # Lưu đơn hàng (bao gồm table_number và order_date)
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO orders (username, total_price, table_number, order_date) VALUES (%s, %s, %s, %s)",
            (username, total_price, table_number, order_date)
        )
        order_id = cursor.lastrowid
        # Lưu chi tiết món
        for item in items:
            cursor.execute(
                "INSERT INTO order_items (order_id, item_name, quantity, price) VALUES (%s, %s, %s, %s)",
                (order_id, item["name"], item["quantity"], item["price"])
            )
        # Cập nhật trạng thái bàn thành 'occupied'
        cursor.execute(
            "UPDATE tables SET status = 'occupied' WHERE number = %s",
            (table_number,)
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
    conn = connect_db()
    if not conn:
        return [], []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name, price, category FROM menu_items")
        rows = cursor.fetchall()

        food_items = []
        drink_items = []
        for item in rows:
            if item["category"] == "food":
                food_items.append({"name": item["name"], "price": item["price"]})
            elif item["category"] == "drink":
                drink_items.append({"name": item["name"], "price": item["price"]})
        return food_items, drink_items
    except Error as e:
        print(f"Error retrieving menu items: {e}")
        return [], []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_items_by_category(category):
    conn = connect_db()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name, price FROM menu_items WHERE category = %s", (category,))
        items = cursor.fetchall()
        return items
    except Error as e:
        print(f"Error retrieving items: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_tables_by_area(area):
    conn = connect_db()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        if area == "all":
            query = "SELECT id, number, area FROM tables WHERE status = 'available'"
            cursor.execute(query)
        else:
            query = "SELECT id, number, area FROM tables WHERE area = %s AND status = 'available'"
            cursor.execute(query, (area,))
        tables = cursor.fetchall()
        return tables
    except Error as e:
        print(f"Error fetching tables: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()