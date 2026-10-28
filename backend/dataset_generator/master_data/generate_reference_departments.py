"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_reference_departments.py

Purpose :
Generate reference department dataset.

Output:
reference_departments.csv

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

from utils import (
    generate_uuid,
    show_progress
)

# ==========================================================
# Departments
# ==========================================================

DEPARTMENTS = [

    (
        "Cardiology",
        "CARD",
        "Clinical"
    ),

    (
        "Neurology",
        "NEUR",
        "Clinical"
    ),

    (
        "Orthopedics",
        "ORTH",
        "Clinical"
    ),

    (
        "Pediatrics",
        "PED",
        "Clinical"
    ),

    (
        "Gynecology",
        "GYN",
        "Clinical"
    ),

    (
        "Oncology",
        "ONC",
        "Clinical"
    ),

    (
        "Radiology",
        "RAD",
        "Diagnostic"
    ),

    (
        "Pathology",
        "PATH",
        "Diagnostic"
    ),

    (
        "Emergency",
        "EMR",
        "Emergency"
    ),

    (
        "ICU",
        "ICU",
        "Critical Care"
    ),

    (
        "General Medicine",
        "GEN",
        "Clinical"
    ),

    (
        "Pulmonology",
        "PUL",
        "Clinical"
    ),

    (
        "Nephrology",
        "NEPH",
        "Clinical"
    ),

    (
        "Dermatology",
        "DERM",
        "Clinical"
    ),

    (
        "Psychiatry",
        "PSY",
        "Clinical"
    ),

    (
        "ENT",
        "ENT",
        "Clinical"
    ),

    (
        "Ophthalmology",
        "OPH",
        "Clinical"
    ),

    (
        "Urology",
        "URO",
        "Clinical"
    ),

    (
        "Endocrinology",
        "ENDO",
        "Clinical"
    ),

    (
        "Gastroenterology",
        "GAST",
        "Clinical"
    ),

    (
        "Anesthesiology",
        "ANES",
        "Support"
    ),

    (
        "Physiotherapy",
        "PHYS",
        "Support"
    ),

    (
        "Pharmacy",
        "PHAR",
        "Support"
    ),

    (
        "Blood Bank",
        "BB",
        "Support"
    ),

    (
        "Administration",
        "ADMIN",
        "Administrative"
    )

]


# ==========================================================
# Generate Reference Departments
# ==========================================================

def generate_reference_departments():

    show_progress(
        "Generating Reference Departments"
    )

    records = []

    floor = 1

    for department in DEPARTMENTS:

        record = {

            "Department_ID":
                generate_uuid(),

            "Department_Name":
                department[0],

            "Department_Code":
                department[1],

            "Department_Type":
                department[2],

            "Location":
                f"Block {chr(65 + (floor % 5))}",

            "Floor_Number":
                floor,

            "Contact_Number":
                f"+91-20-4{floor:03d}5678",

            "Email":
                department[1].lower()
                + "@hospital.org"

        }

        records.append(
            record
        )

        floor += 1

    dataframe = pd.DataFrame(
        records
    )

    path = os.path.join(
        config.REFERENCE_DIR,
        "reference_departments.csv"
    )

    dataframe.to_csv(
        path,
        index=False
    )

    print(
        "Created reference_departments.csv"
    )

    print(
        f"Generated {len(dataframe)} reference departments."
    )


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    generate_reference_departments()