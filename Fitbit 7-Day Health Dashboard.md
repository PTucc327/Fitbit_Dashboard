# 📊 Fitbit 7-Day Health Dashboard

This is an interactive Streamlit dashboard that visualizes and summarizes Fitbit data for steps, sleep, and heart rate across a selected 7-day period. It also supports week-over-week comparisons and generates a downloadable PDF report for personal tracking.

## 🧠 Features

- 📅 **Week Selector**: Choose any week from the past 5 weeks
- 🚶 **Steps Analysis**: View daily steps and average metrics
- 😴 **Sleep Insights**: Monitor total sleep minutes per day
- ❤️ **Heart Rate Trends**: Analyze resting heart rate across the week
- 📈 **Compare Weeks**: Optionally compare with the previous week
- 🧾 **PDF Report**: Download a weekly summary with visual plots

---

## 📂 Project Structure

fitbit-dashboard/
├── app.py # Main Streamlit app
├── fitbit_steps.csv # Sample data - daily step counts
├── fitbit_sleep.csv # Sample data - daily sleep durations
├── fitbit_heart_rate.csv # Sample data - resting heart rate
├── README.md # Project overview (this file)


---

## 🛠️ Requirements

- Python 3.8+
- Streamlit
- Pandas
- Seaborn
- Matplotlib
- ReportLab

You can install all dependencies using:

```bash
pip install -r requirements.txt


🚀 Run the App

streamlit run app.py

Then open your browser to http://localhost:8501.

🧾 Sample PDF Output
The app generates a clean weekly report in PDF format that includes:

Avg steps, sleep, and resting heart rate

Three plots (steps, sleep, heart rate)

Date range summary

PDFs are created using the reportlab library and can be downloaded from the sidebar.

📸 Screenshots
Add screenshots of your app here for better visibility (optional)

📌 Notes
Data files (fitbit_steps.csv, etc.) must be in the same directory as the app.

This is a personal health dashboard — make sure your data is secure and local.

📬 Contact
Built by Paul Tuccinardi
Feel free to connect on LinkedIn or explore my other projects!
