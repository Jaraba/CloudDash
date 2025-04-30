import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# Load data (replace with your CSV/API call)
df = pd.read_csv("oilprod.csv")

# Clean the column headers
df.columns = [
    col.replace(" Field Production of Crude Oil (Thousand Barrels)", "") if col != "Date" else col
    for col in df.columns
]

# Unpivot the data: keep 'Date' as identifier, melt the rest
df = df.melt(id_vars=["Date"], 
                    var_name="State", 
                    value_name="Production (Thousand Barrels)")

df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year

all_states = df["State"].unique().tolist() #Define the list of all available states

state_options = ["All"] + all_states

#'''   #### STREAMLIT PART ####   '''

# Title
st.title("📊 Oil & Gas Production Dashboard")

# Sidebar title
st.sidebar.title("Filters")

# Year range filter
min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

start_year, end_year = st.sidebar.slider(
    "Select year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Dropdown for states

    # selected_state = st.selectbox("Select State", df["State"].unique())   Unique selection

selected_states = st.sidebar.multiselect(
    "Select States",
    options=state_options,
    default=["All"]
)

# Filter data

# If "All" is selected, use all states
if "All" in selected_states:
    filtered_states = all_states
    filtered_states.remove("U.S.")
else:
    filtered_states = selected_states

filtered_data = df[
    (df["State"].isin(filtered_states)) &
    (df["Year"] >= start_year) &
    (df["Year"] <= end_year)
]

'''Line chart'''
# Plot production trends
fig = px.line(
    filtered_data,
    x="Date",
    y="Production (Thousand Barrels)",
    color="State",
    title="Oil Production Trends by State"
)

st.plotly_chart(fig)

'''Bar chart'''
#Bar chart
bar_data = filtered_data.groupby("State")["Production (Thousand Barrels)"].sum().reset_index()

bar_fig = px.bar(
    bar_data,
    x="State",
    y="Production (Thousand Barrels)",
    title="Total Production by State",
    text_auto=True
)
st.plotly_chart(bar_fig)

'''Pie chart'''

# Pie chart: Share of production per state
pie_fig = px.pie(
    bar_data,
    names="State",
    values="Production (Thousand Barrels)",
    title="Production Share by State"
)
st.plotly_chart(pie_fig)

# Show raw data
if st.checkbox("Show raw data"):
    st.write(filtered_data)