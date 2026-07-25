import os
import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

os.environ['DATABASE_URL'] = 'sqlite:///temp_test.db'

from app.main import app

client = TestClient(app)
product_id = '99a4788cb24856965c36a24e339b6058'

resp = client.get(f'/sales-history/{product_id}')
print('sales_history_status', resp.status_code)
print('sales_history_len', len(resp.json()))
print('sales_history_sample', json.dumps(resp.json()[:5], default=str, indent=2))

# Choose a target_date with at least 7 historical rows in the trailing 30-day window.
import pandas as pd
from pathlib import Path
csv_path = Path(__file__).resolve().parent.parent / 'data' / 'processed' / 'olist_phase2_features.csv'
df = pd.read_csv(csv_path, usecols=['product_id', 'order_date'])
df = df[df['product_id'] == product_id].copy()
df['order_date'] = pd.to_datetime(df['order_date'])
df = df.sort_values('order_date')
chosen_target = None
for i in range(len(df) - 1, -1, -1):
    target = df['order_date'].iloc[i] + pd.Timedelta(days=1)
    count = ((df['order_date'] >= target - pd.Timedelta(days=30)) & (df['order_date'] < target)).sum()
    if count >= 7:
        chosen_target = target.date()
        break
if chosen_target is None:
    raise RuntimeError('Could not find a valid target_date with >=7 history rows')
print('chosen_target', chosen_target)

base_payload = {
    'product_id': product_id,
    'target_date': str(chosen_target)
}
resp1 = client.post('/forecast/predict', json=base_payload)
print('forecast_no_override_status', resp1.status_code)
print('forecast_no_override_body', json.dumps(resp1.json(), indent=2))

payload2 = {
    'product_id': product_id,
    'target_date': str(chosen_target),
    'simulated_price': 999.99
}
resp2 = client.post('/forecast/predict', json=payload2)
print('forecast_override_status', resp2.status_code)
print('forecast_override_body', json.dumps(resp2.json(), indent=2))

print('prediction_diff', resp1.json().get('predicted_units_sold') != resp2.json().get('predicted_units_sold'))
