import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="medical"
)

query = """
SELECT 
    batch_id,
    quantity_remaining,
    DATEDIFF(expiry_date, CURDATE()) AS days_left,
    avg_daily_sale
FROM inventory_batches
"""

df = pd.read_sql(query, conn)

df['expected_days_to_sell'] = df['quantity_remaining'] / df['avg_daily_sale']
df['risk'] = (df['expected_days_to_sell'] > df['days_left']).astype(int)

X = df[['quantity_remaining', 'days_left', 'avg_daily_sale']]
y = df['risk']

model = LogisticRegression()
model.fit(X, y)

pickle.dump(model, open("expiry_model.pkl", "wb"))
print("Model trained and saved")