"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_reference_patient_data.py

Purpose :
Create patient supporting reference data.

Creates:
- Indian Male Names
- Indian Female Names
- Indian Last Names
- Indian Cities
- Occupations

Output:
reference/*.csv

Author : Diya Lodha & Team
===========================================================
"""

import os
import sys
import pandas as pd


# ==========================================================
# Add Parent Directory
# ==========================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PARENT_DIR = os.path.dirname(
    CURRENT_DIR
)

if PARENT_DIR not in sys.path:

    sys.path.insert(
        0,
        PARENT_DIR
    )


import config

from utils import save_reference_dataframe


# ==========================================================
# Male Names
# ==========================================================

MALE_NAMES = [

    "Rahul",
    "Amit",
    "Arjun",
    "Vikram",
    "Rohan",
    "Aditya",
    "Karan",
    "Raj",
    "Ankit",
    "Manish",
    "Akshay",
    "Varun",
    "Siddharth",
    "Harsh",
    "Yash"

]


# ==========================================================
# Female Names
# ==========================================================

FEMALE_NAMES = [

    "Priya",
    "Ananya",
    "Neha",
    "Pooja",
    "Kavya",
    "Riya",
    "Diya",
    "Isha",
    "Meera",
    "Sneha",
    "Aarti",
    "Nisha",
    "Shreya",
    "Komal",
    "Tanvi"

]


# ==========================================================
# Last Names
# ==========================================================

LAST_NAMES = [

    "Sharma",
    "Patel",
    "Jadhav",
    "Lodha",
    "Deshmukh",
    "Gupta",
    "Verma",
    "Joshi",
    "Kulkarni",
    "Singh",
    "Mehta",
    "Reddy",
    "Shah",
    "More",
    "Pawar"

]


# ==========================================================
# Indian Cities
# ==========================================================

CITIES = [

    "Pune",
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Ahmedabad",
    "Nashik",
    "Nagpur",
    "Solapur"

]


# ==========================================================
# Occupations
# ==========================================================

OCCUPATIONS = [

    "Engineer",
    "Teacher",
    "Doctor",
    "Business Owner",
    "Student",
    "Farmer",
    "Software Developer",
    "Government Employee",
    "Bank Employee",
    "Driver",
    "Homemaker",
    "Retired"

]


# ==========================================================
# Generate Patient Reference Data
# ==========================================================

def generate_reference_patient_data():

    save_reference_dataframe(

        pd.DataFrame(
            {
                "First_Name": MALE_NAMES
            }
        ),

        "indian_first_names_male.csv"

    )

    save_reference_dataframe(

        pd.DataFrame(
            {
                "First_Name": FEMALE_NAMES
            }
        ),

        "indian_first_names_female.csv"

    )

    save_reference_dataframe(

        pd.DataFrame(
            {
                "Last_Name": LAST_NAMES
            }
        ),

        "indian_last_names.csv"

    )

    save_reference_dataframe(

        pd.DataFrame(
            {
                "City": CITIES
            }
        ),

        "indian_cities.csv"

    )

    save_reference_dataframe(

        pd.DataFrame(
            {
                "Occupation": OCCUPATIONS
            }
        ),

        "occupations.csv"

    )

    print()

    print("=======================================")

    print("Patient reference data created successfully.")

    print("Files created:")

    print("- indian_first_names_male.csv")
    print("- indian_first_names_female.csv")
    print("- indian_last_names.csv")
    print("- indian_cities.csv")
    print("- occupations.csv")

    print("Stored in : reference/")

    print("=======================================")


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    generate_reference_patient_data()