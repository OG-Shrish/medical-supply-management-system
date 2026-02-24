import pickle
import pandas as pd
from datetime import date
from main import db, InventoryBatch, ExpiryAlert

model = pickle.load(open("expiry_model.pkl", "rb"))

def run_prediction_for_batch(batch):

    days_left = (batch.expiry_date - date.today()).days

    data = pd.DataFrame([[batch.quantity_remaining, days_left, batch.avg_daily_sale]],
                        columns=['quantity_remaining', 'days_left', 'avg_daily_sale'])

    prediction = model.predict(data)[0]

    existing = ExpiryAlert.query.filter_by(batch_id=batch.batch_id).first()

    if existing:
        existing.risk_flag = int(prediction)
        existing.prediction_date = date.today()
    else:
        new_alert = ExpiryAlert(
            batch_id=batch.batch_id,
            risk_flag=int(prediction),
            prediction_date=date.today()
        )
        db.session.add(new_alert)

    db.session.commit()