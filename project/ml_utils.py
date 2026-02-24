import pickle
import pandas as pd
from datetime import date

model = pickle.load(open("expiry_model.pkl", "rb"))

def predict_risk(quantity_remaining, expiry_date, avg_daily_sale):

    days_left = (expiry_date - date.today()).days

    data = pd.DataFrame(
        [[quantity_remaining, days_left, avg_daily_sale]],
        columns=['quantity_remaining', 'days_left', 'avg_daily_sale']
    )

    prediction = model.predict(data)[0]

    return int(prediction)