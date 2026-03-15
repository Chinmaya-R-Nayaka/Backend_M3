
import streamlit as st
from datetime import datetime
from db import get_database
from services import (
    calculate_age_in_months, calculate_growth_percentile, 
    check_milestone_delay, check_immunization_delay
)

# Database Setup
db = get_database()

patients_col = db["patients"]
growth_col = db["growth"]
immunization_col = db["immunization"]
milestone_col = db["milestones"]
alert_col = db["alerts"]

# UI Layout
st.set_page_config(page_title="M3 Pediatric System", layout="wide")

st.title("M3 - Pediatric Clinical Data System")
st.markdown("---")

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Add Patient",
        "Add Growth Record",
        "Add Immunization",
        "Add Milestone",
        "View Patients",
        "View Alerts"
    ]
)


# ADD PATIENT
if menu == "Add Patient":

    st.header("Add New Pediatric Patient")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Child Name")
        gender = st.selectbox("Gender", ["Male", "Female"])

    with col2:
        dob = st.date_input("Date of Birth")

    if st.button("Save Patient"):
        age_months = calculate_age_in_months(dob)

        patients_col.insert_one({
            "name": name,
            "dob": dob.strftime("%Y-%m-%d"),
            "gender": gender,
            "age_months": age_months,
            "created_at": datetime.now()
        })

        st.success("Patient saved successfully.")


# ADD GROWTH
elif menu == "Add Growth Record":

    st.header("Add Growth Record")

    col1, col2 = st.columns(2)

    with col1:
        patient_name = st.text_input("Patient Name")
        height = st.number_input("Height (cm)", min_value=0.0)
        weight = st.number_input("Weight (kg)", min_value=0.0)

    with col2:
        head_circumference = st.number_input("Head Circumference (cm)", min_value=0.0)
        measurement_date = st.date_input("Measurement Date")

    if st.button("Save Growth Record"):

        # Calculate BMI
        if height > 0:
            bmi = weight / ((height / 100) ** 2)
        else:
            bmi = 0

        if bmi < 18:
            alert = "Underweight"
        elif bmi > 25:
            alert = "Overweight"
        else:
            alert = "Normal"

        growth_col.insert_one({
            "patient_name": patient_name,
            "height": height,
            "weight": weight,
            "head_circumference": head_circumference,
            "bmi": round(bmi, 2),
            "alert": alert,
            "measurement_date": measurement_date.strftime("%Y-%m-%d"),
            "created_at": datetime.now()
        })
    
        st.success("Growth record added successfully.")



# ADD IMMUNIZATION
elif menu == "Add Immunization":

        # Enosh Write ur Logic here

        st.success("Immunization saved successfully.")



# ADD MILESTONE
elif menu == "Add Milestone":

        # Enosh Write ur Logic here
    
        st.success("Milestone saved successfully.")


# VIEW PATIENTS
elif menu == "View Patients":

    st.header("All Pediatric Patients")
    patients=list(patients_col.find())
    if patients:
        for patient in patients:
            patient.pop("_id")
        st.dataframe(patients)
    else:
        st.warning("No Patients found.")


# VIEW ALERTS
elif menu == "View Alerts":

    st.header("Growth Alerts")

    alerts=list(growth_col.find({"alert":{"$ne":"Normal"}}))
    if alerts:
        for record in alerts:
            record.pop("_id")
        st.dataframe(alerts)
    else:
        st.success("No alerts found.All children are normal.")
     
