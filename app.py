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
st.markdown("**Visualizations**")
st.markdown("Several interactive visualizations were created using Plotly and Streamlit to better understand bike rental trends. Clustering analysis (KMeans) was performed to segment rental demand into Low, Medium, and High categories, with normalization applied to numerical features before clustering. A scatter plot visualized bike rental demand by temperature, categorizing demand levels using KMeans. The impact of temperature, humidity, and wind speed on rentals under different weather conditions was analyzed using facet-based scatter plots, ensuring proper layout adjustments for clarity. Additionally, stacked bar charts were employed to examine seasonal preferences among casual vs. registered riders. All plots were integrated into a Streamlit dashboard, allowing interactive exploration of rental patterns. The methodology ensured that both regression analysis and clustering provided actionable insights into bike demand dynamics.")
st.markdown("**Predictive Modeling of Bike Rentals**")
st.markdown("The predictive modeling process was designed to forecast bike rental demand based on various environmental and temporal features. The dataset was first preprocessed, including handling missing values, encoding categorical variables, and ensuring numerical consistency. A train-test split (80-20) was performed to allow robust model evaluation. Multiple regression models were implemented, including Linear Regression, Ridge, Lasso, ElasticNet, Bayesian Ridge, Huber, Decision Trees, Random Forest, Gradient Boosting, XGBoost, and k-Nearest Neighbors. Each model was evaluated based on Mean Squared Error (MSE) and R² scores to assess performance. Hyperparameter tuning using GridSearchCV was conducted for selected models like Random Forest, Gradient Boosting, and Decision Trees to optimize predictive accuracy. The best model’s feature importance was analyzed using the Gradient Boosting Regressor, revealing which factors most influenced bike rental trends. Finally, the results were visualized in Streamlit, allowing users to compare model performance and explore feature significance interactively.")
st.markdown("**Predictive Modeling for Clustering-Based Demand Classification**")
st.markdown("A separate approach was taken to cluster rental demand patterns based on environmental conditions, particularly temperature and humidity. The dataset underwent feature scaling using StandardScaler to normalize values before applying KMeans clustering with three clusters: Low Demand, Medium Demand, and High Demand. The clustering results were assigned human-readable labels, providing an intuitive understanding of demand segmentation. To further explore the demand structure, a scatter plot was generated to visualize bike rental demand based on temperature, with colors representing different demand clusters. Additionally, a k-Nearest Neighbors (KNN) model was prepared for future classification tasks to determine how well the temperature-humidity combination predicts rental demand levels. The visualization was implemented using Plotly and Streamlit, offering an interactive way to explore how weather conditions influence rental demand patterns.")


st.subheader("Part 1. The Rhythm of Ridership: When Do People Ride?")
#############################################################
# VISUALIZATION 1: Bike Usage Across Different Seasons
st.markdown("<h4>1A. How does bike usage vary across different seasons?</h4>", unsafe_allow_html=True)
fig_season_box = px.box(day_df, x='season_name', y='cnt', color='season_name',
                        title="Bike Usage Across Different Seasons",
                        labels={'cnt': 'Total Bike Rentals', 'season_name': 'Season'})
st.plotly_chart(fig_season_box)
st.markdown("**Analysis**: The box plot illustrating bike rentals across seasons reveals the presence of clear seasonal trends in bike rentals, with significantly higher usage during warmer months (Spring and Summer seasons) and lower usage in colder seasons (Winter and Fall). Spring and Summer show the highest median rentals, exceeding 4000, with a wide range of variability, suggesting that factors like weather conditions and special events influence demand. Contrastingly, Winter has the lowest median rentals, around 2000, with some days experiencing near-zero usage, which may be due to typical harsh weather conditions that occur during the Winter months. Fall exhibits moderate bike usage, but with a few extreme outliers. The variability in Summer and Spring highlights fluctuating demand, while Winter and Fall rentals are more consistent but lower overall. This analysis underscores the strong influence of seasonality on bike rentals, indicating that bike-sharing programs should optimize bike availability based on seasonal trends to maximize efficiency and rider satisfaction.")

