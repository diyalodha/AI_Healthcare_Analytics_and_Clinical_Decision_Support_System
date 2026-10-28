"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_imaging_reports.py

Purpose :
Generate medical imaging report dataset.

Input:
admissions.csv
doctors.csv
departments.csv

Output:
imaging_reports.csv

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


ADMISSION_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "admissions.csv"
)


DOCTOR_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "doctors.csv"
)


DEPARTMENT_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "departments.csv"
)



# ==========================================================
# Imaging Types
# ==========================================================


IMAGING_TYPES = [

    {
        "Type": "X-Ray",
        "Body_Part": "Chest"
    },

    {
        "Type": "MRI",
        "Body_Part": "Brain"
    },

    {
        "Type": "CT Scan",
        "Body_Part": "Abdomen"
    },

    {
        "Type": "Ultrasound",
        "Body_Part": "Abdomen"
    },

    {
        "Type": "Echocardiography",
        "Body_Part": "Heart"
    },

    {
        "Type": "Mammography",
        "Body_Part": "Breast"
    }

]



# ==========================================================
# Generate Imaging Reports
# ==========================================================


def generate_imaging_reports():


    show_progress(
        "Generating Imaging Reports Dataset"
    )



    admissions = pd.read_csv(
        ADMISSION_FILE
    )


    doctors = pd.read_csv(
        DOCTOR_FILE
    )


    departments = pd.read_csv(
        DEPARTMENT_FILE
    )



    records = []

    admission_index = np.random.randint(
        0,
        len(admissions),
        config.NUM_IMAGING_REPORTS
    )

    doctor_index = np.random.randint(
        0,
        len(doctors),
        config.NUM_IMAGING_REPORTS
)



    radiology_department = departments[
        departments["Department_Code"] == "RAD"
    ]



    if len(radiology_department) > 0:

        radiology_id = (
            radiology_department.iloc[0]
            ["Department_ID"]
        )

    else:

        radiology_id = None



    for i in range(
        config.NUM_IMAGING_REPORTS
    ):



        admission = admissions.iloc[admission_index[i]]


        doctor = doctors.iloc[doctor_index[i]]


        imaging = random.choice(
            IMAGING_TYPES
        )



        record = {



            "Imaging_Report_ID":
                generate_uuid(),


            "Patient_ID":
                admission["Patient_ID"],


            "Admission_ID":
                admission["Admission_ID"],


            "Radiology_Department_ID":
                radiology_id,


            "Doctor_ID":
                doctor["Doctor_ID"],


            "Imaging_Type":
                imaging["Type"],


            "Body_Part":
                imaging["Body_Part"],


            "Imaging_Date":
                admission["Admission_Date"],


            "Findings":

                (
                "Imaging examination completed. "
                "Clinical findings documented "
                "by radiologist."
                ),


            "Impression":
                random.choice(
                    [
                    "Normal study",
                    "Abnormal findings detected",
                    "Further evaluation required",
                    "Follow up recommended"
                    ]
                ),


            "Report_Status":
                "Final"



        }


        records.append(
            record
        )



        if (i + 1) % 50000 == 0:

            print(
                f"{i+1} imaging reports generated"
            )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "imaging_reports.csv"
    )



    print(
        f"Generated {len(dataframe)} imaging reports"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_imaging_reports()