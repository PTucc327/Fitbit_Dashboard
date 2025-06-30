import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import os

def generate_pdf(avg_steps, avg_sleep, avg_hr_val, selected_start, selected_end, fig_steps, fig_sleep, fig_hr):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet
    import tempfile
    import os

    tmp_pdf_path = os.path.join(tempfile.gettempdir(), "fitbit_report.pdf")
    doc = SimpleDocTemplate(tmp_pdf_path)
    styles = getSampleStyleSheet()
    story = []

    # Header
    story.append(Paragraph(f"📅 Week: {selected_start.date()} to {selected_end.date()}", styles['Title']))
    story.append(Spacer(1, 12))

    # Metrics
    story.append(Paragraph(f"🚶 Avg Daily Steps: {avg_steps:,.0f}", styles['Normal']))
    story.append(Paragraph(f"😴 Avg Sleep (min): {avg_sleep:.1f}", styles['Normal']))
    story.append(Paragraph(f"❤️ Avg Resting HR: {avg_hr_val:.1f} bpm", styles['Normal']))
    story.append(Spacer(1, 12))

    # Save plots as temp files and embed
    for fig, name in [(fig_steps, "steps_plot.png"), (fig_sleep, "sleep_plot.png"), (fig_hr, "hr_plot.png")]:
        image_path = os.path.join(tempfile.gettempdir(), name)
        fig.savefig(image_path, bbox_inches='tight')
        story.append(Image(image_path, width=400, height=200))
        story.append(Spacer(1, 12))

    doc.build(story)
    return tmp_pdf_path

# === Layout Settings ===
st.set_page_config(page_title="Fitbit Dashboard", layout="wide")
st.title("📅 7-Day Fitbit Health Dashboard")

# === Load and Filter Data ===
@st.cache_data
def load_data():
    steps = pd.read_csv("fitbit_steps.csv", parse_dates=["date"])
    sleep = pd.read_csv("fitbit_sleep.csv", parse_dates=["date"])
    hr = pd.read_csv("fitbit_heart_rate.csv", parse_dates=["date"])
    return steps, sleep, hr

steps_df, sleep_df, hr_df = load_data()

# === Week Selector in Sidebar ===
st.sidebar.header("🗓️ Select Week")

# Show options for past 0 to 4 weeks (you can increase range)
week_options = {
    "This Week": 0,
    "Last Week": 1,
    "2 Weeks Ago": 2,
    "3 Weeks Ago": 3,
    "4 Weeks Ago": 4
}

selected_label = st.sidebar.selectbox("View Data From:", list(week_options.keys()))
selected_offset = week_options[selected_label]
compare_toggle = st.sidebar.checkbox("Compare with previous week?")

# Calculate week start and end based on selection
today = pd.Timestamp.today().normalize()
start_of_week = today - pd.Timedelta(days=today.weekday())  # Monday
selected_start = start_of_week - pd.Timedelta(weeks=selected_offset)
selected_end = selected_start + pd.Timedelta(days=6)
prev_start = selected_start - pd.Timedelta(weeks=1)
prev_end = selected_end - pd.Timedelta(weeks=1)

# Current week data
steps_df_current = steps_df[(steps_df['date'] >= selected_start) & (steps_df['date'] <= selected_end)]
sleep_df_current = sleep_df[(sleep_df['date'] >= selected_start) & (sleep_df['date'] <= selected_end)]
hr_df_current = hr_df[(hr_df['date'] >= selected_start) & (hr_df['date'] <= selected_end)]

# Previous week data (if needed)
steps_df_prev = steps_df[(steps_df['date'] >= prev_start) & (steps_df['date'] <= prev_end)]
sleep_df_prev = sleep_df[(sleep_df['date'] >= prev_start) & (sleep_df['date'] <= prev_end)]
hr_df_prev = hr_df[(hr_df['date'] >= prev_start) & (hr_df['date'] <= prev_end)]


