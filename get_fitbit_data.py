import fitbit
import datetime
import json
import pandas as pd
from dateutil import rrule
import os
import time
# Allow HTTP for local testing
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Replace with your Fitbit app credentials
CLIENT_ID = 'ENETER_CLIENT_ID_HERE'
CLIENT_SECRET = 'ENTER_CLIENT_SECRET_HERE'

TOKEN_FILE = "fitbit_tokens.json"

def load_tokens():
    with open(TOKEN_FILE, 'r') as f:
        return json.load(f)

def save_tokens(tokens):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f)

# Load saved tokens
tokens = load_tokens()

# Enable insecure HTTP if needed
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Define refresh callback
def refresh_cb(new_token):
    save_tokens(new_token)
    print("🔄 Token refreshed and saved")

# Init Fitbit client with refresh support
client = fitbit.Fitbit(
    CLIENT_ID,
    CLIENT_SECRET,
    access_token=tokens['access_token'],
    refresh_token=tokens['refresh_token'],
    expires_at=tokens.get('expires_at', time.time() - 1000),
    refresh_cb=refresh_cb
)

# Today's date
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=30)

# Containers for data
steps_data = []
sleep_data = []
hr_data_all = []

# Loop over date range
for dt in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
    date_str = dt.strftime('%Y-%m-%d')
    print(f"📆 Fetching for {date_str}...")

    # Steps
    try:
        activity = client.activities(date=date_str)
        steps = activity['summary']['steps']
    except:
        steps = None

    # Sleep
    try:
        sleep = client.sleep(date=date_str)
        if sleep['sleep']:
            duration = sleep['sleep'][0]['duration'] / 1000 / 60
            efficiency = sleep['sleep'][0]['efficiency']
        else:
            duration = efficiency = None
    except:
        duration = efficiency = None

    # Heart Rate
    try:
        hr = client.intraday_time_series('activities/heart', base_date=date_str, detail_level='1min')
        hr_df = pd.DataFrame(hr['activities-heart-intraday']['dataset'])
        hr_df['date'] = date_str
        hr_data_all.append(hr_df)
    except:
        pass

    # Save summary row
    steps_data.append({'date': date_str, 'steps': steps})
    sleep_data.append({'date': date_str, 'duration_min': duration, 'efficiency': efficiency})

# Convert to DataFrames
# Steps + Sleep
df_steps = pd.DataFrame(steps_data)
df_sleep = pd.DataFrame(sleep_data)

# Heart Rate
if hr_data_all:
    df_hr = pd.concat(hr_data_all, ignore_index=True)
    df_hr.to_csv("fitbit_heart_rate.csv", index=False)
    print("✅ Heart rate data saved.")
else:
    df_hr = pd.DataFrame()
    print("⚠️ No heart rate data was available to save.")

# Save steps/sleep
df_steps.to_csv("fitbit_steps.csv", index=False)
df_sleep.to_csv("fitbit_sleep.csv", index=False)


print("✅ All data saved!")