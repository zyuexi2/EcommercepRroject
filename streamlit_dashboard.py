import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
# Streamlit App Layout
st.title("Tesla Analysis Dashboard")

intro_text = """
### Introduction
In the fast-paced world of electric vehicles, Tesla stands out as a beacon of innovation and ambition. 
Yet, with its rapid growth and technological advances come questions about safety and market performance. 
This blog post is the second installment in our journey to understand Tesla better, this time through the lens of Exploratory Data Analysis (EDA).
"""

st.markdown(intro_text)

# Load the provided datasets
deaths_df = pd.read_csv('https://raw.githubusercontent.com/zyuexi2/EcommercepRroject/main/Tesla%20Deaths%20-%20Deaths%20(3).csv')
miles_df = pd.read_csv('https://raw.githubusercontent.com/zyuexi2/EcommercepRroject/main/Tesla%20Deaths%20-%20Miles.csv')
sudden_acceleration_df = pd.read_csv('https://raw.githubusercontent.com/zyuexi2/EcommercepRroject/main/Tesla%20Deaths%20-%20Sudden%20Acceleration.csv')
tsla_df = pd.read_csv('https://raw.githubusercontent.com/zyuexi2/EcommercepRroject/main/TSLA.csv')


st.header("Yearly Deaths Analysis")
yearly_deaths = deaths_df.groupby('Year')[' Deaths '].sum().sort_values()

# Set the aesthetics for the plots
sns.set(style="whitegrid")


# Yearly deaths visualization
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=yearly_deaths.index, y=yearly_deaths.values, palette="viridis", ax=ax)
ax.set_title('Number of Deaths per Year in Tesla Incidents', fontsize=15)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Number of Deaths', fontsize=12)
ax.set_xticklabels(yearly_deaths.index, rotation=45)

# Use Streamlit's function to display the plot
st.pyplot(fig)






description_text = """
The bars represent the number of deaths each year, with a visible increase over time. Starting from a few deaths in 2013, 
there is a fluctuating pattern with a notable rise in deaths starting in 2019, peaking in 2021 with the highest number of fatalities represented by the tallest bar on the chart. 
The year 2022 shows a slight decrease from 2021 but remains high compared to the earlier years.
"""
st.markdown(description_text)




st.header("Sudden Acceleration Incidents by Tesla Model")
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(y=sudden_acceleration_df['Model'].value_counts().index, x=sudden_acceleration_df['Model'].value_counts().values, ax=ax)
st.pyplot(fig)


# Model selection from the user
model_choice = st.selectbox("Select a Tesla Model:", sudden_acceleration_df['Model'].unique())

# Filter the data based on the model
model_data = sudden_acceleration_df[sudden_acceleration_df['Model'] == model_choice]

# Sort the filtered data by 'Incident Date' and select the top 10 recent incidents
top_incidents = model_data.sort_values('Incident Date', ascending=False).head(10)

# Display the top 10 incident descriptions
if not top_incidents.empty:
    st.header(f"Top 10 Recent Incident Descriptions for {model_choice}")
    for i, row in top_incidents.iterrows():
        st.text(f"Incident {i+1}: {row['Details']}")
else:
    st.write(f"No incidents to display for model {model_choice}")




# Stock Data Analysis
st.header("Tesla Stock Data Analysis")
st.subheader("Closing Price of Tesla")
open_close = tsla_df[['Open', 'Close']]
fig = px.line(open_close, title='Opening & Closing Price of Tesla')
st.plotly_chart(fig)

# Streamlit app layout
st.title("Tesla Stock Change")
def load_stock_data():
    tsla_data = pd.read_csv('https://raw.githubusercontent.com/zyuexi2/EcommercepRroject/main/TSLA.csv', parse_dates=['Date'])
    # Make sure the 'Date' column is in the correct datetime format
    tsla_data['Date'] = pd.to_datetime(tsla_data['Date']).dt.date
    return tsla_data

tsla_df = load_stock_data()


# Define min and max dates for the date input
min_date = pd.to_datetime('2013-04-02').date()
max_date = pd.to_datetime('2022-03-24').date()

# Create a date input widget
input_date = st.date_input("Select a date", min_value=min_date, max_value=max_date, value=max_date)

