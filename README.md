# Medical Supply Management System

A Flask-based medical inventory management system with machine-learning-based expiry-risk prediction.

## Overview

The Medical Supply Management System helps manage medical stores, medicines, inventory batches, and product availability.

The system integrates a Logistic Regression model to identify medicine batches that may be at high risk of expiry based on expiry timelines and sales velocity.

## Features

* Medical store management
* Medicine and product management
* Inventory batch management
* Medicine availability search
* Expiry-risk prediction
* Logistic Regression classification
* High-risk batch identification
* Automated alerts
* Database-backed reporting

## Machine Learning

The system uses Logistic Regression to classify inventory batches based on factors related to:

* Expiry timeline
* Sales velocity
* Inventory information

The model produces a risk classification that helps identify batches requiring attention.

## Tech Stack

* Python
* Flask
* Machine Learning
* Scikit-learn
* Logistic Regression
* SQL
* Relational Database
* HTML
* CSS
* JavaScript

## Workflow

```text
Inventory Entry
      |
      v
Inventory Data
      |
      v
Feature Processing
      |
      v
Logistic Regression
      |
      v
Expiry Risk Prediction
      |
      +----> Low Risk
      |
      +----> High Risk
                 |
                 v
              Alert
```

## Installation

Clone the repository:

```bash
git clone https://github.com/OG-Shrish/medical-supply-management-system.git
cd medical-supply-management-system
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open the application in your browser at the local address displayed by Flask.

## Project Goals

* Improve medical inventory visibility
* Reduce manual inventory tracking
* Identify potentially expiring batches early
* Support data-driven inventory management

## Future Improvements

* Demand forecasting
* Advanced expiry prediction
* Automated stock-reordering
* Email/SMS alerts
* Role-based access control
* Dashboard analytics

## Author

**Shrish Ahankari**

## License

This project is licensed under the MIT License.