st.sidebar.markdown(f"📆 Showing data from **{selected_start.date()} to {selected_end.date()}**")
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
st.sidebar.markdown("🎯 **Set Your Goals (Optional)**")
steps_goal = st.sidebar.number_input("🦶 Daily Steps Goal", min_value=0, value=10000)
sleep_goal = st.sidebar.number_input("😴 Sleep Goal (min)", min_value=0, value=420)
hr_goal = st.sidebar.number_input("❤️ Max Resting HR Goal", min_value=30, value=70)


# === Filter by selected week range ===
steps_df = steps_df[(steps_df['date'] >= selected_start) & (steps_df['date'] <= selected_end)]
sleep_df = sleep_df[(sleep_df['date'] >= selected_start) & (sleep_df['date'] <= selected_end)]
hr_df = hr_df[(hr_df['date'] >= selected_start) & (hr_df['date'] <= selected_end)]


steps_df = steps_df.assign(day=steps_df['date'].dt.day_name())
sleep_df = sleep_df.assign(day=sleep_df['date'].dt.day_name())
hr_df = hr_df.assign(day=hr_df['date'].dt.day_name())


sns.set_theme(style="whitegrid")

# === Insights Section ===
with st.container():
    st.markdown("### 🔍 Weekly Insights")
    avg_steps = steps_df["steps"].mean()
    avg_sleep = sleep_df["duration_min"].mean()
    avg_hr = hr_df.groupby("date")["value"].mean().reset_index()
    avg_hr["day"] = avg_hr["date"].dt.day_name()
    avg_hr_val = avg_hr["value"].mean()
    top_day = steps_df.groupby("day")["steps"].mean().idxmax()
    top_day_steps = steps_df["steps"].max()
    low_day = sleep_df.groupby("day")["duration_min"].mean().idxmin()
    rest_hr = hr_df['value'].min()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Daily Steps", f"{avg_steps:,.0f}")
        st.metric("🚶Most Active Day Steps " , top_day_steps)
        st.metric("Most Active Day", top_day)
        
    with col2:
        st.metric("😴Avg Sleep (min)", f"{avg_sleep:.1f}")
        st.metric("Least Sleep Day", low_day)
    with col3:
        st.metric("❤️ Avg Resting Heart Rate",f"{avg_hr_val:.1f}" )  
        st.metric("Resting Heartrate", rest_hr) 
   

if compare_toggle:
    st.markdown("## 📊 Week-over-Week Comparison")
    colA, colB = st.columns(2)

    for label, steps, sleep, hr in [("This Week", steps_df_current, sleep_df_current, hr_df_current),
                                    ("Previous Week", steps_df_prev, sleep_df_prev, hr_df_prev)]:
        
        steps['day'] = steps['date'].dt.day_name()
        sleep['day'] = sleep['date'].dt.day_name()
        hr['day'] = hr['date'].dt.day_name()
        avg_hr = hr.groupby("date")["value"].mean().reset_index()
        avg_hr["day"] = avg_hr["date"].dt.day_name()

        with colA if label == "This Week" else colB:
            st.markdown(f"### {label}")
            st.metric("Avg Daily Steps", f"{steps['steps'].mean():,.0f}")
            st.metric("Avg Sleep (min)", f"{sleep['duration_min'].mean():.1f}")
            st.metric("Avg HR", f"{avg_hr['value'].mean():.1f} bpm")

            fig, ax = plt.subplots(figsize=(5.5, 3))
            sns.barplot(data=steps, x="day", y="steps", ax=ax, palette="Blues_d", order=day_order)
            ax.set_title("Steps by Day")
            ax.tick_params(axis='x', rotation=30)
            ax.set_xlabel("")  # Optional: hides the redundant 'Day' label
            st.pyplot(fig)

            fig2, ax2 = plt.subplots(figsize=(5.5, 3))
            sns.barplot(data=sleep, x="day", y="duration_min", ax=ax2, palette="Purples_d", order=day_order)
            ax2.set_title("Sleep Duration")
            ax2.tick_params(axis='x', rotation=30)
            ax2.set_xlabel("")  # Optional: hides the redundant 'Day' label

            st.pyplot(fig2)

            fig3, ax3 = plt.subplots(figsize=(5.5, 3))
            sns.lineplot(data=avg_hr, x="day", y="value", marker="o", ax=ax3, color="red")
            ax3.set_title("Resting HR")
            ax3.tick_params(axis='x', rotation=30)
            ax3.set_xlabel("")  # Optional: hides the redundant 'Day' label

            st.pyplot(fig3)
