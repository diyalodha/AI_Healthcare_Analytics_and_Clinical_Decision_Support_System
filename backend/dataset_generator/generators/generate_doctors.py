"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 02_generate_doctors.py

Purpose :
Generate ground-truth based synthetic doctors dataset.

Input:
datasets/synthetic/departments.csv

Output:
datasets/synthetic/doctors.csv

Author : Diya Lodha & Team
===========================================================
"""


import os
import sys
import random
import pandas as pd

from datetime import date

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

import config

from utils import (
    generate_uuid,
    generate_date,
    save_dataframe,
    show_progress,
    fake
)


# ==========================================================
# Department Based Specialization Mapping
# ==========================================================


SPECIALIZATION_MAP = {

    "Emergency Medicine":
        [
            "Emergency Physician",
            "Trauma Specialist"
        ],


    "Cardiology":
        [
            "Cardiologist",
            "Interventional Cardiologist"
        ],


    "Neurology":
        [
            "Neurologist",
            "Neuro Physician"
        ],


    "Orthopedics":
        [
            "Orthopedic Surgeon",
            "Joint Replacement Specialist"
        ],


    "Oncology":
        [
            "Medical Oncologist",
            "Cancer Specialist"
        ],


    "General Medicine":
        [
            "General Physician",
            "Internal Medicine Specialist"
        ],


    "Pediatrics":
        [
            "Pediatrician"
        ],


    "Gynecology":
        [
            "Gynecologist",
            "Obstetrician"
        ],


    "Radiology":
        [
            "Radiologist"
        ],


    "Pathology Laboratory":
        [
            "Pathologist"
        ],


    "Pharmacy":
        [
            "Clinical Pharmacist"
        ],


    "ICU":
        [
            "Critical Care Specialist",
            "Intensivist"
        ]

}



# ==========================================================
# Qualifications
# ==========================================================


QUALIFICATIONS = [

    "MBBS",
    "MBBS, MD",
    "MBBS, MS",
    "MBBS, DNB",
    "MBBS, MD, Fellowship"

]



# ==========================================================
# Generate Doctors
# ==========================================================


def generate_doctors():


    show_progress(
        "Generating Doctors Dataset"
    )


    # Read departments

    department_file = (
        config.SYNTHETIC_DIR
        +
        "/departments.csv"
    )


    departments = pd.read_csv(
        department_file
    )


    doctors = []



    for i in range(
        config.NUM_DOCTORS
    ):


        department = (
            departments
            .sample(1)
            .iloc[0]
        )


        department_name = (
            department["Department_Name"]
        )



        specialization = random.choice(

            SPECIALIZATION_MAP.get(

                department_name,

                [
                    "Medical Specialist"
                ]

            )

        )



        experience = random.choices(

            range(1,36),

            weights=[

                10 if x < 5
                else
                30 if x < 15
                else
                20

                for x in range(1,36)

            ]

        )[0]



        joining_year = (
            date.today().year
            -
            experience
        )



        doctor = {


            "Doctor_ID":
                generate_uuid(),



            "First_Name":
                fake.first_name(),



            "Middle_Name":
                fake.first_name(),



            "Last_Name":
                fake.last_name(),



            "Gender":
                random.choice(
                    [
                        "Male",
                        "Female"
                    ]
                ),



            "Date_of_Birth":
                generate_date(
                    1960,
                    1998
                ),



            "Medical_License_No":
                "MED"
                +
                str(
                    random.randint(
                        100000,
                        999999
                    )
                ),



            "Qualification":
                random.choice(
                    QUALIFICATIONS
                ),



            "Specialization":
                specialization,



            "Years_of_Experience":
                experience,



            "Department_ID":
                department["Department_ID"],



            "Phone":
                fake.phone_number()
                [:15],



            "Email":
                fake.email(),



            "Consultation_Fee":
                random.choice(
                    [
                        300,
                        500,
                        800,
                        1000,
                        1500
                    ]
                ),



            "Joining_Date":
                generate_date(
                    joining_year-1,
                    joining_year
                ),



            "Shift":
                random.choice(
                    [
                        "Morning",
                        "Evening",
                        "Night",
                        "Rotational"
                    ]
                ),



            "Employment_Type":
                random.choice(
                    [
                        "Full-Time",
                        "Part-Time",
                        "Visiting"
                    ]
                ),



            "Status":
                "Active",



            "Is_Active":
                True,



            "Created_By":
                "Synthetic Generator",



            "Updated_By":
                "Synthetic Generator"



        }


        doctors.append(
            doctor
        )



    df = pd.DataFrame(
        doctors
    )



    save_dataframe(
        df,
        "doctors.csv"
    )



    print(
        f"Generated {len(df)} doctors"
    )



# ==========================================================
# Execute
# ==========================================================


if __name__ == "__main__":

    generate_doctors()