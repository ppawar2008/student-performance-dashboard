
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Student Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Student Performance Analytics")
st.write("Analyze student marks and attendance with ease.")

data = {
    "Student": ["Aarav", "Priya", "Rahul", "Neha", "Dev",
                "Aarav", "Priya", "Rahul", "Neha", "Dev",
                "Aarav", "Priya", "Rahul", "Neha", "Dev"],
    "Subject": ["Maths"] * 5 + ["Python"] * 5 + ["Statistics"] * 5,
    "Marks": [85, 92, 68, 78, 88, 90, 86, 72, 95, 80,
              76, 89, 65, 91, 84],
    "Attendance": [90, 95, 75, 85, 92, 90, 95, 75, 85, 92,
                   90, 95, 75, 85, 92]
}

sample_df = pd.DataFrame(data)

st.subheader("📂 Upload Student Data")
uploaded_file = st.file_uploader(
    "Upload a CSV file (optional)",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        required = {"Student", "Subject", "Marks", "Attendance"}

        if not required.issubset(df.columns):
            st.error(
                "CSV must contain: Student, Subject, Marks, Attendance"
            )
            df = sample_df.copy()
        else:
            df["Marks"] = pd.to_numeric(df["Marks"], errors="coerce")
            df["Attendance"] = pd.to_numeric(
                df["Attendance"], errors="coerce"
            )
            df = df.dropna(
                subset=["Student", "Subject", "Marks", "Attendance"]
            )
    except Exception:
        st.error("Unable to read this CSV. Please check your file.")
        df = sample_df.copy()
else:
    df = sample_df.copy()

if df.empty:
    st.warning("No valid student records found.")
    st.stop()

st.subheader("📌 Performance Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Records", len(df))
c2.metric("Average Marks", f"{df['Marks'].mean():.1f}")
c3.metric("Highest Marks", f"{df['Marks'].max():.1f}")
c4.metric("Avg Attendance", f"{df['Attendance'].mean():.1f}%")

st.divider()

subjects = ["All Subjects"] + sorted(
    df["Subject"].astype(str).unique().tolist()
)

selected_subject = st.selectbox("Choose Subject", subjects)

filtered = df.copy()

if selected_subject != "All Subjects":
    filtered = filtered[
        filtered["Subject"].astype(str) == selected_subject
    ]

left, right = st.columns(2)

with left:
    st.subheader("📈 Average Marks by Subject")
    avg_marks = (
        filtered.groupby("Subject", as_index=False)["Marks"]
        .mean()
    )
    fig = px.bar(
        avg_marks,
        x="Subject",
        y="Marks",
        color="Subject",
        title="Subject-wise Average Marks"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("🎯 Grade Distribution")
    grades = pd.cut(
        filtered["Marks"],
        bins=[-float("inf"), 40, 60, 80, float("inf")],
        labels=["Needs Improvement", "Average", "Good", "Excellent"]
    )
    grade_counts = grades.value_counts().reset_index()
    grade_counts.columns = ["Grade", "Students"]
    fig2 = px.pie(
        grade_counts,
        names="Grade",
        values="Students",
        title="Performance Categories"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("💡 Data Insights")

best = (
    filtered.groupby("Subject")["Marks"]
    .mean()
    .idxmax()
)

st.success(
    f"Highest average marks are in {best}."
)

st.write(
    f"Average attendance across displayed records: "
    f"{filtered['Attendance'].mean():.1f}%"
)

st.subheader("📋 Student Records")
st.dataframe(filtered, use_container_width=True)

st.caption(
    "Demo dashboard built with Python, Pandas, Plotly and Streamlit."
)
