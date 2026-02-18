
from datetime import datetime


def calculate_age_in_months(dob):
    days_difference = (datetime.now() - datetime.combine(dob, datetime.min.time())).days
    return days_difference // 30


def calculate_growth_percentile(weight, height):
    if weight < 5:
        return 10
    elif weight > 20:
        return 95
    else:
        return 50


def check_milestone_delay(expected_age, achieved_age):
    return achieved_age > expected_age


def check_immunization_delay(scheduled_date):
    return datetime.now().date() > scheduled_date
