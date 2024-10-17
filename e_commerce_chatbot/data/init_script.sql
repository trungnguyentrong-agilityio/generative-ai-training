CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

INSERT INTO categories (name) VALUES
('Electronics'),
('Clothing'),
('Home & Kitchen'),
('Beauty & Personal Care'),
('Books & Media');

CREATE TABLE IF NOT EXISTS sub_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    category_id INTEGER REFERENCES categories(id),
    UNIQUE (name, category_id)
);

INSERT INTO sub_categories (name, category_id) VALUES
('smartphones', 1),
('laptops', 1),
('tablets', 1),
('cameras', 1),
('headphones', 1),
('smartwatches', 1),
('men''s apparel', 2),
('women''s apparel', 2),
('kids'' apparel', 2),
('appliances', 3),
('furniture', 3),
('decor', 3),
('makeup', 4),
('skincare', 4),
('hair care', 4),
('books', 5),
('media', 5);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    sub_category_id INTEGER REFERENCES sub_categories(id)
);

CREATE TABLE IF NOT EXISTS payment_methods (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO payment_methods (name) VALUES
('Credit/Debit Card'),
('PayPal'),
('Apple Pay'),
('Google Pay');

CREATE TABLE order_process_steps (
    id SERIAL PRIMARY KEY,
    step_number INTEGER NOT NULL,
    description TEXT NOT NULL,
    UNIQUE (step_number)
);

INSERT INTO order_process_steps (step_number, description) VALUES
(1, 'Browse and select products'),
(2, 'Add products to cart'),
(3, 'Proceed to checkout'),
(4, 'Enter shipping and billing information'),
(5, 'Choose payment method'),
(6, 'Review and confirm order'),
(7, 'Order placed successfully');

CREATE ROLE readonly;
GRANT CONNECT ON DATABASE e_commerce_db TO readonly;
GRANT USAGE ON SCHEMA public TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly;

CREATE USER read_only_user WITH PASSWORD 'read_only_password';
GRANT readonly TO read_only_user;
