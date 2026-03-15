
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


    st.header("Add Immunization")

    patients = list(patients_col.find())

    if not patients:
        st.warning("No patients found. Please add patient first.")

    else:
        patient_dict = {p["name"]: p for p in patients}
        selected_patient = st.selectbox("Select Patient", list(patient_dict.keys()))

        vaccine = st.text_input("Vaccine Name")
        given_date = st.date_input("Date Given")

        if st.button("Save Immunization"):

            patient = patient_dict[selected_patient]
            patient_id = patient["_id"]

            dob = datetime.strptime(patient["dob"], "%Y-%m-%d").date()
            age_months = (given_date - dob).days / 30.44

            delay = check_immunization_delay(vaccine, given_date, patient["dob"])

            immunization_col.insert_one({
                "patient_id": patient_id,
                "patient_name": selected_patient,
                "vaccine": vaccine,
                "date_given": given_date.strftime("%Y-%m-%d"),
                "age_months": round(age_months,1),
                "delay": delay,
                "created_at": datetime.now()
            })

            if delay:
                alert_col.insert_one({
                    "patient_name": selected_patient,
                    "type": "Immunization Delay",
                    "message": f"{vaccine} vaccine delayed",
                    "created_at": datetime.now()
                })

                st.warning("Immunization delay detected")

            

        st.success("Immunization saved successfully.")

# ADD MILESTONE
elif menu == "Add Milestone":

       

    st.header("Add Development Milestone")

    patients = list(patients_col.find())

    if not patients:
        st.warning("No patients found. Please add patient first.")

    else:
        patient_dict = {p["name"]: p for p in patients}
        selected_patient = st.selectbox("Select Patient", list(patient_dict.keys()))

        milestone = st.text_input("Milestone Name")
        achieved_age = st.number_input("Age Achieved (months)", min_value=0)

        if st.button("Save Milestone"):

            patient = patient_dict[selected_patient]
            patient_id = patient["_id"]

            delay = check_milestone_delay(milestone, achieved_age)

            milestone_col.insert_one({
                "patient_id": patient_id,
                "patient_name": selected_patient,
                "milestone": milestone,
                "achieved_age_months": achieved_age,
                "delay": delay,
                "created_at": datetime.now()
            })

            if delay:
                alert_col.insert_one({
                    "patient_name": selected_patient,
                    "type": "Milestone Delay",
                    "message": f"{milestone} milestone delayed",
                    "created_at": datetime.now()
                })

                st.warning("Milestone delay detected")

        
    
        st.success("Milestone saved successfully.")



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