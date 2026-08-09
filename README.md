# Medical Supply Management System

A Flask-based medical inventory and supply management system with machine-learning-based expiry-risk prediction. The application manages medical stores, medicines, products, customer orders, inventory batches, and medicine availability while using Logistic Regression to identify inventory batches that are at risk of expiring before they can be sold.

## Features

### Medical Supply Management

* Add and manage medical store information
* Maintain medicine and product lists
* Record medicine and product orders
* View stored orders
* Delete order records
* Search medicine and product availability

### Inventory Management

* Add medicine inventory batches
* Track remaining quantity
* Store expiry dates
* Record average daily sales
* Maintain inventory data in MySQL

### Machine Learning-Based Expiry Prediction

* Logistic Regression classification
* Automatic risk prediction when inventory is added
* Uses quantity remaining, days until expiry, and average daily sales as prediction features
* Identifies batches with a higher likelihood of expiring before being sold
* Stores prediction results in an expiry-alert table
* Displays expiry-risk results through the web application

## Machine Learning

The system uses a Logistic Regression model to classify inventory batches into expiry-risk categories.

The model uses three features:

* `quantity_remaining`
* `days_left`
* `avg_daily_sale`

During model training, the system calculates the expected number of days required to sell the remaining inventory:

```text
expected_days_to_sell = quantity_remaining / avg_daily_sale
```

A batch is considered high risk when the expected selling time exceeds the number of days remaining before expiry.

The trained model is serialized using Python's `pickle` module and reused by the Flask application for batch-level predictions.

## System Workflow

```text
Add Inventory Batch
        |
        v
Store Inventory in MySQL
        |
        v
Calculate Days Until Expiry
        |
        v
Extract ML Features
        |
        v
Logistic Regression Model
        |
        v
Expiry Risk Prediction
        |
        +------------------+
        |                  |
        v                  v
    Low Risk           High Risk
                           |
                           v
                    Store Expiry Alert
                           |
                           v
                    Display Results
```

## Technology Stack

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* PyMySQL / MySQLdb

### Machine Learning

* Scikit-learn
* Logistic Regression
* Pandas
* Pickle

### Database

* MySQL
* SQLAlchemy ORM

### Frontend

* HTML
* CSS
* JavaScript
* Jinja2 Templates

## Project Structure

```text
medical-supply-management-system/
│
├── project/
│   ├── main.py
│   ├── expiry_model.py
│   ├── ml_utils.py
│   ├── predict_expiry.py
│   ├── medical.sql
│   ├── requirements.txt
│   ├── static/
│   └── templates/
│
├── .gitignore
└── README.md
```

## Database

The application uses MySQL with the following main tables:

* `addmp` — medicine catalogue
* `addpd` — product catalogue
* `posts` — medical store information
* `medicines` — customer/order records
* `inventory_batches` — medicine inventory and expiry information
* `expiry_alerts` — machine-learning expiry-risk predictions

The database schema and sample data are provided in `project/medical.sql`.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/OG-Shrish/medical-supply-management-system.git
cd medical-supply-management-system/project
```

### 2. Create the MySQL database

Open MySQL and execute:

```bash
mysql -u root -p < medical.sql
```

Alternatively, import `medical.sql` using MySQL Workbench.

### 3. Configure the database connection

The Flask application reads the database connection from `config.json`.

Update the local database URI with your MySQL username, password, host, and database configuration before running the application.

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

Make sure the ML and database dependencies required by the application are installed, including:

```bash
pip install flask flask-sqlalchemy pymysql pandas scikit-learn
```

### 5. Train the expiry-risk model

From the `project` directory:

```bash
python expiry_model.py
```

This trains the Logistic Regression model using the inventory data and generates:

```text
expiry_model.pkl
```

### 6. Run the application

```bash
python main.py
```

Open the local Flask address shown in the terminal, typically:

```text
http://127.0.0.1:5000/
```

## Application Workflow

1. Add medical store information.
2. Maintain medicine and product catalogues.
3. Record customer medicine/product orders.
4. Add inventory batches with quantity, expiry date, and average daily sales.
5. The system calculates expiry-risk automatically using the trained Logistic Regression model.
6. The prediction is stored in the `expiry_alerts` table.
7. Expiry-risk results can be viewed through the application.

## ML Components

### `expiry_model.py`

Retrieves inventory data from MySQL, calculates the training risk label, trains the Logistic Regression model, and saves the trained model as `expiry_model.pkl`.

### `ml_utils.py`

Loads the trained model and provides a reusable `predict_risk()` function for individual inventory batches.

### `predict_expiry.py`

Runs expiry-risk prediction for inventory batches and creates or updates corresponding records in the `expiry_alerts` table.

### `main.py`

Provides the Flask web application, database models, routes, inventory management, medicine management, search functionality, and integration with the ML prediction pipeline.

## Project Goals

* Digitize medical inventory management
* Improve visibility of available medicines and products
* Track inventory batches and expiry dates
* Identify potentially high-risk batches before expiry
* Integrate machine learning into practical inventory management
* Store and retrieve inventory risk information using a relational database

## Future Improvements

* Demand forecasting using historical sales data
* More advanced expiry-risk models
* Automated stock-reordering recommendations
* Email/SMS notifications for high-risk batches
* Role-based authentication and access control
* Interactive inventory analytics dashboard
* Model evaluation using accuracy, precision, recall, and F1-score
* Automated periodic model retraining

## Author

**Shrish Ahankari**

## License

This project is licensed under the MIT License.
