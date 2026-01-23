import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Employee Attrition Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------ LOAD DATA ------------------
df = pd.read_csv("employee_attrition_datasett.csv")

# Clean column names
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(" ", "", regex=True)

# ------------------ TITLE ------------------
st.markdown(
    "<h1 style='text-align: center;'>📊 Employee Attrition Analytics Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Interactive HR insights to analyze employee attrition</p>",
    unsafe_allow_html=True
)

st.markdown("---")

# ------------------ KPIs ------------------
total_emp = len(df)
attrition_count = len(df[df['Attrition'] == 'Yes'])
attrition_rate = round((attrition_count / total_emp) * 100, 2)

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("👥 Total Employees", total_emp)
kpi2.metric("🚪 Employees Left", attrition_count)
kpi3.metric("📉 Attrition Rate (%)", attrition_rate)

st.markdown("---")

# ------------------ SIDEBAR FILTERS ------------------
st.sidebar.header("🔍 Filter Employee Data")

department = st.sidebar.multiselect(
    "Select Department",
    options=df['Department'].unique(),
    default=df['Department'].unique()
)

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

jobrole = st.sidebar.multiselect(
    "Select Job_Role",
    options=df['Job_Role'].unique(),
    default=df['Job_Role'].unique()
)

filtered_df = df[
    (df['Department'].isin(department)) &
    (df['Gender'].isin(gender)) &
    (df['Job_Role'].isin(jobrole))
]

# ------------------ VISUALIZATIONS ------------------
st.markdown("## 📌 Attrition Insights")

col1, col2 = st.columns(2)

# Attrition by Department
with col1:
    fig_dept = px.bar(
        filtered_df,
        x='Department',
        color='Attrition',
        title="Attrition by Department",
        text_auto=True
    )
    st.plotly_chart(fig_dept, use_container_width=True)

# Attrition by Gender
with col2:
    fig_gender = px.pie(
        filtered_df,
        names='Gender',
        color='Attrition',
        title="Attrition by Gender"
    )
    st.plotly_chart(fig_gender, use_container_width=True)

# Attrition by Job Role
fig_job = px.bar(
    filtered_df,
    x='Job_Role',
    color='Attrition',
    title="Attrition by Job_Role"
)
st.plotly_chart(fig_job, use_container_width=True)

# Monthly Income vs Attrition
fig_income = px.box(
    filtered_df,
    x='Attrition',
    y='Monthly_Income',
    title="Monthly_Income vs Attrition"
)
st.plotly_chart(fig_income, use_container_width=True)

# ------------------ INSIGHTS SECTION ------------------
st.markdown("## 🧠 Key Insights")
st.markdown("""
- Employees working in specific departments show higher attrition.
- Job roles with higher workload and overtime have increased attrition.
- Lower monthly income is associated with higher employee turnover.
- Gender-wise and role-wise analysis helps HR teams plan retention strategies.
""")

st.success("✅ Dashboard loaded successfully")