#############################################################
# VISUALIZATION 2: Long-term Trends in Bike Usage
st.markdown("<h4>1B. What are the long-term trends in bike usage over the years?</h4>", unsafe_allow_html=True)
fig_trend = px.line(day_df, x='dteday', y='cnt', title="Long-term Trends in Bike Usage Over the Years",
                    labels={'dteday': 'Date', 'cnt': 'Total Bike Rentals'}, markers=True)
st.plotly_chart(fig_trend)
st.markdown("**Analysis**: The time series plot shows clear long-term trends in bike usage, with strong seasonal patterns and overall fluctuations in bike rentals. There is an evident increase in bike rentals starting in early 2011, reaching peaks during the warmer months and declining in the winter, a pattern that repeats across multiple years. The highest usage is observed in mid-2012, which might be explained by either increased adoption of bike-sharing programs or favorable weather and infrastructure improvements. However, there is a visible decline in ridership toward the end of 2012 and into early 2013, likely due to seasonal effects rather than a long-term downward trend. These fluctuations indicate that while ridership has generally grown, external factors such as weather, policy changes, and infrastructure development may influence the consistency of bike usage over time.")

#############################################################
# VISUALIZATION 3: Hourly Bike Demand Across Days of the Week
st.markdown("<h4>1C. How does bike demand fluctuate throughout the day?</h4>", unsafe_allow_html=True)
weekday_mapping = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
                   4: "Thursday", 5: "Friday", 6: "Saturday"}
hour_df["weekday"] = hour_df["weekday"].map(weekday_mapping)
hourly_trends = hour_df.groupby(["hr", "weekday"])["cnt"].mean().reset_index()
fig_hourly_animated = px.bar(hourly_trends, x="hr", y="cnt", animation_frame="weekday",
                             title="Hourly Bike Demand Across Days of the Week",
                             labels={"cnt": "Average Rentals", "hr": "Hour of Day", "weekday": "Day of the Week"},
                             color="cnt", color_continuous_scale="viridis")
st.plotly_chart(fig_hourly_animated)
st.markdown("**Analysis**: The interactive bar chart provides a detailed view of hourly bike demand across different days of the week, offering insights into how usage patterns vary between weekdays and weekends. On weekdays (Monday to Friday), there are two distinct peaks in bike rentals: one in the morning between 7-9 AM and another in the evening between 4-7 PM. These trends indicate that a significant portion of users rely on bike-sharing services for commuting to work or school. In contrast, weekends (Saturday and Sunday) exhibit a more gradual increase in demand throughout the day, with peak usage occurring later in the morning and early afternoon, around 10 AM - 6 PM. This suggests a shift from structured commuting-based rentals to recreational or leisurely bike rides. Late-night and early-morning bike rentals remain consistently low across all days, with minimal activity between 12 AM and 5 AM, indicating limited demand during these hours. However, weekend nights show slightly higher late-night rentals, likely due to social outings or nightlife activities. Additionally, Fridays stand out as a transitional day, displaying characteristics of both weekday commuting behavior and increasing evening leisure activity. Unlike other weekdays, Friday’s evening peak extends later into the night, reflecting a gradual shift into weekend patterns. Overall, this visualization highlights the clear distinction between weekday and weekend bike rental behaviors. Weekdays are characterized by structured demand tied to work and school schedules, while weekends cater more to flexible, leisure-oriented biking. These insights can be valuable for bike-sharing companies and urban planners, helping them optimize bike availability, adjust station placements, and enhance overall user experience based on demand fluctuations.")

