import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Employee Attrition Dashboard",
    layout="wide"
)

# ---------------------------------
# LOAD DATA
# ---------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("employee_attrition_datasett.csv")

df = load_data()

# ---------------------------------
# SIDEBAR FILTERS (USER INPUTS)
# ---------------------------------
st.sidebar.header("🔍 Employee Filters")

department = st.sidebar.selectbox(
    "Department",
    ["All"] + sorted(df["Department"].unique().tolist())
)

gender = st.sidebar.selectbox(
    "Gender",
    ["All"] + sorted(df["Gender"].unique().tolist())
)

job_role = st.sidebar.selectbox(
    "Job Role",
    ["All"] + sorted(df["Job_Role"].unique().tolist())
)

marital_status = st.sidebar.selectbox(
    "Marital Status",
    ["All"] + sorted(df["Marital_Status"].unique().tolist())
)

age_range = st.sidebar.slider(
    "Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (int(df["Age"].min()), int(df["Age"].max()))
)

income_range = st.sidebar.slider(
    "Monthly Income Range",
    int(df["Monthly_Income"].min()),
    int(df["Monthly_Income"].max()),
    (int(df["Monthly_Income"].min()), int(df["Monthly_Income"].max()))
)

# =====================================================
# STEP 1️⃣ APPLY FILTERS (CRITICAL FIX)
# =====================================================
filtered_df = df.copy()

if department != "All":
    filtered_df = filtered_df[filtered_df["Department"] == department]

if gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender]

if job_role != "All":
    filtered_df = filtered_df[filtered_df["Job_Role"] == job_role]

if marital_status != "All":
    filtered_df = filtered_df[filtered_df["Marital_Status"] == marital_status]

filtered_df = filtered_df[
    (filtered_df["Age"] >= age_range[0]) &
    (filtered_df["Age"] <= age_range[1])
]

filtered_df = filtered_df[
    (filtered_df["Monthly_Income"] >= income_range[0]) &
    (filtered_df["Monthly_Income"] <= income_range[1])
]

# =====================================================
# STEP 2️⃣ KPI CALCULATIONS (USING filtered_df)
# =====================================================
total_employees = filtered_df.shape[0]
employees_left = filtered_df[filtered_df["Attrition"] == "Yes"].shape[0]

if total_employees > 0:
    attrition_rate = round((employees_left / total_employees) * 100, 2)
else:
    attrition_rate = 0

avg_income = int(filtered_df["Monthly_Income"].mean()) if total_employees > 0 else 0
avg_years_company = round(filtered_df["Years_at_Company"].mean(), 1) if total_employees > 0 else 0

# ---------------------------------
# DASHBOARD TITLE
# ---------------------------------
st.title("📊 Employee Attrition Analytics Dashboard")
st.caption("Real-time HR insights based on employee attributes")

# =====================================================
# STEP 3️⃣ KPI DISPLAY
# =====================================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Total Employees", total_employees)
col2.metric("🚪 Employees Left", employees_left)
col3.metric("📉 Attrition Rate (%)", attrition_rate)
col4.metric("💰 Avg Monthly Income", avg_income)

st.divider()

# ---------------------------------
# VISUALIZATIONS
# ---------------------------------

# Attrition by Department
fig_dept = px.bar(
    filtered_df,
    x="Department",
    color="Attrition",
    title="Attrition by Department",
    barmode="group"
)
st.plotly_chart(fig_dept, use_container_width=True)

# Attrition by Job Role
fig_role = px.bar(
    filtered_df,
    x="Job_Role",
    color="Attrition",
    title="Attrition by Job Role"
)
st.plotly_chart(fig_role, use_container_width=True)

# Attrition by Gender
fig_gender = px.pie(
    filtered_df,
    names="Gender",
    color="Attrition",
    title="Attrition by Gender"
)
st.plotly_chart(fig_gender, use_container_width=True)

# Age vs Attrition
fig_age = px.histogram(
    filtered_df,
    x="Age",
    color="Attrition",
    nbins=20,
    title="Age Distribution vs Attrition"
)
st.plotly_chart(fig_age, use_container_width=True)

# Income vs Attrition
fig_income = px.box(
    filtered_df,
    x="Attrition",
    y="Monthly_Income",
    title="Monthly Income vs Attrition"
)
st.plotly_chart(fig_income, use_container_width=True)

# ---------------------------------
# DATA PREVIEW
# ---------------------------------
with st.expander("📄 View Filtered Employee Data"):
    st.dataframe(filtered_df)
