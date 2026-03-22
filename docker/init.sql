-- Auto-runs when PostgreSQL container starts for the first time

CREATE TABLE IF NOT EXISTS bills (
    bill_id     SERIAL PRIMARY KEY,
    vendor_name VARCHAR(200),
    amount      NUMERIC(10,2),
    bill_date   DATE,
    file_path   TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id      SERIAL PRIMARY KEY,
    customer_name VARCHAR(200),
    amount        NUMERIC(10,2),
    order_date    DATE,
    status        VARCHAR(50)
);

-- Sample data
INSERT INTO bills (vendor_name, amount, bill_date, file_path) VALUES
('MSEB',              3492.80, '2026-03-01', '/app/data/uploads/bills/electricity_bill_mar2026.txt'),
('Reliance Jio',      1668.82, '2026-03-05', '/app/data/uploads/bills/jio_fiber_mar2026.txt'),
('Sharma Supplies',   5661.60, '2026-02-28', '/app/data/uploads/bills/office_supplies_feb2026.txt'),
('AWS India',         8968.00, '2026-03-10', '/app/data/uploads/bills/aws_india_mar2026.txt');

INSERT INTO orders (customer_name, amount, order_date, status) VALUES
('Ethan Hunt',        320.75, '2026-02-13', 'Shipped'),
('Fiona Gallagher',    89.99, '2026-02-14', 'Pending'),
('George Miller',     560.00, '2026-02-14', 'Delivered'),
('Hannah Davis',       42.50, '2026-02-15', 'Cancelled'),
('Ian Wright',        199.95, '2026-02-15', 'Shipped'),
('Acme Corp',       38083.00, '2026-03-01', 'Delivered'),
('Beta Solutions',  30570.00, '2026-03-05', 'Pending'),
('Gamma Ltd',       56252.00, '2026-03-08', 'Shipped'),
('Delta Pvt Ltd',   29000.00, '2026-03-10', 'Cancelled'),
('Sigma Traders',   83625.00, '2026-03-11', 'Pending');