#############################################################
# VISUALIZATION 4: Bike Usage Trends Over the Week
st.markdown("<h4>1D. Are there noticeable weekly trends in bike usage?</h4>", unsafe_allow_html=True)
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
st.markdown("**Analysis**: The line chart shows a gradual increase in bike rentals from Sunday to Friday, with a peak on Thursday and Friday, before dropping slightly on Saturday. This suggests that bike usage is highest during the weekdays, likely driven by commuters using bikes for work or school. The slight decline on weekends could indicate that fewer people are commuting, although there is still significant bike usage. The box plot complements this by showing the distribution and variability of bike rentals for each day. It reveals that while weekdays generally have higher median rentals, the spread is also greater, suggesting higher fluctuations in demand. This could be due to variations in weather, events, or different commuting patterns. Interestingly, weekend rentals have a wider range, indicating some days see substantial usage spikes, possibly due to recreational activities. Together, these two visuals suggest that bike rentals are primarily driven by weekday commuting patterns, but weekends still see significant usage, albeit with more variability. This insight can be useful for bike-sharing companies or city planners to optimize availability based on expected demand throughout the week.")

#############################################################
# VISUALIZATION 6: Holiday and Workday Trends in Ridership
st.markdown("<h4>1E. How do bike rental patterns differ between workdays and holidays throughout the day?</h4>", unsafe_allow_html=True)
# Convert date columns to datetime format
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
# Map weekday and holiday labels
hour_df["day_type"] = hour_df.apply(lambda row: 
                                    "Holiday" if row["holiday"] == 1 else 
                                    ("Weekend" if row["weekday"] in [0, 6] else "Workday"), axis=1)
# Aggregate hourly rentals based on the new categories
hourly_avg = hour_df.groupby(["hr", "day_type"])["cnt"].mean().reset_index()
# Line chart visualization
fig_hourly_rentals = px.line(
    hourly_avg, 
    x="hr", 
    y="cnt", 
    color="day_type",
    title="Hourly Bike Rental Trends",
    labels={"hr": "Hour of the Day", "cnt": "Average Rentals", "day_type": "Day Type"},
    template="plotly_dark", 
    markers=True,
    width=1000)

fig_hourly_rentals.update_traces(line=dict(width=3))
fig_hourly_rentals.update_layout(legend_title_text="Day Type")
st.plotly_chart(fig_hourly_rentals, use_container_width=True)
st.markdown("**Analysis**: The line chart highlights key differences in bike rental patterns between workdays and holidays. On workdays, rentals peak sharply around 8 AM and 5-6 PM, aligning with commuting hours, indicating that many users rely on bike-sharing for work or school travel. In contrast, holiday rentals are more evenly distributed throughout the day, suggesting that usage is more recreational. Overall, rentals are higher on workdays, especially during peak hours, reinforcing the role of bike-sharing in daily commutes. These insights can help optimize bike availability, ensuring sufficient supply during peak commuting hours while maintaining balanced distribution for recreational riders on holidays.")

#############################################################
# VISUALIZATION 7: Hourly Bike Rental Trends Across Months
st.markdown("<h4>1F. How does bike rental demand fluctuate across different months of the year? Are there noticeable seasonal patterns in hourly usage?</h4>", unsafe_allow_html=True)
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
st.markdown("**Analysis**: This visualization reveals distinct seasonal patterns in bike rental demand. Warmer months, particularly May through September, exhibit significantly higher peaks, especially in the afternoon and evening, suggesting increased recreational and leisure usage. Conversely, colder months (November to February) show lower overall rentals, likely due to unfavorable weather conditions. A consistent two-peak pattern emerges across most months, with demand surging around 8 AM and 5-6 PM, aligning with typical commuting hours. However, during summer months (June–August), the afternoon peak is notably higher, indicating that more people are renting bikes for activities beyond commuting. Additionally, July and August experience the highest rental volumes, while December and January see the lowest, further emphasizing the correlation between temperature, daylight hours, and biking behavior. Another key insight is that during warmer months, usage remains sustained throughout the day, while in colder months, demand is concentrated primarily around peak commute times. These findings suggest that bike rental usage is strongly season-dependent, with warmer months encouraging more widespread and extended use beyond essential travel needs.")
            
