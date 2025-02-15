import streamlit as st

st.title("My Streamlit App")

# Add interactivity here (sliders, buttons, inputs, etc.)

import pandas as pd
import plotly as px

# Load the datasets
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")



import pandas as pd
import plotly.express as px
import plotly.io as pio

# Load dataset
day_df = pd.read_csv("day.csv")

# Convert date column to datetime format
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Map season codes to names
season_map = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
day_df['season_name'] = day_df['season'].map(season_map)

# Set dark theme for advanced aesthetics
pio.templates.default = "plotly_dark"

# Adjust figure size
fig_width = 1000  # Reduce width for better visibility

# ========== 1. Bike Usage Across Different Seasons ==========
fig_season_box = px.box(
    day_df,
    x='season_name',
    y='cnt',
    color='season_name',
    title="Bike Usage Across Different Seasons",
    labels={'cnt': 'Total Bike Rentals', 'season_name': 'Season'},
    width=fig_width
)
fig_season_box.update_layout(font=dict(size=14))
fig_season_box.show()
fig_season_box.write_image("1.png", scale=3)

# ========== 2. Long-term Trends in Bike Usage ==========
fig_trend = px.line(
    day_df,
    x='dteday',
    y='cnt',
    title="Long-term Trends in Bike Usage Over the Years",
    labels={'dteday': 'Date', 'cnt': 'Total Bike Rentals'},
    markers=True,
    width=fig_width
)
fig_trend.update_traces(line=dict(width=3))
fig_trend.show()
fig_trend.write_image("2.png", scale=3)

# ========== 3. Impact of Temperature on Bike Rentals ==========
fig_temp = px.scatter(
    day_df,
    x='temp',
    y='cnt',
    title="Impact of Temperature on Bike Rentals",
    labels={'temp': 'Temperature (Normalized)', 'cnt': 'Total Bike Rentals'},
    color='cnt',
    color_continuous_scale='turbo',
    width=fig_width
)
fig_temp.show()
fig_temp.write_image("3.png", scale=3)

# ========== 4. Impact of Humidity on Bike Rentals ==========
fig_humidity = px.scatter(
    day_df,
    x='hum',
    y='cnt',
    title="Impact of Humidity on Bike Rentals",
    labels={'hum': 'Humidity (Normalized)', 'cnt': 'Total Bike Rentals'},
    color='cnt',
    color_continuous_scale='magma',
    width=fig_width
)
fig_humidity.show()
fig_humidity.write_image("4.png", scale=3)

import plotly.io as pio
pio.write_html(fig_humidity, "moving.html", auto_open=True)



# ========== Impact of Holidays on Bike Rentals========== 

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Map season codes to names - easier to manage
season_map = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
day_df['season_name'] = day_df['season'].map(season_map)

px.defaults.template = "plotly_dark"

holiday_counts = day_df.groupby('holiday')['cnt'].sum().reset_index()
holiday_counts['holiday'] = holiday_counts['holiday'].map({0: 'Regular Days', 1: 'Holidays'})
fig_holiday_donut = px.pie(
    holiday_counts,
    names='holiday',
    values='cnt',
    title="Holiday vs Regular Day Bike Rentals ",
    hole=0.4,
    color='holiday',
    color_discrete_sequence=['#1f77b4', '#ff7f0e'], 
    width=1100)
fig_holiday_donut.show()
fig_holiday_donut.write_image("5.png", scale=3)





# ========== Hourly Fluctuations in Bike Demand ========== 

import pandas as pd
import plotly.express as px

# Load dataset
hour_df = pd.read_csv("hour.csv")

# Define mapping for weekdays (0-6) to actual names
weekday_mapping = {
    0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
    4: "Thursday", 5: "Friday", 6: "Saturday"}

# Group by hour and weekday, then calculate the average rentals
hourly_trends = hour_df.groupby(["hr", "weekday"])["cnt"].mean().reset_index()

# Apply mapping to weekday column
hourly_trends["weekday"] = hourly_trends["weekday"].map(weekday_mapping)

# Create the bar chart
fig_hourly_animated = px.bar(
    hourly_trends,
    x="hr",
    y="cnt",
    animation_frame="weekday",
    title="Hourly Bike Demand Across Days of the Week",
    labels={"cnt": "Average Rentals", "hr": "Hour of Day", "weekday": "Day of the Week"},
    color="cnt",
    color_continuous_scale="viridis",
    template="plotly_dark",
    width=1100)

fig_hourly_animated.show()
fig_hourly_animated.write_image("6.png", scale=3)

fig_hourly_animated.write_html("moving.html")




# How do bike rentals differ between holidays, weekends, and workdays at different times of the day?

import plotly.express as px
import pandas as pd

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Map weekday and holiday labels
hour_df["day_type"] = hour_df.apply(lambda row: 
                                    "Holiday" if row["holiday"] == 1 else 
                                    ("Weekend" if row["weekday"] in [0, 6] else "Workday"), axis=1)

# Aggregate hourly rentals based on the new categories
hourly_avg = hour_df.groupby(["hr", "day_type"])["cnt"].mean().reset_index()

