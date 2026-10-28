"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 01_generate_departments.py

Purpose :
Generate ground-truth based synthetic hospital department
dataset.

Output:
datasets/synthetic/departments.csv

Author : Diya Lodha & Team
===========================================================
"""


import os
import sys
import random
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

import config

from utils import (
    generate_uuid,
    save_dataframe,
    show_progress
)


# ==========================================================
# Ground Truth Department Master Data
# ==========================================================


DEPARTMENTS = [

    {
        "Department_Name": "Emergency Medicine",
        "Department_Code": "EM",
        "Description": "Emergency and trauma care",
        "Department_Type": "Clinical",
        "Is_24x7": True,
        "Capacity": 120
    },

    {
        "Department_Name": "General Medicine",
        "Department_Code": "GENMED",
        "Description": "Adult medical care",
        "Department_Type": "Clinical",
        "Is_24x7": True,
        "Capacity": 180
    },

    {
        "Department_Name": "Cardiology",
        "Department_Code": "CARD",
        "Description": "Heart diseases",
        "Department_Type": "Clinical",
        "Is_24x7": False,
        "Capacity": 90
    },

    {
        "Department_Name": "Neurology",
        "Department_Code": "NEURO",
        "Description": "Brain and nervous system",
        "Department_Type": "Clinical",
        "Is_24x7": False,
        "Capacity": 80
    },

    {
        "Department_Name": "Nephrology",
        "Department_Code": "NEPH",
        "Description": "Kidney disorders",
        "Department_Type": "Clinical",
        "Is_24x7": False,
        "Capacity": 70
    },

    {
        "Department_Name": "Gastroenterology",
        "Department_Code": "GASTRO",
        "Description": "Digestive system",
        "Department_Type": "Clinical",
        "Is_24x7": False,
        "Capacity": 75
    },

    {
        "Department_Name": "Pulmonology",
        "Department_Code": "PULMO",
        "Description": "Respiratory diseases",
        "Department_Type": "Clinical",
        "Is_24x7": False,
        "Capacity": 70
    },

    {
        "Department_Name": "Orthopedics",
        "Department_Code": "ORTHO",
        "Description": "Bones and joints",
        "Department_Type": "Clinical",
        "Is_24x7": False,
        "Capacity": 100
    },

    {
        "Department_Name": "Oncology",
        "Department_Code": "ONCO",
        "Description": "Cancer treatment",
        "Department_Type": "Clinical",
        "Is_24x7": False,
        "Capacity": 110
    },

    {
        "Department_Name": "Pediatrics",
        "Department_Code": "PED",
        "Description": "Child healthcare",
        "Department_Type": "Clinical",
        "Is_24x7": False,
        "Capacity": 90
    },

    {
        "Department_Name": "Gynecology",
        "Department_Code": "GYN",
        "Description": "Women's healthcare",
        "Department_Type": "Clinical",
        "Is_24x7": False,
        "Capacity": 80
    },

    {
        "Department_Name": "Obstetrics",
        "Department_Code": "OBS",
        "Description": "Pregnancy and childbirth",
        "Department_Type": "Clinical",
        "Is_24x7": True,
        "Capacity": 70
    },

    {
        "Department_Name": "Dermatology",
        "Department_Code": "DERM",
        "Description": "Skin disorders",
        "Department_Type": "Clinical",
        "Is_24x7": False,
        "Capacity": 50
    },

    {
        "Department_Name": "Psychiatry",
        "Department_Code": "PSY",
        "Description": "Mental health",
        "Department_Type": "Clinical",
        "Is_24x7": False,
        "Capacity": 60
    },

    {
        "Department_Name": "ENT",
        "Department_Code": "ENT",
        "Description": "Ear, Nose and Throat",
        "Department_Type": "Clinical",
        "Is_24x7": False,
        "Capacity": 60
    },

    {
        "Department_Name": "Ophthalmology",
        "Department_Code": "OPH",
        "Description": "Eye care",
        "Department_Type": "Clinical",
        "Is_24x7": False,
        "Capacity": 55
    },

    {
        "Department_Name": "Dentistry",
        "Department_Code": "DENT",
        "Description": "Dental care",
        "Department_Type": "Clinical",
        "Is_24x7": False,
        "Capacity": 45
    },

    {
        "Department_Name": "Radiology",
        "Department_Code": "RAD",
        "Description": "Medical imaging",
        "Department_Type": "Diagnostic",
        "Is_24x7": True,
        "Capacity": 60
    },

    {
        "Department_Name": "Pathology Laboratory",
        "Department_Code": "LAB",
        "Description": "Clinical laboratory",
        "Department_Type": "Diagnostic",
        "Is_24x7": True,
        "Capacity": 50
    },

    {
        "Department_Name": "Blood Bank",
        "Department_Code": "BB",
        "Description": "Blood collection and storage",
        "Department_Type": "Support",
        "Is_24x7": True,
        "Capacity": 30
    },

    {
        "Department_Name": "Pharmacy",
        "Department_Code": "PHARM",
        "Description": "Medicine dispensing",
        "Department_Type": "Support",
        "Is_24x7": True,
        "Capacity": 40
    },

    {
        "Department_Name": "ICU",
        "Department_Code": "ICU",
        "Description": "Critical care",
        "Department_Type": "Clinical",
        "Is_24x7": True,
        "Capacity": 70
    },

    {
        "Department_Name": "Operation Theatre",
        "Department_Code": "OT",
        "Description": "Surgical operations",
        "Department_Type": "Clinical",
        "Is_24x7": True,
        "Capacity": 20
    },

    {
        "Department_Name": "Physiotherapy",
        "Department_Code": "PT",
        "Description": "Physical rehabilitation",
        "Department_Type": "Support",
        "Is_24x7": False,
        "Capacity": 40
    },

    {
        "Department_Name": "Administration",
        "Department_Code": "ADMIN",
        "Description": "Hospital administration",
        "Department_Type": "Administrative",
        "Is_24x7": False,
        "Capacity": 100
    }

]


# ==========================================================
# Generate Departments
# ==========================================================


def generate_departments():

    show_progress(
        "Generating Hospital Departments"
    )


    records = []


    for dept in DEPARTMENTS[:config.NUM_DEPARTMENTS]:


        record = {

            "Department_ID":
                generate_uuid(),


            "Department_Name":
                dept["Department_Name"],


            "Department_Code":
                dept["Department_Code"],


            "Description":
                dept["Description"],


            "Department_Type":
                dept["Department_Type"],


            "Contact_Number":
                "020-" +
                str(
                    random.randint(
                        10000000,
                        99999999
                    )
                ),


            "Email":
                dept["Department_Code"].lower()
                +
                "@healthcare.com",


            "Location":
                "Main Hospital Campus",


            "Floor_Number":
                random.randint(
                    1,
                    8
                ),


            "Extension_Number":
                str(
                    random.randint(
                        1000,
                        9999
                    )
                ),


            "Head_Doctor_ID":
                None,


            "Total_Doctors":
                random.randint(
                    5,
                    40
                ),


            "Total_Staff":
                random.randint(
                    20,
                    150
                ),


            "Capacity":
                dept["Capacity"],


            "Opening_Time":
                "00:00:00"
                if dept["Is_24x7"]
                else "08:00:00",


            "Closing_Time":
                "23:59:59"
                if dept["Is_24x7"]
                else "20:00:00",


            "Is_24x7":
                dept["Is_24x7"],


            "Status":
                "Active",


            "Is_Active":
                True

        }


        records.append(record)



    dataframe = pd.DataFrame(records)



    save_dataframe(
        dataframe,
        "departments.csv"
    )


    print(
        f"Generated {len(dataframe)} departments"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_departments()