#############################################################
st.subheader("Part 2. Riding with the Weather: What Influences Bike Demand?")
#############################################################
# VISUALIZATION 8: Impact of Temperature on Bike Rentals
st.markdown("<h4>2A. What is the impact of temperature on bike rentals? (e.g., is there an optimal temperature for bike rentals?)</h4>", unsafe_allow_html=True)
fig_temp = px.scatter(day_df, x='temp', y='cnt', title="Impact of Temperature on Bike Rentals",
                      labels={'temp': 'Temperature (Normalized)', 'cnt': 'Total Bike Rentals'},
                      color='cnt', color_continuous_scale='turbo')
st.plotly_chart(fig_temp)
st.markdown("**Analysis**: The scatter plot shown above demonstrates a clear positive correlation between temperature and bike rentals, indicating that warmer temperatures generally lead to higher bike usage. At lower normalized temperatures (around 0.2), bike rentals remain relatively low, suggesting that colder conditions discourage ridership. As temperature increases, the number of rentals rises steadily, peaking at moderate to high normalized temperatures (between 0.6 and 0.8), where total bike rentals frequently exceed 6000. However, at the highest temperature levels, there appears to be a slight plateau, suggesting that extreme heat may not necessarily lead to increased ridership and could even discourage some users. This pattern implies that there is an optimal temperature range for bike rentals, likely in mild to warm conditions, beyond which extreme heat may act as a deterrent. Understanding this relationship between temperature and bike rentals, can aid city planners and bike-sharing programs optimize operations by ensuring adequate bike availability during peak temperature conditions while also considering the potential impact of extreme weather.")

#############################################################
# VISUALIZATION 9: Impact of Humidity on Bike Rentals
st.markdown("<h4>2B. How does humidity influence bike rental demand?</h4>", unsafe_allow_html=True)
fig_humidity = px.scatter(day_df, x='hum', y='cnt', title="Impact of Humidity on Bike Rentals",
                          labels={'hum': 'Humidity (Normalized)', 'cnt': 'Total Bike Rentals'},
                          color='cnt', color_continuous_scale='magma')
st.plotly_chart(fig_humidity)
st.markdown("**Analysis**: The scatter plot illustrates the relationship between humidity and bike rental demand, showing a weak but noticeable trend. At lower humidity levels (below 0.4), bike rentals vary widely but tend to be lower on average, with fewer instances of peak usage. As humidity increases, rental counts remain relatively stable, suggesting that moderate humidity does not significantly impact ridership. However, at very high humidity levels (above 0.8), bike rentals appear to slightly decline, indicating that extreme humidity may discourage biking due to discomfort or unfavorable weather conditions such as heavy moisture or rain. While humidity does not exhibit a strong linear relationship with bike rentals, there may be an optimal mid-range where ridership is less affected, whereas extreme conditions—either too dry or too humid—might contribute to decreased demand. Understanding this relationship can help in predicting rental fluctuations and planning for weather-related ridership patterns.")

#############################################################
# VISUALIZATION 10: Are bike rentals more affected by temperature or humidity?
st.markdown("<h4>2C. Are bike rentals more affected by temperature or humidity?</h4>", unsafe_allow_html=True)
import numpy as np  
num_bins = 10
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
    yaxis_title_font=dict(size=16))
st.plotly_chart(fig_heatmap, use_container_width=True)
st.markdown("**Analysis**: A clear trend of interaction between temperature, humidity, and bike rentals, emerges from the heatmap. The intensity of rentals is higher in mid to high-range temperatures (0.5 - 0.9 normalized scale), where demand increases significantly. The most significant observation is the sharp increase in bike rentals when temperatures are at their peak, suggesting that warmer weather encourages higher ridership. In contrast, humidity exhibits a more gradual and less pronounced effect on rentals. While extreme humidity levels (both low and high) seem to slightly suppress demand, bike rentals remain relatively stable across most humidity ranges. This suggests that while riders may be slightly deterred by excessive humidity, temperature plays a far greater role in influencing ridership patterns. The brightest yellow sections (indicating the highest rental volumes) align with warmer temperatures rather than specific humidity levels. This reinforces the idea that bike-sharing systems should prioritize temperature forecasts over humidity when optimizing fleet distribution and availability.")
            
