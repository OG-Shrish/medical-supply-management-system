import pickle
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression


MODEL_PATH = Path(__file__).resolve().parent / "expiry_model.pkl"


rng = np.random.default_rng(42)

samples = 5000

quantity_remaining = rng.integers(
    1,
    5000,
    samples
)

days_left = rng.integers(
    -30,
    365,
    samples
)

avg_daily_sale = rng.uniform(
    0.5,
    100,
    samples
)

expected_days_to_sell = (
    quantity_remaining / avg_daily_sale
)

risk = (
    expected_days_to_sell > days_left
).astype(int)

X = np.column_stack(
    [
        quantity_remaining,
        days_left,
        avg_daily_sale
    ]
)

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X, risk)

with open(MODEL_PATH, "wb") as file:
    pickle.dump(model, file)

print(f"Model saved to {MODEL_PATH}")