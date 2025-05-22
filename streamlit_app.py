# streamlit_app.py
import streamlit as st
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

backend_url = "https://stackup-backend.onrender.com"  # FastAPI backend

st.title("StackUp Portfolio Dashboard")

username = st.text_input("Enter your username", value="testuser")
uploaded_file = st.file_uploader("Upload your investment CSV", type="csv")

def show_trend_chart(trend_data):
    # Convert timestamps to matplotlib-compatible float format
    timestamps = [
        mdates.date2num(datetime.fromisoformat(point["timestamp"].replace("Z", "")))
        for point in trend_data
    ]
    invested = [point["total_invested"] for point in trend_data]
    current = [point["current_value"] for point in trend_data]

    # Create plot
    plt.figure(figsize=(10, 4))
    plt.plot(timestamps, invested, label="Total Invested", linestyle='--', marker='o')
    plt.plot(timestamps, current, label="Current Value", linestyle='-', marker='o')
    plt.xlabel("Timestamp")
    plt.ylabel("Amount (₹)")
    plt.title("Portfolio Trend Over Time")
    plt.legend()
    plt.grid(True)

    # Tell matplotlib to format the x-axis as dates
    ax = plt.gca()
    ax.xaxis_date()
    plt.gcf().autofmt_xdate()

    # Show plot in Streamlit
    fig = plt.gcf()
    st.pyplot(fig)

if uploaded_file and username:
    files = {"files": ("portfolio.csv", uploaded_file, "text/csv")}
    upload_response = requests.post(f"{backend_url}/portfolio/upload?username={username}", files=files)

    if upload_response.status_code == 200:
        st.success("File uploaded successfully!")

        # Fetch trend data
        trend_response = requests.get(f"{backend_url}/portfolio/trends?username={username}")
        if trend_response.status_code == 200:
            trend_data = trend_response.json().get("trends", [])
            if trend_data:
                st.subheader("Portfolio Trend")
                show_trend_chart(trend_data)
            else:
                st.info("No trend data available yet. Upload more files to track changes.")
        else:
            st.error("Failed to fetch trends from backend.")
    else:
        st.error("Upload failed. Please try again.")