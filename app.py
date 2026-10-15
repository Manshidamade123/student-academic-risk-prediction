
import streamlit as st
import pandas as pd
import joblib

# Load the trained machine learning model
model = joblib.load("student_risk_model.pkl")

st.set_page_config(
    page_title="Student Academic Risk Predictor",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Academic Risk Prediction System")

st.write(
    "An experimental machine learning application that classifies "
    "student records using academic and personal characteristics."
)

st.info(
    "Educational project only. Predictions are experimental and "
    "should not be used to make high-stakes decisions about students."
)

st.sidebar.title("About This Project")
st.sidebar.write("""
**Model:** Logistic Regression

**Dataset:** UCI Student Performance

**Training records:** 316

**Testing records:** 79

**Evaluation:** ROC-AUC 0.727

This application demonstrates a machine learning workflow.
""")

st.header("Enter Student Information")

with st.form("student_information"):

    col1, col2 = st.columns(2)

    with col1:
        school = st.selectbox("School", ["GP", "MS"])
        sex = st.selectbox("Sex", ["F", "M"])
        age = st.slider("Age", 15, 22, 17)
        address = st.selectbox("Home area", ["U", "R"])
        famsize = st.selectbox("Family size", ["GT3", "LE3"])
        Pstatus = st.selectbox("Parents' cohabitation status", ["T", "A"])

        Medu = st.selectbox("Mother's education level", [0, 1, 2, 3, 4])
        Fedu = st.selectbox("Father's education level", [0, 1, 2, 3, 4])

        Mjob = st.selectbox(
            "Mother's job",
            ["teacher", "health", "services", "at_home", "other"]
        )

        Fjob = st.selectbox(
            "Father's job",
            ["teacher", "health", "services", "at_home", "other"]
        )

        reason = st.selectbox(
            "Reason for choosing school",
            ["course", "home", "reputation", "other"]
        )

        guardian = st.selectbox(
            "Main guardian",
            ["mother", "father", "other"]
        )

        traveltime = st.selectbox("Travel time to school", [1, 2, 3, 4])
        studytime = st.selectbox("Weekly study time category", [1, 2, 3, 4])
        failures = st.selectbox("Previous class failures", [0, 1, 2, 3])

    with col2:
        schoolsup = st.selectbox("Extra educational support", ["yes", "no"])
        famsup = st.selectbox("Family educational support", ["yes", "no"])
        paid = st.selectbox("Extra paid classes", ["yes", "no"])
        activities = st.selectbox("Extracurricular activities", ["yes", "no"])
        nursery = st.selectbox("Attended nursery school", ["yes", "no"])
        higher = st.selectbox("Wants higher education", ["yes", "no"])
        internet = st.selectbox("Internet access at home", ["yes", "no"])
        romantic = st.selectbox("In a romantic relationship", ["yes", "no"])

        famrel = st.slider("Family relationship quality", 1, 5, 4)
        freetime = st.slider("Free time", 1, 5, 3)
        goout = st.slider("Going out with friends", 1, 5, 3)
        Dalc = st.slider("Workday alcohol consumption scale", 1, 5, 1)
        Walc = st.slider("Weekend alcohol consumption scale", 1, 5, 1)
        health = st.slider("Self-reported health", 1, 5, 3)
        absences = st.slider("School absences", 0, 30, 0)

    submitted = st.form_submit_button("Predict Academic Risk")

if submitted:

    student = pd.DataFrame([{
        "school": school,
        "sex": sex,
        "age": age,
        "address": address,
        "famsize": famsize,
        "Pstatus": Pstatus,
        "Medu": Medu,
        "Fedu": Fedu,
        "Mjob": Mjob,
        "Fjob": Fjob,
        "reason": reason,
        "guardian": guardian,
        "traveltime": traveltime,
        "studytime": studytime,
        "failures": failures,
        "schoolsup": schoolsup,
        "famsup": famsup,
        "paid": paid,
        "activities": activities,
        "nursery": nursery,
        "higher": higher,
        "internet": internet,
        "romantic": romantic,
        "famrel": famrel,
        "freetime": freetime,
        "goout": goout,
        "Dalc": Dalc,
        "Walc": Walc,
        "health": health,
        "absences": absences
    }])

    expected_features = model.named_steps["preprocessor"].feature_names_in_
    student = student.reindex(columns=expected_features)

    prediction = int(model.predict(student)[0])
    risk_score = float(model.predict_proba(student)[0][1])

    st.divider()
    st.subheader("Prediction Result")

    if prediction == 1:
        st.warning("The model flags this record as potentially at academic risk.")
    else:
        st.success("The model does not flag this record as academically at risk.")

    st.metric("Model-estimated risk score", f"{risk_score:.1%}")

    st.caption(
        "The risk score is an experimental model output, not a calibrated "
        "probability of future academic failure. The model uses a grade-based "
        "risk definition and has not been validated for real-world decisions."
    )
