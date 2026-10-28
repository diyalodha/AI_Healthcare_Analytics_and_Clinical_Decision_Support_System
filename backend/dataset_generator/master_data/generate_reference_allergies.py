"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_reference_allergies.py

Purpose :
Generate reference dataset for common allergies.

Output :
reference_allergies.csv

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



# ==========================================================
# Allergy Reference Data
# ==========================================================

ALLERGIES = [

    {
        "Allergy_Code":"ALG001",
        "Allergy_Name":"Penicillin",
        "Category":"Medication",
        "Severity":"High"
    },

    {
        "Allergy_Code":"ALG002",
        "Allergy_Name":"Amoxicillin",
        "Category":"Medication",
        "Severity":"High"
    },

    {
        "Allergy_Code":"ALG003",
        "Allergy_Name":"Aspirin",
        "Category":"Medication",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG004",
        "Allergy_Name":"Ibuprofen",
        "Category":"Medication",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG005",
        "Allergy_Name":"Sulfa Drugs",
        "Category":"Medication",
        "Severity":"High"
    },

    {
        "Allergy_Code":"ALG006",
        "Allergy_Name":"Insulin",
        "Category":"Medication",
        "Severity":"Low"
    },

    {
        "Allergy_Code":"ALG007",
        "Allergy_Name":"Latex",
        "Category":"Material",
        "Severity":"High"
    },

    {
        "Allergy_Code":"ALG008",
        "Allergy_Name":"Nickel",
        "Category":"Material",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG009",
        "Allergy_Name":"Dust Mites",
        "Category":"Environmental",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG010",
        "Allergy_Name":"Pollen",
        "Category":"Environmental",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG011",
        "Allergy_Name":"Grass",
        "Category":"Environmental",
        "Severity":"Low"
    },

    {
        "Allergy_Code":"ALG012",
        "Allergy_Name":"Mold",
        "Category":"Environmental",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG013",
        "Allergy_Name":"Animal Dander",
        "Category":"Environmental",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG014",
        "Allergy_Name":"Bee Sting",
        "Category":"Insect",
        "Severity":"High"
    },

    {
        "Allergy_Code":"ALG015",
        "Allergy_Name":"Wasp Sting",
        "Category":"Insect",
        "Severity":"High"
    },

    {
        "Allergy_Code":"ALG016",
        "Allergy_Name":"Mosquito Bite",
        "Category":"Insect",
        "Severity":"Low"
    },

    {
        "Allergy_Code":"ALG017",
        "Allergy_Name":"Peanuts",
        "Category":"Food",
        "Severity":"High"
    },

    {
        "Allergy_Code":"ALG018",
        "Allergy_Name":"Tree Nuts",
        "Category":"Food",
        "Severity":"High"
    },

    {
        "Allergy_Code":"ALG019",
        "Allergy_Name":"Milk",
        "Category":"Food",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG020",
        "Allergy_Name":"Egg",
        "Category":"Food",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG021",
        "Allergy_Name":"Soy",
        "Category":"Food",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG022",
        "Allergy_Name":"Wheat",
        "Category":"Food",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG023",
        "Allergy_Name":"Shellfish",
        "Category":"Food",
        "Severity":"High"
    },

    {
        "Allergy_Code":"ALG024",
        "Allergy_Name":"Fish",
        "Category":"Food",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG025",
        "Allergy_Name":"Sesame",
        "Category":"Food",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG026",
        "Allergy_Name":"Chocolate",
        "Category":"Food",
        "Severity":"Low"
    },

    {
        "Allergy_Code":"ALG027",
        "Allergy_Name":"Strawberry",
        "Category":"Food",
        "Severity":"Low"
    },

    {
        "Allergy_Code":"ALG028",
        "Allergy_Name":"Banana",
        "Category":"Food",
        "Severity":"Low"
    },

    {
        "Allergy_Code":"ALG029",
        "Allergy_Name":"Tomato",
        "Category":"Food",
        "Severity":"Low"
    },

    {
        "Allergy_Code":"ALG030",
        "Allergy_Name":"Seafood",
        "Category":"Food",
        "Severity":"High"
    },

    {
        "Allergy_Code":"ALG031",
        "Allergy_Name":"Contrast Dye",
        "Category":"Medication",
        "Severity":"High"
    },

    {
        "Allergy_Code":"ALG032",
        "Allergy_Name":"Iodine",
        "Category":"Chemical",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG033",
        "Allergy_Name":"Alcohol",
        "Category":"Chemical",
        "Severity":"Low"
    },

    {
        "Allergy_Code":"ALG034",
        "Allergy_Name":"Perfume",
        "Category":"Chemical",
        "Severity":"Low"
    },

    {
        "Allergy_Code":"ALG035",
        "Allergy_Name":"Cleaning Chemicals",
        "Category":"Chemical",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG036",
        "Allergy_Name":"Sunlight",
        "Category":"Environmental",
        "Severity":"Low"
    },

    {
        "Allergy_Code":"ALG037",
        "Allergy_Name":"Cold Temperature",
        "Category":"Environmental",
        "Severity":"Low"
    },

    {
        "Allergy_Code":"ALG038",
        "Allergy_Name":"Heat",
        "Category":"Environmental",
        "Severity":"Low"
    },

    {
        "Allergy_Code":"ALG039",
        "Allergy_Name":"Smoke",
        "Category":"Environmental",
        "Severity":"Medium"
    },

    {
        "Allergy_Code":"ALG040",
        "Allergy_Name":"Pet Hair",
        "Category":"Environmental",
        "Severity":"Medium"
    }

]


# ==========================================================
# Generate Dataset
# ==========================================================

def generate_reference_allergies():

    dataframe = pd.DataFrame(
        ALLERGIES
    )

    path = os.path.join(
        config.REFERENCE_DIR,
        "reference_allergies.csv"
    )

    dataframe.to_csv(
        path,
        index=False
    )

    print(
        "Created reference_allergies.csv"
    )

    print(
        f"Generated {len(dataframe)} allergy references."
    )


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    generate_reference_allergies()