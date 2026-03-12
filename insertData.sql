CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    amount NUMERIC(10,2),
    order_date DATE,
    status VARCHAR(50)
);

CREATE TABLE bills (
    bill_id INT PRIMARY KEY,
    vendor_name VARCHAR(100),
    amount NUMERIC(10,2),
    bill_date DATE,
    file_path TEXT
);

INSERT INTO orders (order_id, customer_name, amount, order_date, status)
VALUES (5, 'Ethan Hunt', 320.75, '2026-02-13', 'Shipped');

INSERT INTO orders (order_id, customer_name, amount, order_date, status)
VALUES (6, 'Fiona Gallagher', 89.99, '2026-02-14', 'Pending');

INSERT INTO orders (order_id, customer_name, amount, order_date, status)
VALUES (7, 'George Miller', 560.00, '2026-02-14', 'Delivered');

INSERT INTO orders (order_id, customer_name, amount, order_date, status)
VALUES (8, 'Hannah Davis', 42.50, '2026-02-15', 'Cancelled');

INSERT INTO orders (order_id, customer_name, amount, order_date, status)
VALUES (9, 'Ian Wright', 199.95, '2026-02-15', 'Shipped');

INSERT INTO orders (order_id, customer_name, amount, order_date, status)
VALUES (10, 'Ethan Hunt', 320.75, '2025-02-13', 'Shipped');

INSERT INTO orders (order_id, customer_name, amount, order_date, status)
VALUES (11, 'Fiona Gallagher', 89.99, '2025-02-14', 'Pending');

INSERT INTO orders (order_id, customer_name, amount, order_date, status)
VALUES (12, 'George Miller', 560.00, '2024-02-14', 'Delivered');

INSERT INTO orders (order_id, customer_name, amount, order_date, status)
VALUES (13, 'Hannah Davis', 42.50, '2024-02-15', 'Cancelled');

INSERT INTO orders (order_id, customer_name, amount, order_date, status)
VALUES (14, 'Ian Wright', 199.95, '2023-02-15', 'Shipped');





INSERT INTO bills (bill_id, vendor_name, amount, bill_date, file_path)
VALUES (4, 'Gas Company', 85.75, '2026-02-05',
'/home/hadoop/workspace/Agent-LocalDB/Files/bills/gas_feb_2026.pdf');

INSERT INTO bills (bill_id, vendor_name, amount, bill_date, file_path)
VALUES (5, 'Mobile Provider', 45.20, '2026-02-08',
'/home/hadoop/workspace/Agent-LocalDB/Files/bills/mobile_feb_2026.pdf');

INSERT INTO bills (bill_id, vendor_name, amount, bill_date, file_path)
VALUES (6, 'Insurance Co', 150.00, '2026-02-10',
'/home/hadoop/workspace/Agent-LocalDB/Files/bills/insurance_feb_2026.pdf');

INSERT INTO bills (bill_id, vendor_name, amount, bill_date, file_path)
VALUES (7, 'Streaming Service', 19.99, '2026-02-12',
'/home/hadoop/workspace/Agent-LocalDB/Files/bills/streaming_feb_2026.pdf');


INSERT INTO bills (bill_id, vendor_name, amount, bill_date, file_path)
VALUES (8, 'Gas Company', 85.75, '2025-02-05',
'/home/hadoop/workspace/Agent-LocalDB/Files/bills/gas_feb_2026.pdf');

INSERT INTO bills (bill_id, vendor_name, amount, bill_date, file_path)
VALUES (9, 'Mobile Provider', 45.20, '2025-02-08',
'/home/hadoop/workspace/Agent-LocalDB/Files/bills/mobile_feb_2026.pdf');

INSERT INTO bills (bill_id, vendor_name, amount, bill_date, file_path)
VALUES (10, 'Insurance Co', 150.00, '2024-02-10',
'/home/hadoop/workspace/Agent-LocalDB/Files/bills/insurance_feb_2026.pdf');

INSERT INTO bills (bill_id, vendor_name, amount, bill_date, file_path)
VALUES (11, 'Streaming Service', 19.99, '2024-02-12',
'/home/hadoop/workspace/Agent-LocalDB/Files/bills/streaming_feb_2026.pdf');



