-- Tạo database
CREATE DATABASE IF NOT EXISTS userdb;
USE userdb;

-- Tạo bảng users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- thêm tài khoản phục vụ 
INSERT INTO users (username, password)
VALUES ('PV', SHA2('123', 256));



-- Tạo bảng orders
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    total_price DECIMAL(10, 2),
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tạo bảng order_items
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    item_name VARCHAR(50),
    quantity INT,
    price DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);
  

CREATE TABLE IF NOT EXISTS ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(50),
    rating INT CHECK (rating >= 1 AND rating <= 5)
);
-- Bảng bàn ăn
CREATE TABLE IF NOT EXISTS tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_number INT UNIQUE NOT NULL,
    status ENUM('available', 'occupied') DEFAULT 'available'
);
select * from users;
CREATE TABLE menu_items (
    id INTEGER PRIMARY KEY auto_increment,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    category TEXT CHECK(category IN ('food', 'drink')) NOT NULL
);
insert into menu_items values (2, 'Burger', 120000, 'food'), (3, 'Mì ý', 118000, 'food'), (4, 'Pizza', 158000, 'food'), (5, 'Salad', 101000, 'food'), (6, 'Beefsteak', 128000, 'food');
insert into menu_items values (8, 'Coca Cola', 20000, 'drink'), (9, 'Soda Chanh', 18000, 'drink'), (10, 'Nước ép dưa hấu', 23000, 'drink'), (11, 'Nước ép chanh dây', 23000, 'drink'), (12, 'Rượu vang đỏ', 100000, 'drink');
select * from menu_items;


ALTER TABLE users ADD COLUMN email TEXT;
Update users set email = 'default@gmail.com' where email is null;


ALTER TABLE tables ADD COLUMN name TEXT;
INSERT INTO tables (table_number, name, status) VALUES
(1, 'Bàn 1', 'available'),
(2, 'Bàn 2', 'available'),
(3, 'Bàn 3', 'available'),
(4, 'Bàn 4', 'available'),
(5, 'Bàn 5', 'available'),
(6, 'Bàn 6', 'available'),
(7, 'Bàn 7', 'available'),
(8, 'Bàn 8', 'available'),
(9, 'Bàn 9', 'available'),
(10, 'Bàn 10', 'available'),
(11, 'Bàn 11', 'available'),
(12, 'Bàn 12', 'available'),
(13, 'Bàn 13', 'available'),
(14, 'Bàn 14', 'available'),
(15, 'Bàn 15', 'available'),
(16, 'Bàn 16', 'available'),
(17, 'Bàn 17', 'available'),
(18, 'Bàn 18', 'available'),
(19, 'Bàn 19', 'available'),
(20, 'Bàn 20', 'available');

select * from tables;
ALTER TABLE orders ADD COLUMN table_id INT;
ALTER TABLE orders ADD FOREIGN KEY (table_id) REFERENCES tables(id);	
alter table ratings drop column item_name;
alter table ratings add column menu_id int;
alter table ratings add foreign key(menu_id) references menu_items(id);

alter table orders add column user_id int;
alter table orders add foreign key(user_id) references users(id);

alter table order_items add column menu_id int;
alter table order_items add foreign key(menu_id) references menu_items(id);
-- Kiểm tra dữ liệu
SELECT * FROM tables;	
DROP DATABASE userdb;
