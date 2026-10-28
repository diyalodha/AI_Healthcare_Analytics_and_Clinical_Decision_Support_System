"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_beds.py

Purpose :
Generate hospital bed master dataset.

Input:
hospital_rooms.csv

Output:
beds.csv

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


ROOM_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "hospital_rooms.csv"
)



# ==========================================================
# Generate Beds
# ==========================================================


def generate_beds():


    show_progress(
        "Generating Hospital Beds Dataset"
    )



    rooms = pd.read_csv(
        ROOM_FILE
    )



    records = []



    for room in rooms.itertuples():



        capacity = int(
            room.Capacity
        )



        for bed_number in range(
            1,
            capacity + 1
        ):



            record = {



                "Bed_ID":
                    generate_uuid(),


                "Room_ID":
                    room.Room_ID,


                "Bed_Number":
                    (
                    str(
                        room.Room_Number
                    )
                    +
                    "-"
                    +
                    str(
                        bed_number
                    )
                    ),


                "Bed_Type":
                    room.Room_Type,


                "Availability_Status":
                    random.choice(
                        [
                        "Available",
                        "Occupied",
                        "Maintenance"
                        ]
                    ),


                "Current_Status":
                    "Active"



            }


            records.append(
                record
            )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "beds.csv"
    )



    print(
        f"Generated {len(dataframe)} beds"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_beds()