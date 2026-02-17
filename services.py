
from datetime import datetime


def calculate_age_in_months(dob):
    """
    Calculates age in months from date of birth.
    """
    days_difference = (datetime.now() - datetime.combine(dob, datetime.min.time())).days
    return days_difference // 30


def calculate_growth_percentile(weight, height):
    """
    Simplified percentile calculation logic.
    Replace with WHO logic if needed.
    """
    if weight < 5:
        return 10
    elif weight > 20:
        return 95
    else:
        return 50


def check_milestone_delay(expected_age, achieved_age):
    """
    Returns True if milestone is delayed.
    """
    return achieved_age > expected_age


def check_immunization_delay(scheduled_date):
    """
    Returns True if vaccine date has passed.
    """
    return datetime.now().date() > scheduled_date
