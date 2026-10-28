"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_hospital_rooms.py

Purpose :
Generate hospital room master dataset.

Input:
departments.csv

Output:
hospital_rooms.csv

Author : Diya Lodha & Team
===========================================================
"""


import os
import sys
import random
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
    save_dataframe,
    show_progress
)



# ==========================================================
# File
# ==========================================================


DEPARTMENT_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "departments.csv"
)



# ==========================================================
# Ground Truth Room Types
# ==========================================================


ROOM_TYPES = [

    {
        "Type": "General Ward",
        "Capacity": 6
    },

    {
        "Type": "Semi Private",
        "Capacity": 2
    },

    {
        "Type": "Private Room",
        "Capacity": 1
    },

    {
        "Type": "ICU Room",
        "Capacity": 1
    },

    {
        "Type": "Isolation Room",
        "Capacity": 1
    }

]



# ==========================================================
# Generate Rooms
# ==========================================================


def generate_hospital_rooms():


    show_progress(
        "Generating Hospital Rooms Dataset"
    )


    departments = pd.read_csv(
        DEPARTMENT_FILE
    )



    records = []



    room_number = 1001



    for department in departments.itertuples():


        number_of_rooms = random.randint(
            10,
            40
        )



        for i in range(
            number_of_rooms
        ):


            room = random.choice(
                ROOM_TYPES
            )


            record = {


                "Room_ID":
                    generate_uuid(),


                "Department_ID":
                    department.Department_ID,


                "Room_Number":
                    str(
                        room_number
                    ),


                "Room_Type":
                    room["Type"],


                "Capacity":
                    room["Capacity"],


                "Floor_Number":
                    random.randint(
                        1,
                        10
                    ),


                "Availability_Status":
                    "Available",


                "Is_ICU":
                    True
                    if room["Type"] == "ICU Room"
                    else False,


                "Room_Status":
                    "Active"


            }


            records.append(
                record
            )


            room_number += 1



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "hospital_rooms.csv"
    )



    print(
        f"Generated {len(dataframe)} hospital rooms"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_hospital_rooms()