import pickle
from datetime import date
from pathlib import Path

import pandas as pd


MODEL_PATH = Path(__file__).resolve().parent / "expiry_model.pkl"

_model = None


def load_model():
    global _model

    if _model is None:
        with open(MODEL_PATH, "rb") as file:
            _model = pickle.load(file)

    return _model


def predict_risk(quantity_remaining, expiry_date, avg_daily_sale):
    days_left = (expiry_date - date.today()).days

    data = pd.DataFrame(
        [[
            quantity_remaining,
            days_left,
            avg_daily_sale
        ]],
        columns=[
            "quantity_remaining",
            "days_left",
            "avg_daily_sale"
        ]
    )

    model = load_model()

    prediction = model.predict(data)[0]

    return int(prediction)