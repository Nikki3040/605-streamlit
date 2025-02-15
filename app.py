import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

st.title("Unlocking the Secrets of Bike-Sharing: A Data Story")

# Load the dataset once
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    return day_df, hour_df

day_df, hour_df = load_data()

# Map season codes to names
season_map = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
day_df['season_name'] = day_df['season'].map(season_map)

# Set dark theme
pio.templates.default = "plotly_dark"

st.subheader("Authors: Anika Achari & Prabhnoor Virk")

# Bike Usage Across Different Seasons
st.subheader("Bike Usage Across Different Seasons")
fig_season_box = px.box(day_df, x='season_name', y='cnt', color='season_name',
                        title="Bike Usage Across Different Seasons",
                        labels={'cnt': 'Total Bike Rentals', 'season_name': 'Season'})
st.plotly_chart(fig_season_box)

# Long-term Trends in Bike Usage
st.subheader("Long-term Trends in Bike Usage")
fig_trend = px.line(day_df, x='dteday', y='cnt', title="Long-term Trends in Bike Usage Over the Years",
                    labels={'dteday': 'Date', 'cnt': 'Total Bike Rentals'}, markers=True)
st.plotly_chart(fig_trend)

# Impact of Temperature on Bike Rentals
st.subheader("Impact of Temperature on Bike Rentals")
fig_temp = px.scatter(day_df, x='temp', y='cnt', title="Impact of Temperature on Bike Rentals",
                      labels={'temp': 'Temperature (Normalized)', 'cnt': 'Total Bike Rentals'},
                      color='cnt', color_continuous_scale='turbo')
st.plotly_chart(fig_temp)

# Impact of Humidity on Bike Rentals
st.subheader("Impact of Humidity on Bike Rentals")
fig_humidity = px.scatter(day_df, x='hum', y='cnt', title="Impact of Humidity on Bike Rentals",
                          labels={'hum': 'Humidity (Normalized)', 'cnt': 'Total Bike Rentals'},
                          color='cnt', color_continuous_scale='magma')
st.plotly_chart(fig_humidity)

# Impact of Holidays on Bike Rentals
st.subheader("Holiday vs Regular Day Bike Rentals")
holiday_counts = day_df.groupby('holiday')['cnt'].sum().reset_index()
holiday_counts['holiday'] = holiday_counts['holiday'].map({0: 'Regular Days', 1: 'Holidays'})
fig_holiday_donut = px.pie(holiday_counts, names='holiday', values='cnt',
                           title="Holiday vs Regular Day Bike Rentals", hole=0.4,
                           color='holiday', color_discrete_sequence=['#1f77b4', '#ff7f0e'])
st.plotly_chart(fig_holiday_donut)

# Hourly Bike Demand Trends
st.subheader("Hourly Bike Demand Across Days of the Week")
weekday_mapping = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
                   4: "Thursday", 5: "Friday", 6: "Saturday"}
hour_df["weekday"] = hour_df["weekday"].map(weekday_mapping)
hourly_trends = hour_df.groupby(["hr", "weekday"])["cnt"].mean().reset_index()
fig_hourly_animated = px.bar(hourly_trends, x="hr", y="cnt", animation_frame="weekday",
                             title="Hourly Bike Demand Across Days of the Week",
                             labels={"cnt": "Average Rentals", "hr": "Hour of Day", "weekday": "Day of the Week"},
                             color="cnt", color_continuous_scale="viridis")
st.plotly_chart(fig_hourly_animated)

# Hourly Rental Trends: Holidays vs. Weekends vs. Workdays
st.subheader("Hourly Bike Rental Trends: Holidays vs. Weekends vs. Workdays")
hour_df["day_type"] = hour_df.apply(lambda row: 
                                    "Holiday" if row["holiday"] == 1 else 
                                    ("Weekend" if row["weekday"] in [0, 6] else "Workday"), axis=1)
hourly_avg = hour_df.groupby(["hr", "day_type"])["cnt"].mean().reset_index()
fig_hourly_rentals = px.line(hourly_avg, x="hr", y="cnt", color="day_type",
                             title="Hourly Bike Rental Trends: Holidays vs. Weekends vs. Workdays",
                             labels={"hr": "Hour of the Day", "cnt": "Average Rentals", "day_type": "Day Type"},
                             markers=True)
st.plotly_chart(fig_hourly_rentals)

# Hourly Distribution of Casual vs. Registered Users
st.subheader("Hourly Distribution of Casual vs. Registered Users")
hourly_comparison = hour_df.groupby("hr").agg({"casual": "sum", "registered": "sum"}).reset_index()
fig_casual_registered_area = px.area(hourly_comparison, x="hr", y=["casual", "registered"],
                                     title="Hourly Distribution of Casual vs. Registered Users",
                                     labels={"hr": "Hour of the Day", "value": "Total Users", "variable": "User Type"})
st.plotly_chart(fig_casual_registered_area)

# Bike Usage Trends Over the Week
st.subheader("Bike Usage Trends Over the Week")
weekday_mapping = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
                   4: "Thursday", 5: "Friday", 6: "Saturday"}
day_df["weekday_name"] = day_df["weekday"].map(weekday_mapping)
weekly_trends = day_df.groupby("weekday_name")["cnt"].mean().reset_index()
fig_weekly_trends_line = px.line(weekly_trends, x="weekday_name", y="cnt",
                                 title="Bike Usage Trends Over the Week",
                                 labels={"cnt": "Average Bike Rentals", "weekday_name": "Day of the Week"},
                                 markers=True)
st.plotly_chart(fig_weekly_trends_line)

# Distribution of Bike Rentals Across the Week
st.subheader("Distribution of Bike Rentals Across the Week")
fig_weekly_trends_box = px.box(day_df, x="weekday_name", y="cnt",
                               title="Distribution of Bike Rentals Across the Week",
                               labels={"cnt": "Total Bike Rentals", "weekday_name": "Day of the Week"},
                               color="weekday_name")
st.plotly_chart(fig_weekly_trends_box)


# HOURLY RENTAL TRENDS ACROSS MONTHS
st.subheader("Hourly Bike Rental Trends Across Months")

# Map numeric month to names
month_mapping = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}
hour_df["month_name"] = hour_df["mnth"].map(month_mapping)

# Group by hour and month to get average rentals
hourly_monthly_rentals = hour_df.groupby(["month_name", "hr"])["cnt"].mean().reset_index()

# Create an interactive faceted line plot
fig_facet_interactive = px.line(
    hourly_monthly_rentals, x="hr", y="cnt", color="month_name",
    title="Hourly Bike Rental Trends Across Months",
    labels={"cnt": "Avg Rentals", "hr": "Hour of the Day", "month_name": "Month"},
    template="plotly_dark",
    facet_col="month_name",
    facet_col_wrap=4,  # Display facets in a grid format
    line_group="month_name",
    markers=True
)

# Remove "Month=" from facet labels
fig_facet_interactive.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Improve layout aesthetics
fig_facet_interactive.update_layout(
    font=dict(size=12),
    showlegend=False,  # Remove legend to avoid redundancy in facets
    height=700,
    width=1000  # Adjust width for better readability
)

# Show the visualization
st.plotly_chart(fig_facet_interactive)







