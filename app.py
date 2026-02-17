
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

        # Sujitha Write ur Logic here
    
        st.success("Growth record added successfully.")



# ADD IMMUNIZATION
elif menu == "Add Immunization":

        # Enosh Write ur Logic here

        st.success("Immunization saved successfully.")



# ADD MILESTONE
elif menu == "Add Milestone":

        # Enosh Write ur Logic here
    
        st.success("Milestone saved successfully.")


# Uncomment this part and write ur code 
# # VIEW PATIENTS
# elif menu == "View Patients":

#     # Sujitha Write ur Logic here
#     st.dataframe()


# # VIEW ALERTS
# elif menu == "View Alerts":

#     # Sujitha Write ur Logic here