#############################################################
# VISUALIZATION 11: What are the effects of wind speed on bike usage?
st.markdown("<h4>2D. What are the effects of wind speed on bike usage?</h4>", unsafe_allow_html=True)
fig_wind1 = px.scatter(
    hour_df, 
    x='windspeed', 
    y='cnt',
    title='Effect of Wind Speed on Bike Rentals',
    labels={'windspeed': 'Wind Speed (Normalized)', 'cnt': 'Total Bike Rentals'},
    opacity=0.5,
    color='cnt',
    color_continuous_scale='Viridis', 
    template='plotly_dark')

fig_wind1.update_layout(
    template="plotly_dark",
    font=dict(size=14),
    title_font=dict(size=20),
    xaxis_title_font=dict(size=16),
    yaxis_title_font=dict(size=16),
    width=900,  
    height=550)
st.plotly_chart(fig_wind1, use_container_width=True)
st.markdown("**Analysis**: The scatter plot reveals an interesting insight: wind speed has a relatively weak impact on total bike rentals. The density of high-rental points remains fairly consistent across lower wind speeds (0.0 - 0.5 normalized scale), suggesting that most riders are not significantly discouraged by mild to moderate wind conditions. However, as wind speed increases beyond 0.5 normalized scale, rental numbers begin to decline, with fewer instances of high usage. This trend indicates that while riders may tolerate light winds, stronger winds likely dissuade potential users, reducing ridership. The bright yellow clusters are concentrated in low-wind conditions, suggesting that bike-sharing programs should account for high-wind days when predicting demand. Although wind speed is not as influential as temperature, extreme wind conditions could warrant strategic bike redistribution to areas with more shelter or alternative transport options.")

