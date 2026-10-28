"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_clinical_notes.py

Purpose :
Generate clinical notes dataset.

Optimized version for faster generation.

Output:
clinical_notes.csv

Records:
500000

Author : Diya Lodha & Team
===========================================================
"""


import os
import sys
import random
import numpy as np
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
# Files
# ==========================================================


PATIENT_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "patients.csv"
)


ADMISSION_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "admissions.csv"
)


DOCTOR_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "doctors.csv"
)



# ==========================================================
# Clinical Note Templates
# ==========================================================


NOTE_TYPES = [

    "Progress Note",
    "Discharge Note",
    "Consultation Note",
    "Nursing Note",
    "Emergency Note",
    "Follow Up Note"

]


OBSERVATIONS = [

    "Patient condition stable",
    "Symptoms improving",
    "Patient requires monitoring",
    "Treatment continued",
    "Further investigation required",
    "Patient responding well to medication"

]


# ==========================================================
# Generate Clinical Notes
# ==========================================================


def generate_clinical_notes():


    show_progress(
        "Generating Clinical Notes Dataset"
    )



    patients = pd.read_csv(
        PATIENT_FILE
    )


    admissions = pd.read_csv(
        ADMISSION_FILE
    )


    doctors = pd.read_csv(
        DOCTOR_FILE
    )



    patient_ids = patients[
        "Patient_ID"
    ].values


    admission_ids = admissions[
        "Admission_ID"
    ].values


    doctor_ids = doctors[
        "Doctor_ID"
    ].values



    records = []



    total = config.NUM_CLINICAL_NOTES



    for start in range(
        0,
        total,
        config.CLINICAL_NOTE_CHUNK_SIZE
    ):


        size = min(
            config.CLINICAL_NOTE_CHUNK_SIZE,
            total-start
        )



        patient_sample = np.random.choice(
            patient_ids,
            size=size
        )


        admission_sample = np.random.choice(
            admission_ids,
            size=size
        )


        doctor_sample = np.random.choice(
            doctor_ids,
            size=size
        )



        for i in range(size):


            note = (

                random.choice(
                    OBSERVATIONS
                )

                +
                ". Patient evaluated by physician. "

                +
                "Clinical management plan documented."

            )



            records.append(

                {


                "Clinical_Note_ID":
                    generate_uuid(),


                "Patient_ID":
                    patient_sample[i],


                "Admission_ID":
                    admission_sample[i],


                "Doctor_ID":
                    doctor_sample[i],


                "Note_Type":
                    random.choice(
                        NOTE_TYPES
                    ),


                "Note_Date":
                    str(
                        pd.Timestamp.now().date()
                    ),


                "Clinical_Text":
                    note,


                "Priority":
                    random.choice(
                        [
                        "Routine",
                        "Urgent",
                        "Critical"
                        ]
                    ),


                "Status":
                    "Completed"



                }

            )



        print(
            f"{len(records)} clinical notes generated"
        )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "clinical_notes.csv"
    )



    print(
        f"Generated {len(dataframe)} clinical notes"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_clinical_notes()