"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_medical_images_metadata.py

Purpose :
Generate medical image metadata records.

Input:
imaging_reports.csv

Output:
medical_images_metadata.csv

Author : Diya Lodha & Team
===========================================================
"""


import os
import sys
import random
import pandas as pd
import numpy as np


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


IMAGING_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "imaging_reports.csv"
)



# ==========================================================
# Generate Image Metadata
# ==========================================================


def generate_medical_images_metadata():


    show_progress(
        "Generating Medical Images Metadata Dataset"
    )



    imaging_reports = pd.read_csv(
        IMAGING_FILE
    )



    records = []

    total_records = len(imaging_reports)

    file_formats = np.random.choice(
        ["DICOM", "PNG", "JPEG"],
        total_records
    )

    image_sizes = np.round(
        np.random.uniform(
        1,
        250,
        total_records
        ),
        2
    )

    machine_ids = np.random.randint(
        1000,
        10000,
        total_records
    )

    storage_ids = np.random.randint(
        10000,
        100000,
        total_records
    ) 



    for i in range(
        len(imaging_reports)
    ):



        report = imaging_reports.iloc[i]



        record = {



            "Image_Metadata_ID":
                generate_uuid(),


            "Imaging_Report_ID":
                report["Imaging_Report_ID"],


            "Patient_ID":
                report["Patient_ID"],


            "Admission_ID":
                report["Admission_ID"],


            "Image_Type":
                report["Imaging_Type"],


            "File_Format":
                file_formats[i],


            "Image_Size_MB":
                image_sizes[i],

            "Modality":

                report["Imaging_Type"],


            "Machine_ID":
                f"IMG-{machine_ids[i]}",


            "Storage_Location":
                f"/hospital/pacs/images/{storage_ids[i]}",


            "Image_Status":
                "Stored"



        }



        records.append(
            record
        )



        if (i + 1) % 50000 == 0:

            print(
                f"{i+1} image metadata records generated"
            )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "medical_images_metadata.csv"
    )



    print(
        f"Generated {len(dataframe)} medical image metadata records"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_medical_images_metadata()