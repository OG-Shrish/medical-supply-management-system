-- Database create karna
CREATE DATABASE IF NOT EXISTS medical;
USE medical;

-- Medicine list store karne ke liye table

CREATE TABLE addmp (
  sno INT AUTO_INCREMENT PRIMARY KEY,
  medicine VARCHAR(500) NOT NULL
);

-- Medicines ka data insert karna
INSERT INTO addmp (medicine) VALUES
('Dolo 650'),
('Carpel 250 mg'),
('Azithromycin 500'),
('Rantac 300'),
('Paracetamol 500');

-- Products list store karne ke liye table

CREATE TABLE addpd (
  sno INT AUTO_INCREMENT PRIMARY KEY,
  product VARCHAR(200) NOT NULL
);

-- Products ka data insert karna
INSERT INTO addpd (product) VALUES
('Colgate'),
('Perfume'),
('Garnier Face Wash');

-- Medical store details store karne ke liye table

CREATE TABLE posts (
  mid INT AUTO_INCREMENT PRIMARY KEY,
  medical_name VARCHAR(100) NOT NULL,
  owner_name VARCHAR(100) NOT NULL,
  phone_no VARCHAR(20) NOT NULL,
  address VARCHAR(50) NOT NULL
);

-- Medical store ka data insert karna
INSERT INTO posts (medical_name, owner_name, phone_no, address)
VALUES
('AHANKARI', 'SHRISH', '78962341230', 'CHICAGO');

-- Customer orders store karne ke liye table

CREATE TABLE medicines (
  id INT AUTO_INCREMENT PRIMARY KEY,
  mid VARCHAR(50) NOT NULL,
  name VARCHAR(100) NOT NULL,
  medicines VARCHAR(500) NOT NULL,
  products VARCHAR(500),
  amount INT NOT NULL,
  email VARCHAR(50) NOT NULL
);

CREATE TABLE inventory_batches (
  batch_id INT AUTO_INCREMENT PRIMARY KEY,
  medicine_name VARCHAR(100),
  quantity_remaining INT,
  expiry_date DATE,
  avg_daily_sale FLOAT
);

CREATE TABLE expiry_alerts (
  alert_id INT AUTO_INCREMENT PRIMARY KEY,
  batch_id INT,
  risk_flag INT,
  prediction_date DATE
);

INSERT INTO inventory_batches (medicine_name, quantity_remaining, expiry_date, avg_daily_sale)
VALUES
('Dolo 650', 500, '2026-03-10', 20),
('Paracetamol 500', 200, '2026-02-28', 15),
('Azithromycin 500', 800, '2026-02-25', 5);