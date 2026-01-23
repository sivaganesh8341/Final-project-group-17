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

try:
    df = load_data()
    df.columns = [c.strip() for c in df.columns]
except Exception as e:
    st.error(f"Error loading CSV file: {e}")
    st.stop()

# ---------------------------------
# SIDEBAR FILTERS
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

# =====================================================
# ✅ UPDATED — OPTIONAL MANUAL AGE INPUT (NO LIMITS)
# =====================================================
st.sidebar.subheader("Age Range (Optional)")

min_age = st.sidebar.number_input(
    "Minimum Age",
    value=None,
    placeholder="Enter min age"
)

max_age = st.sidebar.number_input(
    "Maximum Age",
    value=None,
    placeholder="Enter max age"
)

# =====================================================
# ✅ UPDATED — OPTIONAL MANUAL INCOME INPUT (NO LIMITS)
# =====================================================
st.sidebar.subheader("Monthly Income Range (Optional)")

min_income = st.sidebar.number_input(
    "Minimum Income",
    value=None,
    placeholder="Enter min income",
    step=500
)

max_income = st.sidebar.number_input(
    "Maximum Income",
    value=None,
    placeholder="Enter max income",
    step=500
)

# =====================================================
# STEP 1️⃣ APPLY FILTERS
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

# ✅ Age filter only if user entered value
if min_age is not None:
    filtered_df = filtered_df[filtered_df["Age"] >= min_age]

if max_age is not None:
    filtered_df = filtered_df[filtered_df["Age"] <= max_age]

# ✅ Income filter only if user entered value
if min_income is not None:
    filtered_df = filtered_df[filtered_df["Monthly_Income"] >= min_income]

if max_income is not None:
    filtered_df = filtered_df[filtered_df["Monthly_Income"] <= max_income]

# =====================================================
# STEP 2️⃣ KPI CALCULATIONS
# =====================================================
total_employees = filtered_df.shape[0]
employees_left = filtered_df[filtered_df["Attrition"] == "Yes"].shape[0]

if total_employees > 0:
    attrition_rate = round((employees_left / total_employees) * 100, 2)
    avg_income = int(filtered_df["Monthly_Income"].mean())
else:
    attrition_rate = 0
    avg_income = 0

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
col3.metric("📉 Attrition Rate (%)", f"{attrition_rate}%")
col4.metric("💰 Avg Monthly Income", f"{avg_income:,}")

st.divider()

# ---------------------------------
# VISUALIZATIONS
# ---------------------------------
c1, c2 = st.columns(2)

with c1:
    st.plotly_chart(px.bar(filtered_df, x="Department", color="Attrition", barmode="group", title="Attrition by Department"), use_container_width=True)
    st.plotly_chart(px.pie(filtered_df, names="Gender", color="Attrition", title="Attrition by Gender"), use_container_width=True)

with c2:
    st.plotly_chart(px.bar(filtered_df, x="Job_Role", color="Attrition", title="Attrition by Job Role"), use_container_width=True)
    st.plotly_chart(px.histogram(filtered_df, x="Age", color="Attrition", nbins=20, title="Age Distribution vs Attrition"), use_container_width=True)

st.plotly_chart(px.box(filtered_df, x="Attrition", y="Monthly_Income", title="Monthly Income vs Attrition"), use_container_width=True)

# =====================================================
# STEP 4️⃣ REASON & ATTRIBUTES ANALYSIS
# =====================================================
st.divider()
st.header("🎯 Deep Dive: Why are Employees Leaving?")

reason_col1, reason_col2 = st.columns(2)

with reason_col1:
    ot_col = "OverTime" if "OverTime" in filtered_df.columns else "Overtime"
    if ot_col in filtered_df.columns:
        st.plotly_chart(
            px.histogram(filtered_df, x=ot_col, color="Attrition", barmode="group",
                         title="Reason: Impact of Overtime on Attrition"),
            use_container_width=True
        )

    if "Distance_From_Home" in filtered_df.columns:
        st.plotly_chart(
            px.box(filtered_df, x="Attrition", y="Distance_From_Home",
                   title="Reason: Commute Distance vs Attrition"),
            use_container_width=True
        )

with reason_col2:
    if "Job_Satisfaction" in filtered_df.columns:
        st.plotly_chart(
            px.histogram(filtered_df, x="Job_Satisfaction", color="Attrition",
                         barmode="group", title="Reason: Job Satisfaction Level"),
            use_container_width=True
        )

    leavers_df = filtered_df[filtered_df["Attrition"] == "Yes"]
    if not leavers_df.empty:
        st.plotly_chart(
            px.sunburst(leavers_df, path=["Marital_Status", "Gender"],
                        title="Attrition Profile: Marital Status & Gender"),
            use_container_width=True
        )
    else:
        st.info("No data available for leavers in this selection.")

# ---------------------------------
# Scatter
# ---------------------------------
ot_hover = [ot_col] if ot_col in filtered_df.columns else []

st.plotly_chart(
    px.scatter(
        filtered_df,
        x="Years_at_Company",
        y="Monthly_Income",
        color="Attrition",
        size="Age",
        hover_data=["Job_Role"] + ot_hover,
        title="Tenure vs Income (Bubble Size = Age)"
    ),
    use_container_width=True
)

# ---------------------------------
# INSIGHTS
# ---------------------------------
st.info("""
**Attrition Drivers Identified:**
• Work-Life Balance (Overtime)
• Financial factors (Income)
• Demographics & Satisfaction
""")

with st.expander("📄 View Filtered Employee Data"):
    st.dataframe(filtered_df, use_container_width=True)