#############################################################
# VISUALIZATION 12: How does different weather conditions (e.g., clear, misty, rainy) affect ridership?
st.markdown("<h4>2E. How does different weather conditions (e.g., clear, misty, rainy) affect ridership?</h4>", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
# **Map weathersit to category names**
weather_map = {
    1: 'Clear',
    2: 'Misty',
    3: 'Light Rain/Snow',
    4: 'Heavy Rain/Snow'}
hour_df['weathersit_name'] = hour_df['weathersit'].map(weather_map)
fig_weather = px.box(
    hour_df, x='weathersit_name', y='cnt', color='weathersit_name',
    title='Bike Rentals by Weather Condition',
    labels={'weathersit_name': 'Weather Condition', 'cnt': 'Total Bike Rentals'},
    color_discrete_sequence=['#E63946', '#F4A261', '#2A9D8F', '#E9C46A'],
    points=False)
fig_weather.update_layout(
    template="plotly_dark",
    font=dict(size=14),
    title_font=dict(size=20), 
    xaxis_title_font=dict(size=16), 
    yaxis_title_font=dict(size=16),
    width=900,
    height=550)
fig_weather.update_traces(
    hovertemplate="Weather Condition: %{x}<br>Min: %{y|.2f}<br>Median: %{median|.2f}<br>Max: %{upperfence|.2f}")
st.plotly_chart(fig_weather, use_container_width=True)
st.markdown("**Analysis**: Weather plays a crucial role in shaping bike-sharing patterns, as seen in the visualizations above. Clear weather consistently sees the highest ridership, with a wide range of total rentals. This suggests that more users are comfortable cycling in favorable conditions. As conditions shift to misty/ cloudy or light rain/ snow, the median number of rentals declines, and variability narrows, indicating fewer peak usage days. However, ridership remains relatively stable, suggesting that moderate weather changes do not completely deter riders. In heavy rain/ ice pellets/ thunderstorms, bike rentals drop significantly. The box plot reveals a much lower median with minimal variation, and scatter plots show very few high-rental points under these conditions. This suggests that extreme weather acts as a strong deterrent, reducing overall riders. For bike-sharing operators, this means optimizing fleet distribution on clear days to accommodate higher demand while considering alternative transportation incentives or service modifications during severe weather.")
          
#############################################################
st.subheader("Part 3. Who’s Riding? Comparing Casual and Registered Users")
#############################################################
# VISUALIZATION 14: How do casual riders and registered users differ in their rental patterns, compare on holiday and non-holiday? Which time of day is most popular for casual users versus registered users?

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

hourly_rentals_holiday = hour_df[hour_df['holiday'] == 1].groupby('hr')[['casual', 'registered']].mean().reset_index()
hourly_rentals_non_holiday = hour_df[hour_df['holiday'] == 0].groupby('hr')[['casual', 'registered']].mean().reset_index()
hourly_rentals_total = hour_df.groupby('hr')[['casual', 'registered']].mean().reset_index()

fig_rental_comparison = make_subplots(
    rows=3, cols=1, subplot_titles=["Holiday Rentals", "Non-Holiday Rentals", "Total Rentals"])

casual_color = "#1E90FF"
registered_color = "#FF6347"

fig_rental_comparison.add_trace(go.Bar(
    x=hourly_rentals_holiday["hr"], y=hourly_rentals_holiday["casual"],
    name="Casual Riders", marker_color=casual_color, opacity=0.8), row=1, col=1)

fig_rental_comparison.add_trace(go.Bar(
    x=hourly_rentals_holiday["hr"], y=hourly_rentals_holiday["registered"],
    name="Registered Users", marker_color=registered_color, opacity=0.6), row=1, col=1)

fig_rental_comparison.add_trace(go.Bar(
    x=hourly_rentals_non_holiday["hr"], y=hourly_rentals_non_holiday["casual"],
    name="Casual Riders", marker_color=casual_color, opacity=0.8, showlegend=False), row=2, col=1)

fig_rental_comparison.add_trace(go.Bar(
    x=hourly_rentals_non_holiday["hr"], y=hourly_rentals_non_holiday["registered"],
    name="Registered Users", marker_color=registered_color, opacity=0.6, showlegend=False), row=2, col=1)

fig_rental_comparison.add_trace(go.Bar(
    x=hourly_rentals_total["hr"], y=hourly_rentals_total["casual"],
    name="Casual Riders", marker_color=casual_color, opacity=0.8, showlegend=False), row=3, col=1)

fig_rental_comparison.add_trace(go.Bar(
    x=hourly_rentals_total["hr"], y=hourly_rentals_total["registered"],
    name="Registered Users", marker_color=registered_color, opacity=0.6, showlegend=False), row=3, col=1)

fig_rental_comparison.update_layout(
    title="Peak Rental Times: Casual Riders vs. Registered Users (Average Rentals)",
    xaxis=dict(title="Hour of the Day", tickmode="array", tickvals=list(range(24)), ticktext=[str(i) for i in range(24)]),
    xaxis2=dict(title="Hour of the Day", tickmode="array", tickvals=list(range(24)), ticktext=[str(i) for i in range(24)]),
    xaxis3=dict(title="Hour of the Day", tickmode="array", tickvals=list(range(24)), ticktext=[str(i) for i in range(24)]),
    yaxis=dict(title="Avg Rentals per Hour", range=[0, 400]),
    yaxis2=dict(title="Avg Rentals per Hour", range=[0, 400]),
    yaxis3=dict(title="Avg Rentals per Hour", range=[0, 400]),
    template='plotly_dark',
    width=1200, height=900,
    font=dict(size=18),
    title_font=dict(size=24),
    xaxis_title_font=dict(size=20),
    yaxis_title_font=dict(size=20),
    margin=dict(t=80, b=80, l=60, r=60))
st.plotly_chart(fig_rental_comparison, use_container_width=True)

#############################################################
# VISUALIZATION 15: Do casual riders exhibit different seasonal preferences than registered riders?
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Debugging: Ensure the dataset loads
st.write("Dataset Loaded Successfully ✅")
st.write(hour_df.head())  # Display first 5 rows

# **Map season numbers to names**
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
seasonal_rentals_avg = hour_df.groupby('season')[['casual', 'registered']].mean().reset_index()
seasonal_rentals_avg['season'] = seasonal_rentals_avg['season'].map(season_map)

# Debugging: Check if grouping worked
st.write("Seasonal Rental Averages ✅")
st.write(seasonal_rentals_avg)

# **Define colors**
casual_color = "#1E90FF"  # Dodger Blue
registered_color = "#FF6347"  # Tomato Red

# **Create Stacked Bar Chart**
fig_seasonal_stacked_avg = go.Figure()

fig_seasonal_stacked_avg.add_trace(go.Bar(
    x=seasonal_rentals_avg['season'],
    y=seasonal_rentals_avg['casual'],
    name='Casual Riders',
    marker_color=casual_color,
    opacity=0.8
))

fig_seasonal_stacked_avg.add_trace(go.Bar(
    x=seasonal_rentals_avg['season'],
    y=seasonal_rentals_avg['registered'],
    name='Registered Users',
    marker_color=registered_color,
    opacity=0.6
))

# **Layout Configuration**
fig_seasonal_stacked_avg.update_layout(
    title="Seasonal Preferences: Casual Riders vs. Registered Users (Average Rentals)",
    xaxis_title="Season",
    yaxis_title="Average Rentals per Hour",
    barmode="stack",
    bargap=0.2,
    template='plotly_dark',
    width=1200, height=600,  # Adjusted for Streamlit display
    font=dict(size=20),
    title_font=dict(size=32),
    xaxis_title_font=dict(size=24),
    yaxis_title_font=dict(size=24)
)

# **Display chart in Streamlit**
st.title("Seasonal Preferences: Casual vs. Registered Riders")
st.plotly_chart(fig_seasonal_stacked_avg, use_container_width=True)

#############################################################

# Predictive Modelling 1

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, BayesianRidge, HuberRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
import streamlit as st
import pandas as pd
from tabulate import tabulate

# **Convert categorical columns to numeric**
if 'weathersit' in hour_df.columns:
    hour_df['weathersit'] = hour_df['weathersit'].astype(str)  # Convert to string
# **Feature selection**
features = ['temp', 'hum', 'windspeed', 'hr', 'weekday', 'weathersit', 'holiday']
X = hour_df[features].copy()
y = hour_df['cnt'].copy()
# **Ensure all features are numeric**
X = pd.get_dummies(X, drop_first=True)  # One-hot encoding for categorical columns
# **Train-Test Split**
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

st.title("📊 Bike Rentals Prediction - Model Comparison & Optimization")
# **Train Multiple Models**
st.subheader("🔍 Model Comparison")
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Lasso Regression": Lasso(alpha=1.0),
    "ElasticNet Regression": ElasticNet(alpha=1.0, l1_ratio=0.5),
    "Bayesian Ridge Regression": BayesianRidge(),
    "Huber Regression": HuberRegressor(),
    "Random Forest Regression": RandomForestRegressor(n_estimators=100),
    "Decision Tree Regression": DecisionTreeRegressor(max_depth=5),
    "Gradient Boosting Regression": GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3),
    "Support Vector Regression": SVR(kernel='rbf'),
    "K-Nearest Neighbors": KNeighborsRegressor(n_neighbors=5),
    "XGBoost": XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=3),
    "Extra Trees Regression": ExtraTreesRegressor(n_estimators=100)}