# Filter data for the selected date
# The 'Date' column in the dataframe should also be of type `datetime.date` for comparison
selected_data = tsla_df[tsla_df['Date'] == input_date]

# Check if data is found for the selected date
if not selected_data.empty:
    high_price = selected_data['High'].iloc[0]
    low_price = selected_data['Low'].iloc[0]
    price_difference = high_price - low_price

    # Display the high and low prices and the difference
    st.write(f"High stock price on {input_date}: ${high_price:,.2f}")
    st.write(f"Low stock price on {input_date}: ${low_price:,.2f}")
    st.write(f"Difference between high and low prices on {input_date}: ${price_difference:,.2f}")
else:
    st.error("No data found for the selected date. Please choose another date.")


description_text2 = """
The two lines indicate the highest price (in blue) and the lowest price (in red) of the stock at various points in time. 
From the start of the graph to around 2020, both lines track closely together, showing relatively modest fluctuations in the stock’s price.
 However, starting in 2020, there is a significant increase in both the high and low values, indicating a period of substantial growth and volatility. 
 The high price line reaches its peak in late 2021 or early 2022, where it surpasses a value of 1200. After this peak, there’s a noticeable decline, but the prices remain at a much higher level than in the years preceding 2020. The graph displays the dynamic nature of Tesla’s stock prices, with a marked upturn in the latter part of the decade shown.
"""
st.markdown(description_text2)


# Ensure 'Date' columns are datetime objects
deaths_df['Date'] = pd.to_datetime(deaths_df['Date'], errors='coerce')
# If 'Date' is not already a column in tsla_df, this line will throw an error.
# Remove or comment it out if 'Date' is already a column.
tsla_df['Date'] = pd.to_datetime(tsla_df['Date'], errors='coerce')

# Prepare the deaths data
deaths_aggregated = deaths_df.groupby('Date').size().reset_index(name='Deaths')

# Merge the stock data with the aggregated deaths data
merged_df = pd.merge(tsla_df, deaths_aggregated, on='Date', how='left')
merged_df.fillna(0, inplace=True)  # Assuming no deaths on days without data

# Calculate the correlation
correlation = merged_df['Close'].corr(merged_df['Deaths'])
st.write(f"Correlation coefficient: {correlation}")

# Visualization with scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=merged_df, x='Close', y='Deaths', ax=ax)
ax.set_title("Scatter Plot of Tesla Stock Closing Price vs. Number of Deaths")
ax.set_xlabel("Stock Closing Price")
ax.set_ylabel("Number of Deaths")

# Use Streamlit's function to display the plot
st.pyplot(fig)


tsla_df['Date'] = pd.to_datetime(tsla_df['Date'])



description_text3 = """
Weak Positive Linear Relationship:
This coefficient indicates a weak positive linear relationship between Tesla’s stock price and the number of fatalities. This suggests that there is a slight tendency for the stock price and fatalities to increase together, albeit weakly.

Correlation ≠ Causation:
A fundamental principle in data analysis is that correlation does not equate to causation. Therefore, while the stock prices and reported fatalities move together to a small extent, we cannot assert that one causes the other.

A Multitude of Influencing Factors:
Tesla’s stock price is subject to a vast array of factors ranging from market trends and investor sentiment to company performance and broader economic indicators. Similarly, the number of reported deaths is a multifaceted issue, influenced by numerous variables beyond the company’s stock valuation.

Statistical Significance:
The correlation coefficient by itself does not confirm if the relationship observed is statistically significant.

In essence, the correlation coefficient revealed a slight positive relationship between the stock price and fatalities, yet this is a weak link and should be interpreted with caution.
 The stock market is a complex ecosystem, and Tesla’s valuation is contingent upon a host of factors, just as the occurrence of fatalities has its independent determinants.

Final Thoughts
As I conclude this phase of our data-driven exploration into Tesla’s stock performance and reported fatalities, my journey has been as enlightening as it has been intricate. 
I’ve unearthed a tenuous connection between stock prices and safety incidents, a relationship that speaks to the multifaceted nature of market forces and public perception.

Moving forward, my experience paves the way to investigate wider questions.
 For instance, how do similar correlations play out in other high-innovation industries? 
 Could a comparative study across different companies reveal common patterns, or would it highlight the uniqueness of each firm’s situation?"""
st.markdown(description_text3)