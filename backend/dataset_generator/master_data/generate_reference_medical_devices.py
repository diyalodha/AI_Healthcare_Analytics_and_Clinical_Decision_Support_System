"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_reference_medical_devices.py

Purpose :
Generate Medical Devices Reference Dataset

Output :
reference_medical_devices.csv

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
# Medical Devices Reference Data
# ==========================================================

DEVICES = [

    {
        "Device_Code":"DEV001",
        "Device_Name":"Ventilator",
        "Category":"Respiratory",
        "Manufacturer":"Philips",
        "Maintenance_Interval":"6 Months",
        "Status":"Active"
    },

    {
        "Device_Code":"DEV002",
        "Device_Name":"ECG Machine",
        "Category":"Cardiology",
        "Manufacturer":"GE Healthcare",
        "Maintenance_Interval":"12 Months",
        "Status":"Active"
    },

    {
        "Device_Code":"DEV003",
        "Device_Name":"Patient Monitor",
        "Category":"Monitoring",
        "Manufacturer":"Mindray",
        "Maintenance_Interval":"6 Months",
        "Status":"Active"
    },

    {
        "Device_Code":"DEV004",
        "Device_Name":"Defibrillator",
        "Category":"Emergency",
        "Manufacturer":"Zoll",
        "Maintenance_Interval":"12 Months",
        "Status":"Active"
    },

    {
        "Device_Code":"DEV005",
        "Device_Name":"Infusion Pump",
        "Category":"Medication Delivery",
        "Manufacturer":"Baxter",
        "Maintenance_Interval":"6 Months",
        "Status":"Active"
    },

    {
        "Device_Code":"DEV006",
        "Device_Name":"Dialysis Machine",
        "Category":"Nephrology",
        "Manufacturer":"Fresenius",
        "Maintenance_Interval":"6 Months",
        "Status":"Active"
    },

    {
        "Device_Code":"DEV007",
        "Device_Name":"MRI Scanner",
        "Category":"Radiology",
        "Manufacturer":"Siemens",
        "Maintenance_Interval":"12 Months",
        "Status":"Active"
    },

    {
        "Device_Code":"DEV008",
        "Device_Name":"CT Scanner",
        "Category":"Radiology",
        "Manufacturer":"GE Healthcare",
        "Maintenance_Interval":"12 Months",
        "Status":"Active"
    },

    {
        "Device_Code":"DEV009",
        "Device_Name":"Ultrasound Machine",
        "Category":"Radiology",
        "Manufacturer":"Samsung",
        "Maintenance_Interval":"12 Months",
        "Status":"Active"
    },

    {
        "Device_Code":"DEV010",
        "Device_Name":"X-Ray Machine",
        "Category":"Radiology",
        "Manufacturer":"Canon",
        "Maintenance_Interval":"12 Months",
        "Status":"Active"
    },

    {
        "Device_Code":"DEV011",
        "Device_Name":"Pulse Oximeter",
        "Category":"Monitoring",
        "Manufacturer":"Masimo",
        "Maintenance_Interval":"12 Months",
        "Status":"Active"
    },

    {
        "Device_Code":"DEV012",
        "Device_Name":"Blood Gas Analyzer",
        "Category":"Laboratory",
        "Manufacturer":"Radiometer",
        "Maintenance_Interval":"12 Months",
        "Status":"Active"
    },

    {
        "Device_Code":"DEV013",
        "Device_Name":"Anesthesia Workstation",
        "Category":"Operation Theater",
        "Manufacturer":"Drager",
        "Maintenance_Interval":"6 Months",
        "Status":"Active"
    },

    {
        "Device_Code":"DEV014",
        "Device_Name":"Syringe Pump",
        "Category":"Medication Delivery",
        "Manufacturer":"B Braun",
        "Maintenance_Interval":"6 Months",
        "Status":"Active"
    },

    {
        "Device_Code":"DEV015",
        "Device_Name":"Hospital Bed Monitor",
        "Category":"Monitoring",
        "Manufacturer":"Hillrom",
        "Maintenance_Interval":"12 Months",
        "Status":"Active"
    }

]


# ==========================================================
# Generate Dataset
# ==========================================================

def generate_reference_medical_devices():

    dataframe = pd.DataFrame(
        DEVICES
    )

    filename = "reference_medical_devices.csv"

    save_reference_dataframe(
        dataframe,
        filename
    )

    print(
        "======================================="
    )

    print(
        f"Generated {len(dataframe)} medical device references."
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

    generate_reference_medical_devices()