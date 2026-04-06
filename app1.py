import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import base64

# ---------------------------------
# SIMPLE LOGIN SYSTEM
# ---------------------------------

def login():

    st.markdown("## 🔐 HR Analytics Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_button = st.button("Login")

    if login_button:

        if username == "admin" and password == "admin123":
            st.session_state["logged_in"] = True
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid Username or Password")

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Employee Attrition Dashboard",
    layout="wide"
)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ---------------------------------
# BACKGROUND VIDEO
# ---------------------------------

video_file = open("hr_dashboard_video.mp4", "rb")
video_bytes = video_file.read()
video_base64 = base64.b64encode(video_bytes).decode()

st.markdown(
f"""
<style>

.stApp {{
background: transparent;
}}

#background-video {{
position: fixed;
right: 0;
bottom: 0;
min-width: 100%;
min-height: 100%;
object-fit: cover;
z-index: -1;
}}

/* -------- MAIN DASHBOARD TITLE -------- */

h1 {{
font-size: 48px !important;
color: white !important;
font-weight: 800 !important;
text-shadow:
0px 0px 10px rgba(255,255,255,0.9),
0px 0px 20px rgba(255,255,255,0.7),
0px 0px 35px rgba(0,170,255,0.8);
}}

/* -------- SIDEBAR MAIN TITLE -------- */

section[data-testid="stSidebar"] h1 {{
font-size: 24px !important;
font-weight: 700 !important;
color: white !important;
text-shadow:
0px 0px 8px rgba(255,255,255,0.9),
0px 0px 15px rgba(0,170,255,0.6);
}}

/* -------- SIDEBAR SECTION HEADER -------- */

section[data-testid="stSidebar"] h2 {{
font-size: 20px !important;
font-weight: 600 !important;
color: white !important;
text-shadow:
0px 0px 6px rgba(255,255,255,0.8),
0px 0px 12px rgba(0,170,255,0.6);
}}

/* -------- NORMAL TEXT -------- */

p, label {{
font-size: 16px !important;
color: white;
}}

/* -------- SIDEBAR LABELS -------- */

section[data-testid="stSidebar"] label {{
font-size: 15px !important;
color: white !important;
}}

/* -------- SIDEBAR FILTER TEXT FIX -------- */

/* Sidebar dropdown selected value */
section[data-testid="stSidebar"] div[data-baseweb="select"] span {{
color: black !important;
}}

/* Sidebar dropdown options */
section[data-testid="stSidebar"] div[data-baseweb="popover"] li {{
color: black !important;
}}

/* Sidebar dropdown input text */
section[data-testid="stSidebar"] div[data-baseweb="select"] input {{
color: black !important;
}}

/* Sidebar number inputs (Age / Income) */
section[data-testid="stSidebar"] input {{
color: black !important;
background-color: white !important;
}}

/* Dropdown background */
section[data-testid="stSidebar"] div[data-baseweb="select"] {{
background-color: white !important;
}}

/* -------- CHART TITLES -------- */

.js-plotly-plot .plotly .gtitle {{
font-size: 22px !important;
color: white !important;
}}

/* -------- GLASS EFFECT -------- */

[data-testid="stPlotlyChart"] {{
background: rgba(255,255,255,0.15);
backdrop-filter: blur(12px);
border-radius: 15px;
padding: 15px;
border: 1px solid rgba(255,255,255,0.25);
box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}}

div[data-testid="metric-container"] {{
background: rgba(255,255,255,0.2);
backdrop-filter: blur(12px);
border-radius: 15px;
padding: 10px;
border: 1px solid rgba(255,255,255,0.25);
}}

section[data-testid="stSidebar"] {{
background: rgba(255,255,255,0.15);
backdrop-filter: blur(10px);
}}

</style>

<video autoplay muted loop id="background-video">
<source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
</video>

""",
unsafe_allow_html=True
)

# ---------------------------------
# LOGIN CHECK
# ---------------------------------

if not st.session_state["logged_in"]:
    login()
    st.stop()

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
# MACHINE LEARNING MODEL
# ---------------------------------

# Copy dataframe for ML
ml_df = df.copy()

# Encode categorical columns
label_encoders = {}

for col in ml_df.select_dtypes(include="object").columns:
    le = LabelEncoder()
    ml_df[col] = le.fit_transform(ml_df[col])
    label_encoders[col] = le

# ---------------------------------
# SELECT FEATURES FOR MODEL
# ---------------------------------
# ---------------------------------
# SELECT FEATURES FOR MODEL
# ---------------------------------

features = [
    "Age",
    "Monthly_Income",
    "Years_at_Company",
    "Gender",
    "Department",
    "Job_Role",
    "Distance_From_Home",
    "Job_Satisfaction",
    "Overtime"
]

X = ml_df[features]

# Convert Attrition Yes/No → 1/0
y = df["Attrition"].map({"Yes":1, "No":0})

model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42
)

model.fit(X, y)

# ---------------------------------
# PAGE NAVIGATION
# ---------------------------------
st.sidebar.title("Employee Attrition for HR Analytics")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Single Prediction"]
)

filtered_df = df.copy()