# Train and evaluate models
results = {}
for name, model in models.items():
    try:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        results[name] = {"MSE": mse, "R²": r2}
    except Exception as e:
        results[name] = {"MSE": "Error", "R²": str(e)}  # Capture errors

# Display results
results_df = pd.DataFrame(results).T
st.write("### 📊 Model Performance Comparison")
st.dataframe(results_df)

# **Grid Search Results**
results = {
    "Model": [
        "Random Forest",
        "Gradient Boosting",
        "k-Nearest Neighbors",
        "Decision Tree",
        "Extra Trees"],
    "Best Parameters": [
        "{'max_depth': 20, 'min_samples_leaf': 1}",
        "{'learning_rate': 0.1, 'max_depth': 7, 'min_samples_leaf': 3}",
        "{'n_neighbors': 9, 'p': 2, 'weights': 'distance'}",
        "{'max_depth': 10, 'min_samples_leaf': 4}",
        "{'max_depth': 20, 'min_samples_leaf': 1}"],
    "Best R² Score": [
        0.836,
        0.847,
        0.775,
        0.792,
        0.835]}
results_df = pd.DataFrame(results)
st.subheader("🏆 Grid Search Results - Best Model Parameters & R² Scores")
st.dataframe(results_df)

# **Feature Importance using Gradient Boosting Regressor**
st.subheader("📊 Feature Importance - Gradient Boosting Regressor")
# Best hyperparameters for Gradient Boosting
best_params = {'learning_rate': 0.1, 'max_depth': 7, 'min_samples_leaf': 3}
# Train Gradient Boosting Model
gb_model = GradientBoostingRegressor(**best_params, random_state=42)
gb_model.fit(X_train, y_train)
# Extract Feature Importance
feature_importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": gb_model.feature_importances_})

