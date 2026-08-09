CREATE TABLE addmp (
    sno SERIAL PRIMARY KEY,
    medicine VARCHAR(500) NOT NULL
);

INSERT INTO addmp (medicine) VALUES
('Dolo 650'),
('Carpel 250 mg'),
('Azithromycin 500'),
('Rantac 300'),
('Paracetamol 500');


CREATE TABLE addpd (
    sno SERIAL PRIMARY KEY,
    product VARCHAR(200) NOT NULL
);

INSERT INTO addpd (product) VALUES
('Colgate'),
('Perfume'),
('Garnier Face Wash');


CREATE TABLE posts (
    mid SERIAL PRIMARY KEY,
    medical_name VARCHAR(100) NOT NULL,
    owner_name VARCHAR(100) NOT NULL,
    phone_no VARCHAR(20) NOT NULL,
    address VARCHAR(100) NOT NULL
);

INSERT INTO posts (
    medical_name,
    owner_name,
    phone_no,
    address
)
VALUES (
    'AHANKARI',
    'SHRISH',
    '78962341230',
    'CHICAGO'
);


CREATE TABLE medicines (
    id SERIAL PRIMARY KEY,
    mid VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    medicines VARCHAR(500) NOT NULL,
    products VARCHAR(500),
    amount INTEGER NOT NULL,
    email VARCHAR(50) NOT NULL
);


CREATE TABLE inventory_batches (
    batch_id SERIAL PRIMARY KEY,
    medicine_name VARCHAR(100) NOT NULL,
    quantity_remaining INTEGER NOT NULL,
    expiry_date DATE NOT NULL,
    avg_daily_sale DOUBLE PRECISION NOT NULL
);


CREATE TABLE expiry_alerts (
    alert_id SERIAL PRIMARY KEY,
    batch_id INTEGER NOT NULL,
    risk_flag INTEGER NOT NULL,
    prediction_date DATE NOT NULL,
    CONSTRAINT fk_expiry_batch
        FOREIGN KEY (batch_id)
        REFERENCES inventory_batches(batch_id)
        ON DELETE CASCADE
);


INSERT INTO inventory_batches (
    medicine_name,
    quantity_remaining,
    expiry_date,
    avg_daily_sale
)
VALUES
(
    'Dolo 650',
    500,
    '2027-03-10',
    20
),
(
    'Paracetamol 500',
    200,
    '2027-02-28',
    15
),
(
    'Azithromycin 500',
    800,
    '2027-02-25',
    5
);