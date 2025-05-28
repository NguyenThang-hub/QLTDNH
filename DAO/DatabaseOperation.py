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

def reset_table_status():
    conn = connect_db()
    if not conn:
        print("Cannot connect to database to reset table status.")
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE tables SET status = 'available'")
        conn.commit()
        print("All tables reset to 'available'.")
        return True
    except Error as e:
        print(f"Error resetting table status: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def save_order(username, total_price, items, table_id):
    conn = connect_db()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tables WHERE table_number = %s", (table_id,))
        if not cursor.fetchone():
            print(f"Error: table_number {table_id} không tồn tại trong bảng tables")
            return None
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO orders (username, total_price, order_date, table_id) VALUES (%s, %s, %s, %s)",
            (username, total_price, order_date, table_id)
        )
        order_id = cursor.lastrowid
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

def get_table_by_id(table_id):
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT table_number, status FROM tables WHERE table_number = %s", (table_id,))
            result = cursor.fetchone()
            return result
    except Error as e:
        print(f"Error fetching table: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()

def update_table_status(table_id, status):
    conn = connect_db()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE tables SET status = %s WHERE table_number = %s", (status, table_id))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Lỗi cập nhật trạng thái bàn: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Các hàm khác giữ nguyên
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
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, category FROM menu_items")
        rows = cursor.fetchall()
        food_items = []
        drink_items = []
        for name, price, category in rows:
            item = {"name": name, "price": price}
            if category == "food":
                food_items.append(item)
            elif category == "drink":
                drink_items.append(item)
        return food_items, drink_items
    except Error as e:
        print(f"Lỗi khi lấy menu: {e}")
        return [], []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

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

def execute_query_fetchall(query, params=None):
    conn = connect_db()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute(query, params if params else ())
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Lỗi khi thực thi truy vấn: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_order_items():
    query = "SELECT item_name, quantity FROM order_items"
    return execute_query_fetchall(query)

def get_table_status():
    conn = connect_db()
    if not conn:
        return {}
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT table_number, status FROM tables")
        tables = cursor.fetchall()
        return {table[0]: table[1] for table in tables}
    except Error as e:
        print(f"Lỗi khi lấy trạng thái bàn: {e}")
        return {}
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_all_tables():
    query = "SELECT id, name, status FROM tables"
    return execute_query_fetchall(query)

def add_menu_item(name, price, category):
    conn = connect_db()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO menu_items (name, price, category) VALUES (%s, %s, %s)",
                       (name, price, category))
        conn.commit()
        return True
    except Error as e:
        print(f"Lỗi thêm món: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def update_menu_item(item_id, name, price, category):
    conn = connect_db()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE menu_items SET name = %s, price = %s, category = %s WHERE id = %s",
            (name, price, category, item_id)
        )
        conn.commit()
        return True
    except Error as e:
        print(f"Lỗi cập nhật món: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def delete_menu_item(item_id):
    conn = connect_db()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM menu_items WHERE id = %s", (item_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Lỗi xoá món: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def insert_order(table_id, items_dict):
    conn = connect_db()
    if not conn:
        return None
    try:
        cursor = conn.cursor()

        # MySQL dùng %s thay vì ?
        cursor.execute("INSERT INTO orders (table_id, order_date) VALUES (%s, NOW())", (table_id,))
        order_id = cursor.lastrowid

        for item_name, quantity in items_dict.items():
            cursor.execute(
                "INSERT INTO order_items (order_id, item_name, quantity) VALUES (%s, %s, %s)",
                (order_id, item_name, quantity)
            )

        conn.commit()
        return order_id
    except Error as e:
        print(f"Lỗi insert_order: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def get_all_orders_with_items():
    conn = connect_db()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.id AS order_id, o.table_id, o.total_price, o.order_date, 
                   oi.item_name, oi.quantity, oi.price 
            FROM orders o 
            JOIN order_items oi ON o.id = oi.order_id
            ORDER BY o.order_date DESC
        """)
        rows = cursor.fetchall()

        # Gom đơn hàng theo order_id
        orders = {}
        for row in rows:
            oid = row['order_id']
            if oid not in orders:
                orders[oid] = {
                    "table_id": row['table_id'],
                    "total_price": row['total_price'],
                    "order_date": row['order_date'],
                    "items": []
                }
            orders[oid]["items"].append({
                "name": row["item_name"],
                "quantity": row["quantity"],
                "price": row["price"]
            })
        return orders.values()
    except Error as e:
        print("Lỗi lấy đơn hàng:", e)
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
