"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_reference_vaccines.py

Purpose :
Generate reference dataset for vaccines.

Output :
reference_vaccines.csv

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
# Vaccine Reference Data
# ==========================================================

VACCINES = [

    {
        "Vaccine_Code":"VAC001",
        "Vaccine_Name":"BCG",
        "Disease_Prevented":"Tuberculosis",
        "Category":"Childhood",
        "Dose":"Single",
        "Route":"Intradermal"
    },

    {
        "Vaccine_Code":"VAC002",
        "Vaccine_Name":"Hepatitis B",
        "Disease_Prevented":"Hepatitis B",
        "Category":"Childhood",
        "Dose":"3 Dose",
        "Route":"Intramuscular"
    },

    {
        "Vaccine_Code":"VAC003",
        "Vaccine_Name":"OPV",
        "Disease_Prevented":"Polio",
        "Category":"Childhood",
        "Dose":"Multiple",
        "Route":"Oral"
    },

    {
        "Vaccine_Code":"VAC004",
        "Vaccine_Name":"IPV",
        "Disease_Prevented":"Polio",
        "Category":"Childhood",
        "Dose":"Multiple",
        "Route":"Intramuscular"
    },

    {
        "Vaccine_Code":"VAC005",
        "Vaccine_Name":"DPT",
        "Disease_Prevented":"Diphtheria, Pertussis, Tetanus",
        "Category":"Childhood",
        "Dose":"3 Dose",
        "Route":"Intramuscular"
    },

    {
        "Vaccine_Code":"VAC006",
        "Vaccine_Name":"MMR",
        "Disease_Prevented":"Measles, Mumps, Rubella",
        "Category":"Childhood",
        "Dose":"2 Dose",
        "Route":"Subcutaneous"
    },

    {
        "Vaccine_Code":"VAC007",
        "Vaccine_Name":"Varicella",
        "Disease_Prevented":"Chickenpox",
        "Category":"Childhood",
        "Dose":"2 Dose",
        "Route":"Subcutaneous"
    },

    {
        "Vaccine_Code":"VAC008",
        "Vaccine_Name":"Rotavirus",
        "Disease_Prevented":"Rotavirus Infection",
        "Category":"Childhood",
        "Dose":"Oral Series",
        "Route":"Oral"
    },

    {
        "Vaccine_Code":"VAC009",
        "Vaccine_Name":"Pneumococcal",
        "Disease_Prevented":"Pneumococcal Disease",
        "Category":"Childhood",
        "Dose":"Multiple",
        "Route":"Intramuscular"
    },

    {
        "Vaccine_Code":"VAC010",
        "Vaccine_Name":"Influenza",
        "Disease_Prevented":"Seasonal Flu",
        "Category":"Adult",
        "Dose":"Annual",
        "Route":"Intramuscular"
    },

    {
        "Vaccine_Code":"VAC011",
        "Vaccine_Name":"COVID-19",
        "Disease_Prevented":"COVID-19",
        "Category":"Adult",
        "Dose":"Booster",
        "Route":"Intramuscular"
    },

    {
        "Vaccine_Code":"VAC012",
        "Vaccine_Name":"HPV",
        "Disease_Prevented":"Human Papillomavirus",
        "Category":"Adolescent",
        "Dose":"2-3 Dose",
        "Route":"Intramuscular"
    },

    {
        "Vaccine_Code":"VAC013",
        "Vaccine_Name":"Typhoid",
        "Disease_Prevented":"Typhoid Fever",
        "Category":"Travel",
        "Dose":"Single",
        "Route":"Intramuscular"
    },

    {
        "Vaccine_Code":"VAC014",
        "Vaccine_Name":"Rabies",
        "Disease_Prevented":"Rabies",
        "Category":"Emergency",
        "Dose":"Multiple",
        "Route":"Intramuscular"
    },

    {
        "Vaccine_Code":"VAC015",
        "Vaccine_Name":"Japanese Encephalitis",
        "Disease_Prevented":"Japanese Encephalitis",
        "Category":"Travel",
        "Dose":"2 Dose",
        "Route":"Intramuscular"
    }

]


# ==========================================================
# Generate Dataset
# ==========================================================

def generate_reference_vaccines():

    dataframe = pd.DataFrame(
        VACCINES
    )

    save_reference_dataframe(
        dataframe,
        "reference_vaccines.csv"
    )

    print(
        "======================================="
    )

    print(
        f"Generated {len(dataframe)} vaccine references."
    )

    print(
        "Stored in : reference/"
    )

    print(
        "======================================="
    )


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    generate_reference_vaccines()