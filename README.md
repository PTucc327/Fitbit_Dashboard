# 📊 Fitbit_Dashboard

A Streamlit-powered health analytics dashboard that connects to the Fitbit Web API to fetch, clean, and visualize personalized fitness and wellness data.
This project demonstrates real-world API integration, ETL workflow design, and interactive dashboard development using Python.

## 🚀 Features

### 🔐 Fitbit API Integration

- OAuth 2.0 authentication (Client ID + Client Secret)

- Automatic token refresh

#### Fetches data such as:

- Daily steps

- Heart rate time series

- Active minutes & calories

- Sleep duration & sleep stages

### ⚙️ Data Processing (ETL)

- Cleans and normalizes Fitbit JSON responses

- Converts raw data into analytics-ready DataFrames

- Handles missing values, duplicates, and timestamp alignment

## 📊 Streamlit Interactive Dashboard

- Daily, weekly, and monthly summaries

- Line charts, bar charts, aggregated tables

- Sleep vs. activity comparison views

- Heart rate analytics (resting HR, HR zones)

- Easy-to-navigate interactive UI

## 🛠️ Tech Stack

- Python

- Streamlit

- Pandas / NumPy
  
- Seaborn

- Matplotlib

- ReportLab


## 📁 Project Structure
fitbit-dashboard/
├── app.py # Main Streamlit app
├── fitbit_steps.csv # Sample data - daily step counts
├── fitbit_sleep.csv # Sample data - daily sleep durations
├── fitbit_heart_rate.csv # Sample data - resting heart rate
├── README.md # Project overview (this file)


▶️ How to Run
1. Install Dependencies
pip install -r requirements.txt

2. Create a Fitbit Developer App

Go to https://dev.fitbit.com/apps

Create a new OAuth 2.0 application

Copy your Client ID, Client Secret, and Redirect URI

3. Add Your Credentials

Set environment variables or create a .env file:

FITBIT_CLIENT_ID=your_client_id  
FITBIT_CLIENT_SECRET=your_client_secret  
FITBIT_REDIRECT_URI=your_redirect_uri

4. Run the Dashboard
streamlit run app.py


The dashboard will open automatically in your browser.

## 📈 Example Insights

- Step count trends over time

- Sleep stage breakdown per day

- Resting heart rate patterns

- Activity vs. calories correlation

- Hourly heart rate time series

## 🎯 Why This Project Is Useful

- Gives deeper insights than the default Fitbit app

- Lets users track long-term health patterns

- Provides modular code for future expansion

- Great real-world example of API + ETL + dashboard development

## 🧠 Future Improvements

- Add ML components (trend prediction, anomaly detection)

- Integrate user accounts (multi-user support)

- Deploy on Streamlit Cloud or Docker

## 👤 Author

Paul Tuccinardi

GitHub: https://github.com/PTucc327

Email: paultuccinardi@gmail.com 
