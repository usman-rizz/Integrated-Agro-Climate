import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Rainfall & Climate Data Analysis",
    page_icon="🌧️",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("4) cleaned_weather_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# --------------------------------------------------
# SIDEBAR – PROFILE & LINKS
# --------------------------------------------------
# st.sidebar.markdown("# )

st.sidebar.markdown(
    """
    <h1 style="color: #c7e0ea; margin-bottom:12px;">
        👤 Dashboard Author
    </h1>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("**Osman Rizz**  \nData Analyst | Climate Analytics")

st.sidebar.markdown("---")

# --------------------------------------------------
# SIDEBAR LINKS
# --------------------------------------------------

st.sidebar.markdown(
    """
    <h2 style="color:#d9ecf2; margin-bottom:12px;">
        🌐 Connect With Me
    </h2>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mohammad-usman736/) 

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)]("https://github.com/usman-rizz")

[![Hotmail](https://img.shields.io/badge/Outlook-0078D4?style=for-the-badge&logo=microsoft-outlook&logoColor=white)](mailto:Muhammad_usman2023@hotmail.com)  


"""
)
st.sidebar.markdown("---")

# --------------------------------------------------
# SIDEBAR FILTERS (Analytics)
# --------------------------------------------------

st.sidebar.markdown(
    """
    <h2 style="color:#d9ecf2; margin-bottom:12px;">
        📊 Analytics
    </h2>
    """,
    unsafe_allow_html=True
)

st.sidebar.metric("👁️ Views", "12.4K")
st.sidebar.metric("👍 Likes", "1.8K")
st.sidebar.metric("📈 Engagement", "14.5%")

st.sidebar.markdown("---")

# --------------------------------------------------
# SIDEBAR FILTERS (DROPDOWN)
# --------------------------------------------------

st.sidebar.markdown(
    """
    <h2 style="color:#d9ecf2; margin-bottom:12px;">
        🎛️ Filters
    </h2>
    """,
    unsafe_allow_html=True
)

selected_location = st.sidebar.selectbox(
    "Select Location",
    options=["All"] + sorted(df["Location"].unique())
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    options=["All"] + sorted(df["Year"].unique())
)

# Apply filters
filtered_df = df.copy()

if selected_location != "All":
    filtered_df = filtered_df[filtered_df["Location"] == selected_location]

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]

# --------------------------------------------------
# HEADER (YOUR COLOR THEME)
# --------------------------------------------------
st.markdown(
    """
<h1 style="text-align:center;
           background:#d9ecf2;
           color:#045174;
           font-size:45px;
           padding:20px;
           border-radius:12px;">
     <b> 🌧️ Rainfall & Climate Data Analysis</b>
</h1>
""",
    unsafe_allow_html=True
)

st.markdown("---")

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------
k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("🌡️ Avg Temperature (°C)", round(filtered_df["Temperature_Avg"].mean(), 2))
k2.metric("🌧️ Total Rainfall (mm)", round(filtered_df["Rainfall_Mm"].sum(), 2))
k3.metric("💧 Avg Humidity (%)", round(filtered_df["Relative_Humidity"].mean(), 2))
k4.metric("💨 Avg Wind Speed (m/s)", round(filtered_df["Wind_Speed_Max_2m"].mean(), 2))
k5.metric("☀️ Avg UV Index", round(filtered_df["Uv_Index"].mean(), 2))

st.markdown("---")

# --------------------------------------------------
# ROW 1 – TIME SERIES
# --------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    fig_temp = px.line(
        filtered_df,
        x="Date",
        y="Temperature_Avg",
        color="Location",
        title="Temperature Trend Over Time"
    )
    st.plotly_chart(fig_temp, use_container_width=True)

with c2:
    fig_rain = px.bar(
        filtered_df,
        x="Date",
        y="Rainfall_Mm",
        title="Rainfall Trend Over Time"
    )
    st.plotly_chart(fig_rain, use_container_width=True)

# --------------------------------------------------
# ROW 2 – DISTRIBUTIONS
# --------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    fig_hist = px.histogram(
        filtered_df,
        x="Temperature_Avg",
        nbins=40,
        title="Temperature Distribution"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    fig_box = px.box(
        filtered_df,
        x="Location",
        y="Relative_Humidity",
        title="Humidity Distribution by Location"
    )
    st.plotly_chart(fig_box, use_container_width=True)

# --------------------------------------------------
# ROW 3 – RELATIONSHIP ANALYSIS
# --------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    fig_scatter = px.scatter(
        filtered_df,
        x="Temperature_Avg",
        y="Rainfall_Mm",
        color="Location",
        title="Temperature vs Rainfall Relationship"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with c2:
    fig_uv = px.line(
        filtered_df,
        x="Date",
        y="Uv_Index",
        title="UV Index Variation Over Time"
    )
    st.plotly_chart(fig_uv, use_container_width=True)

# --------------------------------------------------
# ROW 4 – SEASONALITY
# --------------------------------------------------
monthly_df = filtered_df.groupby("Month").mean(numeric_only=True).reset_index()

fig_season = px.line(
    monthly_df,
    x="Month",
    y="Rainfall_Mm",
    title="Average Monthly Rainfall Pattern"
)

st.plotly_chart(fig_season, use_container_width=True)

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------
st.markdown("---")
st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df.head(25))
