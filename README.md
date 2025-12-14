📌 **1. INTRODUCTION**
The Medical Supply Management System is a web-based application developed as part of a Database Management System (DBMS) mini project. The main purpose of this project is to efficiently manage medical stores, medicines, products, and customer orders using a relational database system.
The application provides an organized platform to store medical information and automatically track database activities using triggers.


🎯 **2. OBJECTIVES OF THE PROJECT**
The objectives of this project are:

* ✔️ To design and implement a database-driven medical supply system
* ✔️ To manage medicines and products efficiently
* ✔️ To store and process customer orders
* ✔️ To implement database triggers for automatic logging
* ✔️ To apply theoretical DBMS concepts in a practical project


🛠️ **3. TECHNOLOGIES USED**

* Backend Language  : Python
* Web Framework    : Flask
* Frontend         : HTML, CSS, Bootstrap
* Database         : MySQL / MariaDB
* ORM              : SQLAlchemy
* Tools Used       : phpMyAdmin, Git, GitHub


✨ **4. FEATURES OF THE SYSTEM**

* 🔐 User authentication system
* 🏪 Medical store information management
* 💊 Medicine and product inventory management
* 🧾 Customer order placement
* 🔍 Search functionality for medicines and products
* 📝 Automatic logging of INSERT, UPDATE, DELETE operations using database triggers


🗄️ **5. DATABASE DESIGN**
The database consists of the following tables:

* 👤 Users
* 🏪 Posts (Medical store details)
* 💊 Medicines
* 📦 Addmp (Medicine list)
* 📦 Addpd (Product list)
* 📝 Logs (Audit records)

Primary keys are used to uniquely identify records. Database triggers are implemented on the medicines table to automatically store logs whenever data is inserted, updated, or deleted.


📚 **6. DBMS CONCEPTS USED**

* 📌 Relational database design
* 🔑 Primary keys
* 🧩 Normalization
* 🔄 CRUD operations
* ⚙️ Database triggers
* 📝 Audit logging
* 🔗 ORM integration


▶️ **7. HOW TO RUN THE PROJECT**

1. Create a database named **medical** in MySQL.
2. Import the `medical.sql` file using phpMyAdmin.
3. Install the required Python packages.
4. Run the application using the command:
   `python main.py`
5. Open a browser and visit:
   `http://127.0.0.1:5000/login`


🎓 **8. APPLICATIONS OF THE PROJECT**
This project can be used as:

* 📘 A DBMS mini project for college submission
* 💻 A demonstration of Flask and MySQL integration
* 🏥 A basic medical inventory management system
