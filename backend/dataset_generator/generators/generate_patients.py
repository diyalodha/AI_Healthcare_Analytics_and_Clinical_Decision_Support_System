"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_patients.py

Purpose :
Generate ground-truth based synthetic patient dataset.

Output:
datasets/synthetic/patients.csv

Author : Diya Lodha & Team
===========================================================
"""


import os
import sys
import random
import pandas as pd

from datetime import datetime, timedelta



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
    save_dataframe,
    show_progress
)



# ==========================================================
# Reference Paths
# ==========================================================


REFERENCE_DIR = os.path.join(
    PARENT_DIR,
    "reference"
)



# ==========================================================
# Load Reference Data
# ==========================================================


male_names = pd.read_csv(
    os.path.join(
        REFERENCE_DIR,
        "indian_first_names_male.csv"
    )
)


female_names = pd.read_csv(
    os.path.join(
        REFERENCE_DIR,
        "indian_first_names_female.csv"
    )
)


last_names = pd.read_csv(
    os.path.join(
        REFERENCE_DIR,
        "indian_last_names.csv"
    )
)


cities = pd.read_csv(
    os.path.join(
        REFERENCE_DIR,
        "indian_cities.csv"
    )
)


occupations = pd.read_csv(
    os.path.join(
        REFERENCE_DIR,
        "occupations.csv"
    )
)



# ==========================================================
# Helper Functions
# ==========================================================


def generate_dob(age):

    today = datetime.today()

    birth_year = today.year - age


    birth_date = datetime(
        birth_year,
        random.randint(1,12),
        random.randint(1,28)
    )


    return birth_date.date()



def calculate_bmi(
        height,
        weight
):

    return round(
        weight /
        ((height/100)**2),
        2
    )



# ==========================================================
# Generate Patients
# ==========================================================


def generate_patients():


    show_progress(
        "Generating Patient Dataset"
    )


    records = []



    for i in range(
        config.NUM_PATIENTS
    ):


        gender = random.choice(
            [
                "Male",
                "Female"
            ]
        )


        if gender == "Male":

            first_name = random.choice(
                male_names["First_Name"].tolist()
            )

        else:

            first_name = random.choice(
                female_names["First_Name"].tolist()
            )


        last_name = random.choice(
            last_names["Last_Name"].tolist()
        )


        age = random.randint(
            1,
            90
        )


        height = random.randint(
            140,
            190
        )


        weight = random.randint(
            35,
            120
        )


        record = {


            "Patient_ID":
                generate_uuid(),


            "First_Name":
                first_name,


            "Last_Name":
                last_name,


            "Date_of_Birth":
                generate_dob(age),


            "Age":
                age,


            "Gender":
                gender,


            "Blood_Group":
                random.choice(
                    [
                    "A+",
                    "A-",
                    "B+",
                    "B-",
                    "AB+",
                    "AB-",
                    "O+",
                    "O-"
                    ]
                ),


            "Phone_Number":
                "9"
                +
                str(
                    random.randint(
                        100000000,
                        999999999
                    )
                ),


            "City":
                random.choice(
                    cities["City"].tolist()
                ),


            "Occupation":
                random.choice(
                    occupations["Occupation"].tolist()
                ),


            "Height_cm":
                height,


            "Weight_kg":
                weight,


            "BMI":
                calculate_bmi(
                    height,
                    weight
                ),


            "Smoking_Status":
                random.choice(
                    [
                    "Never",
                    "Former",
                    "Current"
                    ]
                ),


            "Alcohol_Consumption":
                random.choice(
                    [
                    "None",
                    "Occasional",
                    "Regular"
                    ]
                ),


            "Family_History":
                random.choice(
                    [
                    "Yes",
                    "No"
                    ]
                ),


            "Emergency_Contact_Name":
                first_name
                +
                " "
                +
                last_name,


            "Status":
                "Active"

        }


        records.append(
            record
        )



        if (i+1) % 10000 == 0:

            print(
                f"{i+1} patients generated"
            )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "patients.csv"
    )


    print(
        f"Generated {len(dataframe)} patients"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_patients()