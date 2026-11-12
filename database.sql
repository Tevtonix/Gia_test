-- DDL & DML Скрипт восстановления БД "velo_drive"
CREATE DATABASE velo_drive;
\c velo_drive;

DROP TABLE IF EXISTS order_product CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS role CASCADE;
DROP TABLE IF EXISTS pickup_point CASCADE;
DROP TABLE IF EXISTS order_status CASCADE;
DROP TABLE IF EXISTS category CASCADE;
DROP TABLE IF EXISTS manufacturer CASCADE;
DROP TABLE IF EXISTS supplier CASCADE;
DROP TABLE IF EXISTS unit CASCADE;

CREATE TABLE role (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    role_id INT NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    login VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    CONSTRAINT fk_user_role FOREIGN KEY (role_id) REFERENCES role(id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE pickup_point (
    id INT PRIMARY KEY,
    address VARCHAR(255) NOT NULL
);

CREATE TABLE order_status (
    id SERIAL PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE manufacturer (
    id SERIAL PRIMARY KEY,
    manufacturer_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE supplier (
    id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE unit (
    id SERIAL PRIMARY KEY,
    unit_name VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE product (
    sku VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    unit_id INT NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK(price >= 0),
    supplier_id INT NOT NULL,
    manufacturer_id INT NOT NULL,
    category_id INT NOT NULL,
    discount INT NOT NULL DEFAULT 0 CHECK(discount >= 0 AND discount <= 100),
    quantity_in_stock INT NOT NULL DEFAULT 0 CHECK(quantity_in_stock >= 0),
    description TEXT,
    photo VARCHAR(255),
    CONSTRAINT fk_product_unit FOREIGN KEY (unit_id) REFERENCES unit(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_product_supplier FOREIGN KEY (supplier_id) REFERENCES supplier(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_product_manufacturer FOREIGN KEY (manufacturer_id) REFERENCES manufacturer(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_product_category FOREIGN KEY (category_id) REFERENCES category(id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE orders (
    id INT PRIMARY KEY,
    order_date DATE NOT NULL,
    delivery_date DATE NOT NULL,
    pickup_point_id INT NOT NULL,
    client_id INT NOT NULL,
    pickup_code INT NOT NULL,
    status_id INT NOT NULL,
    CONSTRAINT fk_order_pickup FOREIGN KEY (pickup_point_id) REFERENCES pickup_point(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_order_client FOREIGN KEY (client_id) REFERENCES "user"(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_order_status FOREIGN KEY (status_id) REFERENCES order_status(id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE order_product (
    order_id INT NOT NULL,
    product_sku VARCHAR(50) NOT NULL,
    quantity INT NOT NULL CHECK(quantity > 0),
    PRIMARY KEY (order_id, product_sku),
    CONSTRAINT fk_op_order FOREIGN KEY (order_id) REFERENCES orders(id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_op_product FOREIGN KEY (product_sku) REFERENCES product(sku) ON UPDATE CASCADE ON DELETE RESTRICT
);

INSERT INTO role (id, role_name) VALUES
(1, 'Администратор'), (2, 'Менеджер'), (3, 'Авторизированный клиент');

INSERT INTO "user" (id, role_id, full_name, login, password) VALUES
(1, 1, 'Никифорова Весения Николаевна', '94d5ous@gmail.com', 'uzWC67'),
(2, 1, 'Сазонов Руслан Германович', 'uth4iz@mail.com', '2L6KZG'),
(3, 1, 'Одинцов Серафим Артёмович', '5d4zbu@tutanota.com', 'rwVDh9'),
(4, 2, 'Ситдикова Елена Анатольевна', 'ptec8ym@yahoo.com', 'LdNyos'),
(5, 2, 'Ворсин Петр Евгеньевич', '1qz4kw@mail.com', 'gynQMT'),
(6, 2, 'Старикова Елена Павловна', '4np6se@mail.com', 'AtnDjr'),
(7, 3, 'Никифорова Анна Семеновна', 'yzls62@outlook.com', 'JlFRCZ'),
(8, 3, 'Стелина Евгения Петровна', '1diph5e@tutanota.com', '8ntwUp'),
(9, 3, 'Михайлюк Анна Вячеславовна', 'tjde7c@yahoo.com', 'YOyhfR'),
(10, 3, 'Степанов Михаил Артёмович', 'wpmrc3do@tutanota.com', 'RSbvHv');

INSERT INTO pickup_point (id, address) VALUES
(1, '420151, г. Лесной, ул. Вишневая, 32'), (2, '125061, г. Лесной, ул. Подгорная, 8'),
(3, '630370, г. Лесной, ул. Шоссейная, 24'), (4, '400562, г. Лесной, ул. Зеленая, 32'),
(5, '614510, г. Лесной, ул. Маяковского, 47'), (6, '410542, г. Лесной, ул. Светлая, 46'),
(7, '620839, г. Лесной, ул. Цветочная, 8'), (8, '443890, г. Лесной, ул. Коммунистическая, 1'),
(9, '603379, г. Лесной, ул. Спортивная, 46'), (10, '603721, г. Лесной, ул. Гоголя, 41'),
(11, '410172, г. Лесной, ул. Северная, 13'), (12, '614611, г. Лесной, ул. Молодежная, 50'),
(13, '454311, г.Лесной, ул. Новая, 19'), (14, '660007, г.Лесной, ул. Октябрьская, 19'),
(15, '603036, г. Лесной, ул. Садовая, 4'), (16, '394060, г.Лесной, ул. Фрунзе, 43'),
(17, '410661, г. Лесной, ул. Школьная, 50'), (18, '625590, г. Лесной, ул. Коммунистическая, 20'),
(19, '625683, г. Лесной, ул. 8 Марта'), (20, '450983, г.Лесной, ул. Комсомольская, 26'),
(21, '394782, г. Лесной, ул. Чехова, 3'), (22, '603002, г. Лесной, ул. Дзержинского, 28'),
(23, '450558, г. Лесной, ул. Набережная, 30'), (24, '344288, г. Лесной, ул. Чехова, 1'),
(25, '614164, г.Лесной, ул. Степная, 30'), (26, '394242, г. Лесной, ул. Коммунистическая, 43'),
(27, '660540, г. Лесной, ул. Солнечная, 25'), (28, '125837, г. Лесной, ул. Шоссейная, 40'),
(29, '125703, г. Лесной, ул. Партизанская, 49'), (30, '625283, г. Лесной, ул. Победы, 46'),
(31, '614753, г. Лесной, ул. Полевая, 35'), (32, '426030, г. Лесной, ул. Маяковского, 44'),
(33, '450375, г. Лесной ул. Клубная, 44'), (34, '625560, г. Лесной, ул. Некрасова, 12'),
(35, '630201, г. Лесной, ул. Комсомольская, 17'), (36, '190949, г. Лесной, ул. Мичурина, 26');

INSERT INTO order_status (id, status_name) VALUES (1, 'Новый'), (2, 'Завершен');
INSERT INTO unit (id, unit_name) VALUES (1, 'шт.');

INSERT INTO supplier (id, supplier_name) VALUES
(1, 'ВелоСтрана'), (2, 'ЯндексМаркет'), (3, 'Скилс'), (4, 'ПерспективаГрупп'), (5, 'kari');

INSERT INTO manufacturer (id, manufacturer_name) VALUES
(1, 'Slash'), (2, 'Shimano'), (3, 'Skill bike'), (4, 'NEXT'), (5, 'Aero'), (6, 'Fizard'), (7, 'kari');

INSERT INTO category (id, category_name) VALUES
(1, 'Велосипед взрослый горный'), (2, 'Велосипед городской подростковый'),
(3, 'Велосипед городской взрослый'), (4, 'Велосипед детский горный'),
(5, 'Велосипед детский городской');

INSERT INTO product (sku, product_name, unit_id, price, supplier_id, manufacturer_id, category_id, discount, quantity_in_stock, description, photo) VALUES
('А112Т4', 'Велосипед взрослый горный Slash Stream 27.5 колеса (2025) 17" Черный (162-172 см)', 1, 19775.00, 1, 1, 1, 30, 15, 'Горный велосипед Slash Stream 27.5 (2025) – легкий и надежный компаньон для поездок по пересеченной местности. Мощные шатуны интенсивно передают усилия мышц на вал каретки.', '1.jpg'),
('G843H5', 'Велосипед взрослый горный Slash Stream 27.5 колеса (2025) 19" Синий (172-182 см)', 1, 19791.00, 1, 1, 1, 30, 9, 'В комплектацию включены дисковые механические тормоза RPT DSC-310. Особый упор разработчики рамы данной модели сделали на увеличение прочности мест наибольшей нагрузки.', '2.jpg'),
('D325D4', 'Велосипед городской подростковый серый', 1, 9919.00, 2, 2, 2, 5, 12, 'Городской подростковый велосипед - идеальный выбор для активного образа жизни! Откройте для себя комфорт и свободу передвижения с нашим стильным городским велосипедом.', '3.jpg'),
('S432T5', 'Велосипед Skill Bike 3051, городской, 21 скорость, сталь, 29" колеса, черно-красный', 1, 16442.00, 3, 3, 3, 15, 15, 'SKILL BIKE модель 3051 - горный велосипед на спицах, обеспечивающий уверенную и комфортную езду как по городским улицам, так и по горной местности.', '4.jpg'),
('F325D4', 'Велосипед Skillbike 3052, горный, складной, рама 17 дюймов, колеса 26 дюймов, 21 скорость', 1, 17985.00, 3, 3, 1, 18, 50, 'SKILL BIKE модель 3052 - велосипед складной, предназначен для тех, кто ценит комфорт, стиль и максимальную мобильность. Горный велосипед легко помещается в багажник и идеально подходит для активных поездок в городской суете.', '5.jpg'),
('G432G6', 'Велосипед Skill Bike 3053, горный, двухподвесный, рама 17 дюймов, колеса 26 дюймов, 21 скорость', 1, 17621.00, 3, 3, 1, 20, 0, 'SKILL BIKE модель 3053 - горный велосипед на литых дисках, имеет амортизаторы как на переднем, так и на заднем колесе.', '6.jpg'),
('H542F5', 'Велосипед MILANO M300, горный, для взрослых, 26", 7 скоростей', 1, 13509.00, 4, 4, 1, 4, 5, 'Горный велосипед MILANO M300 с диаметром колес 26 дюйма подойдет для подростков и взрослых, без усилий позволит преодолевать любые непроходимые каменистые поверхности и зоны бездорожья.', '7.jpg'),
('C346F5', 'Горный велосипед скоростной, колёса 24", рама - 14", черно-красный', 1, 15212.00, 4, 5, 4, 5, 4, 'Горный велосипед – это надежный и стильный выбор для любителей активного отдыха. Удобное седло из искусственной кожи и наличие подножки добавляют удобства во время поездок.', '8.jpg'),
('F256G6', '26" Велосипед Fizard, 15" алюминий, дисковые тормоза, 21 скорость, серый', 1, 15126.00, 4, 6, 4, 25, 3, 'Горный велосипед Fizard — надёжный универсальный маунтинбайк для города и бездорожья.', '9.jpg'),
('J532V5', 'Велосипед двухколесный детский 14 дюймов, со светящимися колесами, черный', 1, 6417.00, 5, 7, 5, 8, 6, 'Велосипед двухколесный детский 14 дюймов от Kari - это надежный и безопасный транспорт для вашего ребенка.', NULL);

INSERT INTO orders (id, order_date, delivery_date, pickup_point_id, client_id, pickup_code, status_id) VALUES
(1, '2023-02-27', '2023-04-20', 1, 10, 901, 1),
(2, '2022-09-28', '2023-04-21', 11, 1, 902, 1),
(3, '2023-03-21', '2023-04-22', 2, 2, 903, 1),
(4, '2023-02-20', '2023-04-23', 11, 3, 904, 2),
(5, '2023-03-17', '2023-04-24', 2, 10, 905, 2),
(6, '2023-03-01', '2023-04-25', 15, 1, 906, 2),
(7, '2023-02-28', '2023-04-26', 3, 2, 907, 2),
(8, '2023-03-31', '2023-04-27', 19, 3, 908, 1),
(9, '2023-04-02', '2023-04-28', 5, 10, 909, 1),
(10, '2023-04-03', '2023-04-29', 19, 10, 910, 1);

INSERT INTO order_product (order_id, product_sku, quantity) VALUES
(1, 'А112Т4', 2), (1, 'G843H5', 2),
(2, 'G843H5', 1), (2, 'А112Т4', 1),
(3, 'D325D4', 10), (3, 'S432T5', 10),
(4, 'F325D4', 5), (4, 'D325D4', 4),
(5, 'G432G6', 20), (5, 'H542F5', 20),
(6, 'А112Т4', 2), (6, 'G843H5', 2),
(7, 'C346F5', 3), (7, 'F256G6', 3),
(8, 'F325D4', 1), (8, 'G432G6', 1),
(9, 'J532V5', 5), (9, 'F256G6', 1),
(10, 'F256G6', 5), (10, 'J532V5', 5);