import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go


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
#############################################################
# VISUALIZATION 1: Bike Usage Across Different Seasons
#st.subheader("Bike Usage Across Different Seasons")
fig_season_box = px.box(day_df, x='season_name', y='cnt', color='season_name',
                        title="Bike Usage Across Different Seasons",
                        labels={'cnt': 'Total Bike Rentals', 'season_name': 'Season'})
st.plotly_chart(fig_season_box)
st.markdown("Analysis: The box plot illustrating bike rentals across seasons reveals the presence of clear seasonal trends in bike rentals, with significantly higher usage during warmer months (Spring and Summer seasons) and lower usage in colder seasons (Winter and Fall). Spring and Summer show the highest median rentals, exceeding 4000, with a wide range of variability, suggesting that factors like weather conditions and special events influence demand. Contrastingly, Winter has the lowest median rentals, around 2000, with some days experiencing near-zero usage, which may be due to typical harsh weather conditions that occur during the Winter months. Fall exhibits moderate bike usage, but with a few extreme outliers. The variability in Summer and Spring highlights fluctuating demand, while Winter and Fall rentals are more consistent but lower overall. This analysis underscores the strong influence of seasonality on bike rentals, indicating that bike-sharing programs should optimize bike availability based on seasonal trends to maximize efficiency and rider satisfaction.")
#############################################################
# VISUALIZATION 2: Long-term Trends in Bike Usage
fig_trend = px.line(day_df, x='dteday', y='cnt', title="Long-term Trends in Bike Usage Over the Years",
                    labels={'dteday': 'Date', 'cnt': 'Total Bike Rentals'}, markers=True)
st.plotly_chart(fig_trend)
st.markdown("Analysis: The time series plot shows clear long-term trends in bike usage, with strong seasonal patterns and overall fluctuations in bike rentals. There is an evident increase in bike rentals starting in early 2011, reaching peaks during the warmer months and declining in the winter, a pattern that repeats across multiple years. The highest usage is observed in mid-2012, which might be explained by either increased adoption of bike-sharing programs or favorable weather and infrastructure improvements. However, there is a visible decline in ridership toward the end of 2012 and into early 2013, likely due to seasonal effects rather than a long-term downward trend. These fluctuations indicate that while ridership has generally grown, external factors such as weather, policy changes, and infrastructure development may influence the consistency of bike usage over time.")
#############################################################
# VISUALIZATION 3: Hourly Bike Demand Across Days of the Week
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
#############################################################
# VISUALIZATION 4: Bike Usage Trends Over the Week
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
    text=weekly_trends["cnt"].round(2),
    title="Bike Usage Trends Over the Week",
    labels={"cnt": "Average Bike Rentals", "weekday_name": "Day of the Week"},
    markers=True,
    template="plotly_dark")
fig_weekly_trends_line.update_traces(line=dict(width=3), textposition="top center")
fig_weekly_trends_line.update_layout(width=800)
#st.title("Bike Usage Trends Over the Week")
st.plotly_chart(fig_weekly_trends_line)

#############################################################
# VISUALIZATION 5: Distribution of Bike Rentals Across the Week
fig_weekly_trends_box = px.box(day_df, x="weekday_name", y="cnt",
                               title="Distribution of Bike Rentals Across the Week",
                               labels={"cnt": "Total Bike Rentals", "weekday_name": "Day of the Week"},
                               color="weekday_name")
st.plotly_chart(fig_weekly_trends_box)
st.markdown("Analysis: The line chart shows a gradual increase in bike rentals from Sunday to Friday, with a peak on Thursday and Friday, before dropping slightly on Saturday. This suggests that bike usage is highest during the weekdays, likely driven by commuters using bikes for work or school. The slight decline on weekends could indicate that fewer people are commuting, although there is still significant bike usage. The box plot complements this by showing the distribution and variability of bike rentals for each day. It reveals that while weekdays generally have higher median rentals, the spread is also greater, suggesting higher fluctuations in demand. This could be due to variations in weather, events, or different commuting patterns. Interestingly, weekend rentals have a wider range, indicating some days see substantial usage spikes, possibly due to recreational activities. Together, these two visuals suggest that bike rentals are primarily driven by weekday commuting patterns, but weekends still see significant usage, albeit with more variability. This insight can be useful for bike-sharing companies or city planners to optimize availability based on expected demand throughout the week.")

#############################################################
# VISUALIZATION 6: Hourly Bike Rental Trends Across Months
# Map numeric month to names
month_mapping = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"}
hour_df["month_name"] = hour_df["mnth"].map(month_mapping)
# Group by hour and month to get average rentals
hourly_monthly_rentals = hour_df.groupby(["month_name", "hr"])["cnt"].mean().reset_index()
fig_facet_interactive = px.line(
    hourly_monthly_rentals, x="hr", y="cnt", color="month_name",
    title="Hourly Bike Rental Trends Across Months",
    labels={"cnt": "Avg Rentals", "hr": "Hour of the Day", "month_name": "Month"},
    template="plotly_dark",
    facet_col="month_name",
    facet_col_wrap=4,  # Display facets in a grid format
    line_group="month_name",
    markers=True)
fig_facet_interactive.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig_facet_interactive.update_layout(
    font=dict(size=12),
    showlegend=False,
    height=700,
    width=1000)
