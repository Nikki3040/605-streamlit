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

st.subheader("Introduction")
st.markdown("As cities continue to grow and shift towards sustainable transportation, bike-sharing systems have emerged as a crucial component of urban mobility. They provide a flexible, eco-friendly, and cost-effective means of transportation for daily commuters, recreational riders, and tourists alike. However, understanding when and how these bike-sharing systems are utilized is essential for optimizing station locations, adjusting bike availability, and improving overall service efficiency. In this data story, we analyze the UCI Bike Sharing Dataset, which contains detailed records of bike rental activity in Washington, D.C., collected over two years (2011-2012). This dataset provides valuable insights into hourly and daily rental patterns, influenced by factors such as time of day, day of the week, seasonality, and weather conditions. By leveraging visual analytics, we explore how different user behaviors emerge based on commuting patterns, weekday vs. weekend usage, and impact of weather conditions, time of day, seasonal variations, and user behavior.")

st.subheader("Objective")
st.markdown("Through our analysis, we aim to answer key questions about bike-sharing trends: How do rental patterns fluctuate across different timescales? Are there noticeable variations between weekdays and weekends? How do external factors like weather, temperature, and wind speed shape bike-sharing demand? How do rental behaviors differ between registered users and casual riders? By addressing these questions, we seek to uncover actionable insights that can help urban planners, policymakers, and bike-sharing companies optimize service availability, improve user experience, and better accommodate evolving urban mobility needs.")

st.subheader("Dataset")
st.markdown("The dataset provides detailed records of bike-sharing rentals in Washington, D.C., including temporal attributes such as date, year, month, hour, day of the week, and holiday/workday status, as well as weather conditions like temperature, humidity, wind speed, and general weather. It also includes user information, distinguishing between casual and registered users, along with total bike rentals. Two primary files were analyzed: hour.csv, which contains hourly bike rental data with 17,379 records, and day.csv, which includes daily bike rental data with 731 records. With this rich dataset, let's dive into the patterns that shape bike-sharing trends.")

st.subheader("Methodology")

st.subheader("Part 1. The Rhythm of Ridership: When Do People Ride?")

# Bike Usage Across Different Seasons
#st.subheader("Bike Usage Across Different Seasons")
fig_season_box = px.box(day_df, x='season_name', y='cnt', color='season_name',
                        title="Bike Usage Across Different Seasons",
                        labels={'cnt': 'Total Bike Rentals', 'season_name': 'Season'})
st.plotly_chart(fig_season_box)
st.markdown("Analysis: The box plot illustrating bike rentals across seasons reveals the presence of clear seasonal trends in bike rentals, with significantly higher usage during warmer months (Spring and Summer seasons) and lower usage in colder seasons (Winter and Fall). Spring and Summer show the highest median rentals, exceeding 4000, with a wide range of variability, suggesting that factors like weather conditions and special events influence demand. Contrastingly, Winter has the lowest median rentals, around 2000, with some days experiencing near-zero usage, which may be due to typical harsh weather conditions that occur during the Winter months. Fall exhibits moderate bike usage, but with a few extreme outliers. The variability in Summer and Spring highlights fluctuating demand, while Winter and Fall rentals are more consistent but lower overall. This analysis underscores the strong influence of seasonality on bike rentals, indicating that bike-sharing programs should optimize bike availability based on seasonal trends to maximize efficiency and rider satisfaction.")

# Long-term Trends in Bike Usage
fig_trend = px.line(day_df, x='dteday', y='cnt', title="Long-term Trends in Bike Usage Over the Years",
                    labels={'dteday': 'Date', 'cnt': 'Total Bike Rentals'}, markers=True)