# Bar chart for feature importance
fig = px.bar(
    feature_importance_df.sort_values(by="Importance", ascending=True),
    x="Importance",
    y="Feature",
    orientation='h',
    title="Feature Importance - Gradient Boosting Regressor",
    labels={"Importance": "Feature Importance Score", "Feature": "Features"},
    color="Importance",
    color_continuous_scale="Blues",
    template='plotly_dark')
st.plotly_chart(fig, use_container_width=True)
st.markdown("Analysis: Based on the results of the comparative table, it can be observed that that Gradient Boosting Regression is the most effective model for predicting bike rental demand, with an R² score of 0.8469. Hour of the day emerged as the most critical factor, reflecting peak rental times during commuting hours. Temperature and weekday trends also significantly influenced demand, with higher rentals on warm days and workdays showing distinct peaks. Adverse weather conditions such as rain and snow were found to reduce rentals considerably. The presence of holidays showed varied effects on demand, with some seasonal variations. These insights suggest that bike-sharing systems can optimize availability by reallocating bikes dynamically during peak hours, adjusting pricing strategies based on weather conditions, and implementing targeted promotions to increase ridership during weekends and holidays. Ultimately, machine learning models offer a robust approach to forecasting demand, aiding both urban mobility planners and bike-sharing companies in improving operational efficiency and customer satisfaction.")

#############################################################

# Predictive Modelling 2

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split

st.title("🚴‍♂️ Bike Rental Demand Clustering & Visualization")

# Feature selection
features = ["temp", "hum", "windspeed", "season", "weekday", "workingday", "weathersit"]
X_full = day_df[features]
y = day_df["cnt"]  # Target: Total rentals
# Normalize numerical features
scaler = StandardScaler()
X_full_scaled = scaler.fit_transform(X_full)
# Apply KMeans Clustering (3 Clusters)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
day_df["demand_cluster"] = kmeans.fit_predict(X_full_scaled)
# Demand Labels
demand_labels = {0: "Medium Demand", 1: "High Demand", 2: "Low Demand"}
day_df["demand_category"] = day_df["demand_cluster"].map(demand_labels)
# KNN Setup for Decision Boundary (Using Temp & Humidity)
X_2D = day_df[["temp", "hum"]].values
y_2D = day_df["demand_cluster"]
# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_2D, y_2D, test_size=0.2, random_state=42)

# **📌 Interactive Scatter Plot for Demand**
st.subheader("📊 Bike Rental Demand Classification by Temperature")

fig_scatter = px.scatter(
    day_df, x="temp", y="cnt", color="demand_category",
    title="Bike Rental Demand Classification by Temperature",
    labels={"temp": "Temperature", "cnt": "Total Rentals", "demand_category": "Demand Category"},
    template="plotly_dark",
    width=800)
st.plotly_chart(fig_scatter, use_container_width=True)











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











