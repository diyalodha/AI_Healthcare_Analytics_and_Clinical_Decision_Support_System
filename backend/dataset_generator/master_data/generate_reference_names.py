"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_reference_names.py

Purpose :
Generate reference names dataset.

Output:
reference_names.csv

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
    save_reference_dataframe,
    show_progress
)

# ==========================================================
# Male First Names
# ==========================================================

MALE_NAMES = [

    "Aarav",
    "Vivaan",
    "Aditya",
    "Krishna",
    "Rohan",
    "Rahul",
    "Arjun",
    "Kunal",
    "Yash",
    "Aman",
    "Harsh",
    "Rajat",
    "Akash",
    "Siddharth",
    "Dhruv",
    "Nikhil",
    "Parth",
    "Ishaan",
    "Aryan",
    "Vihaan"

]


# ==========================================================
# Female First Names
# ==========================================================

FEMALE_NAMES = [

    "Diya",
    "Ananya",
    "Aadhya",
    "Kiara",
    "Myra",
    "Sara",
    "Riya",
    "Aarohi",
    "Meera",
    "Priya",
    "Neha",
    "Sneha",
    "Kavya",
    "Pooja",
    "Nisha",
    "Ishita",
    "Tanvi",
    "Khushi",
    "Palak",
    "Shreya"

]


# ==========================================================
# Last Names
# ==========================================================

LAST_NAMES = [

    "Sharma",
    "Patel",
    "Gupta",
    "Verma",
    "Singh",
    "Joshi",
    "Kulkarni",
    "Deshmukh",
    "Mehta",
    "Jain",
    "Lodha",
    "Agarwal",
    "Kapoor",
    "Bansal",
    "Pandey",
    "Naik",
    "Chaudhary",
    "Reddy",
    "Iyer",
    "Nair"

]


# ==========================================================
# Generate Reference Names
# ==========================================================

def generate_reference_names():

    show_progress(
        "Generating Reference Names"
    )

    records = []

    for name in MALE_NAMES:

        records.append(

            {

                "Name_ID":
                    generate_uuid(),

                "First_Name":
                    name,

                "Last_Name":
                    LAST_NAMES[
                        MALE_NAMES.index(name)
                    ],

                "Gender":
                    "Male",

                "Title":
                    "Mr."

            }

        )

    for name in FEMALE_NAMES:

        records.append(

            {

                "Name_ID":
                    generate_uuid(),

                "First_Name":
                    name,

                "Last_Name":
                    LAST_NAMES[
                        FEMALE_NAMES.index(name)
                    ],

                "Gender":
                    "Female",

                "Title":
                    "Ms."

            }

        )

    dataframe = pd.DataFrame(
        records
    )

    filename = "reference_names.csv"

    save_reference_dataframe(
        dataframe,
        filename
    )

    print(
        "======================================="
    )

    print(
        f"Generated {len(dataframe)} reference names."
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

    generate_reference_names()