# Reduce figure width for better visualization
fig_width = 1000

# Line chart to show rental trends across diff times of day
fig_hourly_rentals = px.line(hourly_avg, x="hr", y="cnt", color="day_type",
                             title="Hourly Bike Rental Trends: Holidays vs. Weekends vs. Workdays",
                             labels={"hr": "Hour of the Day", "cnt": "Average Rentals", "day_type": "Day Type"},
                             template="plotly_dark", markers=True, width=fig_width)

fig_hourly_rentals.update_traces(line=dict(width=3))
fig_hourly_rentals.update_layout(legend_title_text="Day Type")
fig_hourly_rentals.show()
fig_hourly_rentals.write_image("7.png", scale=3)


# HOURLY DISTRIBUTION OF CASUAL VS. REGISTERED USERS 

import plotly.graph_objects as go

hour_df = pd.read_csv("hour.csv")

# Group by hour to compare casual and registered users
hourly_comparison = hour_df.groupby("hr").agg({"casual": "sum", "registered": "sum"}).reset_index()

fig_casual_registered_area = go.Figure()

fig_casual_registered_area.add_trace(go.Scatter(
    x=hourly_comparison["hr"], y=hourly_comparison["casual"],
    mode="lines", fill="tozeroy", name="Casual Users",
    line=dict(color="blue", width=2), opacity=0.8))

fig_casual_registered_area.add_trace(go.Scatter(
    x=hourly_comparison["hr"], y=hourly_comparison["registered"],
    mode="lines", fill="tonexty", name="Registered Users",
    line=dict(color="red", width=2), opacity=0.6))

fig_casual_registered_area.update_layout(
    title="Hourly Distribution of Casual vs. Registered Users",
    xaxis_title="Hour of the Day",
    yaxis_title="Total Users",
    template="plotly_dark",
    showlegend=True,
    xaxis=dict(tickmode="linear", dtick=1),
    yaxis=dict(separatethousands=True, rangemode="tozero", gridcolor="rgba(255,255,255,0.1)"))

fig_casual_registered_area.show()
fig_casual_registered_area.write_image("8.png", scale=3)

# HOURLY RENTAL TRENDS ACROSS MONTHS
# Create an interactive line plot with facet grid for monthly trends

import pandas as pd
import plotly.express as px

# Load dataset
hour_df = pd.read_csv("hour.csv")

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
fig_facet_interactive.show()
fig_facet_interactive.write_image("9.png", scale=3)


import pandas as pd
import plotly.express as px

# Load the dataset
day_df = pd.read_csv("day.csv")

# Map weekday numbers (0-6) to actual names
weekday_mapping = {
    0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
    4: "Thursday", 5: "Friday", 6: "Saturday"
}
day_df["weekday_name"] = day_df["weekday"].map(weekday_mapping)

# Aggregate bike rentals by weekday
weekly_trends = day_df.groupby("weekday_name")["cnt"].mean().reset_index()

# Sort the days of the week properly
weekday_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
weekly_trends["weekday_name"] = pd.Categorical(weekly_trends["weekday_name"], categories=weekday_order, ordered=True)
weekly_trends = weekly_trends.sort_values("weekday_name")

# Create a line chart to show bike rental trends across the week
fig_weekly_trends_line = px.line(
    weekly_trends, 
    x="weekday_name", 
    y="cnt", 
    text=weekly_trends["cnt"].round(2),  # Round to 2 decimal places
    title="Bike Usage Trends Over the Week",
    labels={"cnt": "Average Bike Rentals", "weekday_name": "Day of the Week"},
    markers=True,
    template="plotly_dark"
)

# Adjust aesthetics
fig_weekly_trends_line.update_traces(line=dict(width=3), textposition="top center")
fig_weekly_trends_line.update_layout(width=800)  # Reduce width for better visibility

# Show the visualization
fig_weekly_trends_line.show()
fig_weekly_trends_line.write_image("10.png", scale=3)


import pandas as pd
import plotly.express as px

# Load the dataset
day_df = pd.read_csv("day.csv")

# Map weekday numbers (0-6) to actual names
weekday_mapping = {
    0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
    4: "Thursday", 5: "Friday", 6: "Saturday"
}
day_df["weekday_name"] = day_df["weekday"].map(weekday_mapping)

# Ensure correct weekday sorting
weekday_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
day_df["weekday_name"] = pd.Categorical(day_df["weekday_name"], categories=weekday_order, ordered=True)

# Create a box plot to show the distribution of bike rentals for each weekday
fig_weekly_trends_box = px.box(
    day_df, 
    x="weekday_name", 
    y="cnt", 
    title="Distribution of Bike Rentals Across the Week",
    labels={"cnt": "Total Bike Rentals", "weekday_name": "Day of the Week"},
    color="weekday_name",
    template="plotly_dark"
)

# Adjust width to make it shorter
fig_weekly_trends_box.update_layout(width=1000)  

# Show the updated visualization
fig_weekly_trends_box.show()

# Save as an image
fig_weekly_trends_box.write_image("box_plot.png", scale=3)
fig_weekly_trends_box.write_image("11.png", scale=3)










