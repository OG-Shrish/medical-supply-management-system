CREATE DATABASE IF NOT EXISTS medical;
USE medical;

CREATE TABLE addmp (
  sno INT AUTO_INCREMENT PRIMARY KEY,
  medicine VARCHAR(500) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE addpd (
  sno INT AUTO_INCREMENT PRIMARY KEY,
  product VARCHAR(200) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE posts (
  mid INT AUTO_INCREMENT PRIMARY KEY,
  medical_name VARCHAR(100) NOT NULL,
  owner_name VARCHAR(100) NOT NULL,
  phone_no VARCHAR(20) NOT NULL,
  address VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE medicines (
  id INT AUTO_INCREMENT PRIMARY KEY,
  amount INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  medicines VARCHAR(500) NOT NULL,
  products VARCHAR(500) NOT NULL,
  email VARCHAR(50) NOT NULL,
  mid VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  mid VARCHAR(50),
  action VARCHAR(30) NOT NULL,
  date VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

DELIMITER $$

CREATE TRIGGER trg_medicines_insert
AFTER INSERT ON medicines
FOR EACH ROW
BEGIN
  INSERT INTO logs VALUES (NULL, NEW.mid, 'INSERTED', NOW());
END$$

CREATE TRIGGER trg_medicines_update
AFTER UPDATE ON medicines
FOR EACH ROW
BEGIN
  INSERT INTO logs VALUES (NULL, NEW.mid, 'UPDATED', NOW());
END$$

CREATE TRIGGER trg_medicines_delete
BEFORE DELETE ON medicines
FOR EACH ROW
BEGIN
  INSERT INTO logs VALUES (NULL, OLD.mid, 'DELETED', NOW());
END$$

DELIMITER ;

INSERT INTO addmp (medicine) VALUES
('Dolo 650'),
('Carpel 250 mg'),
('Azythromycin 500'),
('Azythromycin 250'),
('Rantac 300'),
('Omez'),
('Okacet'),
('Paracetamol');

INSERT INTO addpd (product) VALUES
('Colgate'),
('Perfume'),
('Garnier Face Wash');

INSERT INTO posts (medical_name, owner_name, phone_no, address)
VALUES ('ARK PROCODER MEDICAL', 'ANEES', '7896541230', 'Bangalore');
