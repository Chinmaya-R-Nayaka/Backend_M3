
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

    st.header("Add Immunization Record")

    # Fetch patients
    patient_list = list(patients_col.find())

    if len(patient_list) == 0:
        st.warning("No patients found. Please add a patient first.")
        st.stop()

    # Create name → id mapping
    patient_dict = {p["name"]: p["_id"] for p in patient_list}

    selected_name = st.selectbox("Select Patient", list(patient_dict.keys()))
    selected_patient = patient_dict[selected_name]

    vaccine_name = st.text_input("Vaccine Name")
    scheduled_date = st.date_input("Scheduled Date")

    if st.button("Save Immunization"):

        if vaccine_name.strip() == "":
            st.error("Please enter vaccine name")
            st.stop()

        delayed = check_immunization_delay(scheduled_date)

        immunization_col.insert_one({
            "patient_id": selected_patient,
            "patient_name": selected_name,
            "vaccine_name": vaccine_name,
            "scheduled_date": scheduled_date.strftime("%Y-%m-%d"),
            "delayed": delayed,
            "created_at": datetime.now()
        })

        # Generate alert if delayed
        if delayed:
            alert_col.insert_one({
                "patient_id": selected_patient,
                "type": "Immunization Delay",
                "status": "Active",
                "created_at": datetime.now()
            })

        st.success("Immunization record added successfully")


# ADD MILESTONE
elif menu == "Add Milestone":

    st.header("Add Developmental Milestone")

    patient_list = list(patients_col.find())

    if len(patient_list) == 0:
        st.warning("No patients found. Please add a patient first.")
        st.stop()

    # name -> id mapping
    patient_dict = {p["name"]: str(p["_id"]) for p in patient_list}

    selected_name = st.selectbox("Select Patient", list(patient_dict.keys()))

    # geting ObjectId
    selected_patient = ObjectId(patient_dict[selected_name])

    milestone_name = st.text_input("Milestone Name")
    expected_age = st.number_input("Expected Age (Months)", min_value=0)
    achieved_age = st.number_input("Achieved Age (Months)", min_value=0)

    if st.button("Save Milestone"):

        delayed = check_milestone_delay(expected_age, achieved_age)

        milestone_col.insert_one({
            "patient_id": selected_patient,
            "patient_name": selected_name,
            "milestone_name": milestone_name,
            "expected_age": expected_age,
            "achieved_age": achieved_age,
            "delayed": delayed,
            "created_at": datetime.now()
        })

        if delayed:
            alert_col.insert_one({
                "patient_id": selected_patient,
                "type": "Milestone Delay",
                "status": "Active",
                "created_at": datetime.now()
            })

        st.success("Milestone saved successfully")

# VIEW PATIENTS
# VIEW PATIENTS
elif menu == "View Patients":

    st.header("All Pediatric Patients")

    patients = list(patients_col.find())

    if patients:
        for patient in patients:
            patient.pop("_id")   # remove MongoDB object id

        st.dataframe(patients)

    else:
        st.warning("No Patients found.")


# VIEW ALERTS
elif menu == "View Alerts":

    st.header("Growth Alerts")

    alerts = list(growth_col.find({"alert": {"$ne": "Normal"}}))

    if alerts:
        for record in alerts:
            record.pop("_id")

        st.dataframe(alerts)

    else:
        st.success("No alerts found. All children are normal.")