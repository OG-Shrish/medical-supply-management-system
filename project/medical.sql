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