st.plotly_chart(fig_facet_interactive)
st.markdown("Analysis: This visualization reveals distinct seasonal patterns in bike rental demand. Warmer months, particularly May through September, exhibit significantly higher peaks, especially in the afternoon and evening, suggesting increased recreational and leisure usage. Conversely, colder months (November to February) show lower overall rentals, likely due to unfavorable weather conditions. A consistent two-peak pattern emerges across most months, with demand surging around 8 AM and 5-6 PM, aligning with typical commuting hours. However, during summer months (June–August), the afternoon peak is notably higher, indicating that more people are renting bikes for activities beyond commuting. Additionally, July and August experience the highest rental volumes, while December and January see the lowest, further emphasizing the correlation between temperature, daylight hours, and biking behavior. Another key insight is that during warmer months, usage remains sustained throughout the day, while in colder months, demand is concentrated primarily around peak commute times. These findings suggest that bike rental usage is strongly season-dependent, with warmer months encouraging more widespread and extended use beyond essential travel needs.")
            
#############################################################
st.subheader("Part 2. Riding with the Weather: What Influences Bike Demand?")
#############################################################
# VISUALIZATION 7: Impact of Temperature on Bike Rentals
fig_temp = px.scatter(day_df, x='temp', y='cnt', title="Impact of Temperature on Bike Rentals",
                      labels={'temp': 'Temperature (Normalized)', 'cnt': 'Total Bike Rentals'},
                      color='cnt', color_continuous_scale='turbo')
st.plotly_chart(fig_temp)
st.markdown("Analysis: The scatter plot shown above demonstrates a clear positive correlation between temperature and bike rentals, indicating that warmer temperatures generally lead to higher bike usage. At lower normalized temperatures (around 0.2), bike rentals remain relatively low, suggesting that colder conditions discourage ridership. As temperature increases, the number of rentals rises steadily, peaking at moderate to high normalized temperatures (between 0.6 and 0.8), where total bike rentals frequently exceed 6000. However, at the highest temperature levels, there appears to be a slight plateau, suggesting that extreme heat may not necessarily lead to increased ridership and could even discourage some users. This pattern implies that there is an optimal temperature range for bike rentals, likely in mild to warm conditions, beyond which extreme heat may act as a deterrent. Understanding this relationship between temperature and bike rentals, can aid city planners and bike-sharing programs optimize operations by ensuring adequate bike availability during peak temperature conditions while also considering the potential impact of extreme weather.")
#############################################################
# VISUALIZATION 8: Impact of Humidity on Bike Rentals
fig_humidity = px.scatter(day_df, x='hum', y='cnt', title="Impact of Humidity on Bike Rentals",
                          labels={'hum': 'Humidity (Normalized)', 'cnt': 'Total Bike Rentals'},
                          color='cnt', color_continuous_scale='magma')
st.plotly_chart(fig_humidity)
st.markdown("Analysis: The scatter plot illustrates the relationship between humidity and bike rental demand, showing a weak but noticeable trend. At lower humidity levels (below 0.4), bike rentals vary widely but tend to be lower on average, with fewer instances of peak usage. As humidity increases, rental counts remain relatively stable, suggesting that moderate humidity does not significantly impact ridership. However, at very high humidity levels (above 0.8), bike rentals appear to slightly decline, indicating that extreme humidity may discourage biking due to discomfort or unfavorable weather conditions such as heavy moisture or rain. While humidity does not exhibit a strong linear relationship with bike rentals, there may be an optimal mid-range where ridership is less affected, whereas extreme conditions—either too dry or too humid—might contribute to decreased demand. Understanding this relationship can help in predicting rental fluctuations and planning for weather-related ridership patterns.")
#############################################################
# VISUALIZATION 9: Are bike rentals more affected by temperature or humidity?
import numpy as np  # Ensure numpy is imported

num_bins = 10

# Ensure 'hour_df' is used instead of 'hour'
temp_bins = np.linspace(hour_df['temp'].min(), hour_df['temp'].max(), num_bins + 1)
hum_bins = np.linspace(0, hour_df['hum'].max(), num_bins + 1)

hour_df['temp_bin'] = pd.cut(hour_df['temp'], bins=temp_bins, include_lowest=True)
hour_df['hum_bin'] = pd.cut(hour_df['hum'], bins=hum_bins)

# Creating pivot table for heatmap
heatmap_data = hour_df.pivot_table(index='temp_bin', columns='hum_bin', values='cnt', aggfunc='mean')

# Formatting bin labels
heatmap_data.index = [f"{float(bin.left):.2f} - {float(bin.right):.2f}" for bin in heatmap_data.index]
heatmap_data.columns = [f"{float(bin.left):.2f} - {float(bin.right):.2f}" for bin in heatmap_data.columns]

# Creating the heatmap figure
fig_heatmap = go.Figure(
    data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Viridis',
        colorbar=dict(title="Avg Bike Rentals")
    )
)

fig_heatmap.update_layout(
    title='Effect of Temperature and Humidity on Bike Rentals',
    xaxis_title='Humidity (%)',
    yaxis_title='Temperature (°C)',
    template='plotly_dark',
    width=1000,
    height=600,
    font=dict(size=14),
    title_font=dict(size=20),
    xaxis_title_font=dict(size=16),
    yaxis_title_font=dict(size=16)
)

# Display the plot in Streamlit
st.plotly_chart(fig_heatmap, use_container_width=True)


#############################################################
# VISUALIZATION 10: What are the effects of wind speed on bike usage?



#############################################################
# VISUALIZATION 11: How does different weather conditions (e.g., clear, misty, rainy) affect ridership?


#############################################################
# VISUALIZATION 12: How do temperature, humidity, and wind speed influence bike rental patterns under different weather conditions, and which factor has the strongest impact in each scenario?


#############################################################
st.subheader("Part 3. Who’s Riding? Comparing Casual and Registered Users")
#############################################################
# VISUALIZATION 13: How do casual riders and registered users differ in their rental patterns, compare on holiday and non-holiday? Which time of day is most popular for casual users versus registered users?

#############################################################
# VISUALIZATION 14: Do casual riders exhibit different seasonal preferences than registered riders?






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