st.plotly_chart(fig_trend)
st.markdown("Analysis: The time series plot shows clear long-term trends in bike usage, with strong seasonal patterns and overall fluctuations in bike rentals. There is an evident increase in bike rentals starting in early 2011, reaching peaks during the warmer months and declining in the winter, a pattern that repeats across multiple years. The highest usage is observed in mid-2012, which might be explained by either increased adoption of bike-sharing programs or favorable weather and infrastructure improvements. However, there is a visible decline in ridership toward the end of 2012 and into early 2013, likely due to seasonal effects rather than a long-term downward trend. These fluctuations indicate that while ridership has generally grown, external factors such as weather, policy changes, and infrastructure development may influence the consistency of bike usage over time.")

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
st.markdown("Analysis: The interactive bar chart provides a detailed view of hourly bike demand across different days of the week, offering insights into how usage patterns vary between weekdays and weekends. On weekdays (Monday to Friday), there are two distinct peaks in bike rentals: one in the morning between 7-9 AM and another in the evening between 4-7 PM. These trends indicate that a significant portion of users rely on bike-sharing services for commuting to work or school. In contrast, weekends (Saturday and Sunday) exhibit a more gradual increase in demand throughout the day, with peak usage occurring later in the morning and early afternoon, around 10 AM - 6 PM. This suggests a shift from structured commuting-based rentals to recreational or leisurely bike rides. Late-night and early-morning bike rentals remain consistently low across all days, with minimal activity between 12 AM and 5 AM, indicating limited demand during these hours. However, weekend nights show slightly higher late-night rentals, likely due to social outings or nightlife activities. Additionally, Fridays stand out as a transitional day, displaying characteristics of both weekday commuting behavior and increasing evening leisure activity. Unlike other weekdays, Friday’s evening peak extends later into the night, reflecting a gradual shift into weekend patterns. Overall, this visualization highlights the clear distinction between weekday and weekend bike rental behaviors. Weekdays are characterized by structured demand tied to work and school schedules, while weekends cater more to flexible, leisure-oriented biking. These insights can be valuable for bike-sharing companies and urban planners, helping them optimize bike availability, adjust station placements, and enhance overall user experience based on demand fluctuations.")

# Bike Usage Trends Over the Week
# Map weekday numbers (0-6) to actual names
weekday_mapping = {
    0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
    4: "Thursday", 5: "Friday", 6: "Saturday"}
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
    template="plotly_dark")

fig_weekly_trends_line.update_traces(line=dict(width=3), textposition="top center")
fig_weekly_trends_line.update_layout(width=800)
st.title("Bike Usage Trends Over the Week")
st.plotly_chart(fig_weekly_trends_line)

# Distribution of Bike Rentals Across the Week
st.subheader("Distribution of Bike Rentals Across the Week")
fig_weekly_trends_box = px.box(day_df, x="weekday_name", y="cnt",
                               title="Distribution of Bike Rentals Across the Week",
                               labels={"cnt": "Total Bike Rentals", "weekday_name": "Day of the Week"},
                               color="weekday_name")
st.plotly_chart(fig_weekly_trends_box)





# Hourly Bike Rental Trends: Holidays vs. Weekends vs. Workdays
# Convert date columns to datetime format
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

# Line chart to show rental trends across different times of day
fig_hourly_rentals = px.line(hourly_avg, x="hr", y="cnt", color="day_type",
                             title="Hourly Bike Rental Trends: Holidays vs. Weekends vs. Workdays",
                             labels={"hr": "Hour of the Day", "cnt": "Average Rentals", "day_type": "Day Type"},
                             template="plotly_dark", markers=True, width=fig_width)

fig_hourly_rentals.update_traces(line=dict(width=3))
fig_hourly_rentals.update_layout(legend_title_text="Day Type")

# Streamlit App
st.title("Bike Usage Trends")

# Show weekly trends chart
st.subheader("Bike Usage Trends Over the Week")
st.plotly_chart(fig_weekly_trends_line)

# Show hourly rental trends chart
st.subheader("Hourly Bike Rental Trends: Holidays vs. Weekends vs. Workdays")
st.plotly_chart(fig_hourly_rentals)




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