else:
        # === Steps Section ===
        with st.container():
            st.markdown("<h1 style='text-align: center;'>🚶 Steps Overview</h1>", unsafe_allow_html=True)
            col1 = st.columns([1,3,1])[1]
            with col1:
                fig1, ax1 = plt.subplots(figsize=(8, 4))
                sns.barplot(data=steps_df, x="day", y="steps", ax=ax1, palette="Blues_d", order=day_order)
                ax1.axhline(steps_goal, color="green", linestyle="--", label="Goal")
               

                ax1.set_ylabel("Steps")
                ax1.set_xlabel("Day")
                ax1.set_title("Steps by Day", fontsize=14)
                ax1.tick_params(axis='x', rotation=30)
                ax1.set_xlabel("")  # Optional: hides the redundant 'Day' label
                ax1.legend()
                plt.tight_layout()
                st.pyplot(fig1)

        # === Sleep Section ===
        with st.container():
            st.markdown("<h1 style='text-align: center;'>😴 Sleep Duration</h1>", unsafe_allow_html=True)
            col2 = st.columns([1, 3, 1])[1]  # Narrow center column
            with col2:
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.barplot(data=sleep_df, x="day", y="duration_min", ax=ax, palette="Purples_d", order=day_order)
                ax.axhline(sleep_goal, color="green", linestyle="--", label="Goal")
                ax.legend()

                ax.set_title("Sleep Duration by Day", fontsize=14)
                ax.tick_params(axis='x', rotation=30)
                ax.set_xlabel("")  # Optional: hides the redundant 'Day' label

                plt.tight_layout()
                st.pyplot(fig)

        # === Heart Rate Section ===
        with st.container():
            st.markdown("<h1 style='text-align: center;'>❤️ Resting Heart Rate</h1>", unsafe_allow_html=True)

            col3 = st.columns([1,3,1])[1]
            with col3:

                fig3, ax3 = plt.subplots(figsize=(8, 4))
                sns.lineplot(data=avg_hr, x="day", y="value", marker="o", ax=ax3, color="red")
                ax3.axhline(hr_goal, color="green", linestyle="--", label="Goal")
                ax3.legend()

                ax3.set_ylabel("Heart Rate (bpm)")
                ax3.set_title("Average Daily Heart Rate", fontsize=14)
                ax3.tick_params(axis='x', rotation=30)
                ax3.set_xlabel("")  # Optional: hides the redundant 'Day' label

                plt.tight_layout()
                st.pyplot(fig3)
        # === Generate PDF and add download button in sidebar ===

        try:
            pdf_path = generate_pdf(
        avg_steps=avg_steps,
        avg_sleep=avg_sleep,
        avg_hr_val=avg_hr_val,
        selected_start=selected_start,
        selected_end=selected_end,
        fig_steps=fig1,
        fig_sleep=fig,
        fig_hr=fig3
    )

            with open(pdf_path, "rb") as f:
                st.sidebar.download_button(
            label="📥 Download Weekly PDF Report",
            data=f,
            file_name=f"fitbit_weekly_report_{selected_start.date()}.pdf",
            mime="application/pdf"
        )
        except Exception as e:
                st.sidebar.error(f"❌ Failed to generate PDF: {e}")