# =====================================================
# DASHBOARD PAGE
# =====================================================
if page == "Dashboard":
    st.title("📊 Employee Attrition Analytics Dashboard")
    st.caption("Real-time HR insights based on employee attributes")

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

    overtime_filter = st.sidebar.selectbox(
        "Overtime",
        ["All"] + sorted(df["Overtime"].unique().tolist())
    )

    st.sidebar.subheader("Age Range")

    min_age = st.sidebar.number_input("Minimum Age", value=None, placeholder="Enter min age >20")
    max_age = st.sidebar.number_input("Maximum Age", value=None, placeholder="Enter max age <60")

    st.sidebar.subheader("Monthly Income Range")

    min_income = st.sidebar.number_input("Minimum Income", value=None, step=500,  placeholder="Enter min income >3000")
    max_income = st.sidebar.number_input("Maximum Income", value=None, step=500,  placeholder="Enter max income <20000")

    # -------------------------------
    # APPLY FILTERS
    # -------------------------------
    filtered_df = df.copy()

    if department != "All":
        filtered_df = filtered_df[filtered_df["Department"] == department]

    if gender != "All":
        filtered_df = filtered_df[filtered_df["Gender"] == gender]

    if job_role != "All":
        filtered_df = filtered_df[filtered_df["Job_Role"] == job_role]

    if overtime_filter != "All":
        filtered_df = filtered_df[filtered_df["Overtime"] == overtime_filter]

    if min_age is not None:
        filtered_df = filtered_df[filtered_df["Age"] >= min_age]

    if max_age is not None:
        filtered_df = filtered_df[filtered_df["Age"] <= max_age]

    if min_income is not None:
        filtered_df = filtered_df[filtered_df["Monthly_Income"] >= min_income]

    if max_income is not None:
        filtered_df = filtered_df[filtered_df["Monthly_Income"] <= max_income]

    # -------------------------------
    # KPI METRICS
    # -------------------------------
    total_employees = filtered_df.shape[0]
    employees_left = filtered_df[filtered_df["Attrition"] == "Yes"].shape[0]

    if total_employees > 0:
        attrition_rate = round((employees_left / total_employees) * 100, 2)
        avg_income = int(filtered_df["Monthly_Income"].mean())
    else:
        attrition_rate = 0
        avg_income = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Total Employees", total_employees)
    col2.metric("🚪 Employees Left", employees_left)
    col3.metric("📉 Attrition Rate (%)", f"{attrition_rate}%")
    col4.metric("💰 Avg Monthly Income", f"{avg_income:,}")

    st.divider()

    # -------------------------------
    # VISUALIZATIONS
    # -------------------------------
    c1, c2 = st.columns(2)

    # Attrition by Department
    fig1 = px.bar(
        filtered_df,
        x="Department",
        color="Attrition",
        barmode="group",
        title="Attrition by Department"
    )

    fig1.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    # Gender Pie
    fig2 = px.pie(
        filtered_df,
        names="Gender",
        color="Attrition",
        title="Attrition by Gender"
    )

    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    # Attrition by Job Role
    fig3 = px.bar(
        filtered_df,
        x="Job_Role",
        color="Attrition",
        title="Attrition by Job Role"
    )

    fig3.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    # Age Histogram
    fig4 = px.histogram(
        filtered_df,
        x="Age",
        color="Attrition",
        nbins=20,
        title="Age Distribution vs Attrition"
    )

    fig4.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    # Income Box Plot
    fig5 = px.box(
        filtered_df,
        x="Attrition",
        y="Monthly_Income",
        title="Monthly Income vs Attrition"
    )

    fig5.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    with c1:
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        st.plotly_chart(fig3, use_container_width=True)
        st.plotly_chart(fig4, use_container_width=True)

    st.plotly_chart(fig5, use_container_width=True)
    st.divider()
    st.info("""
    **Attrition Drivers Identified:**
    • Work-Life Balance (Overtime)
    • Financial factors (Income)
    • Demographics & Satisfaction
    """)

    with st.expander("📄 View Filtered Employee Data"):
        st.dataframe(filtered_df, use_container_width=True)
# =====================================================
# SINGLE PREDICTION PAGE
# =====================================================
if page == "Single Prediction":
    st.title("🤖 Predict Employee Attrition")

    col1, col2, col3 = st.columns(3)

    age = col1.number_input("Age", 18, 60)
    income = col2.number_input("Monthly Income", 3000, 20000)
    years = col3.number_input("Years at Company", 0, 40)

    gender = st.selectbox("Gender", label_encoders["Gender"].classes_)
    department = st.selectbox("Department", label_encoders["Department"].classes_)
    job_role = st.selectbox("Job Role", label_encoders["Job_Role"].classes_)
    distance = st.slider("Distance From Home", 1, 50)
    job_satisfaction = st.slider("Job Satisfaction", 1, 4)
    overtime = st.selectbox("Overtime", label_encoders["Overtime"].classes_)

    predict_button = st.button("Predict Attrition")

    if predict_button:

        input_data = pd.DataFrame([[

            age,
            income,
            years,
            label_encoders["Gender"].transform([gender])[0],
            label_encoders["Department"].transform([department])[0],
            label_encoders["Job_Role"].transform([job_role])[0],
            distance,
            job_satisfaction,
            label_encoders["Overtime"].transform([overtime])[0]

        ]], columns=[

            "Age",
            "Monthly_Income",
            "Years_at_Company",
            "Gender",
            "Department",
            "Job_Role",
            "Distance_From_Home",
            "Job_Satisfaction",
            "Overtime"

        ])

        prediction = model.predict(input_data)[0]

        if prediction == 1:
            st.error("⚠️ Employee Likely to Leave")
        else:
            st.success("✅ Employee Likely to Stay")