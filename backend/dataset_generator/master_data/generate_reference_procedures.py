"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File :
generate_reference_procedures.py

Purpose :
Generate reference dataset for medical procedures.

Output :
reference_procedures.csv

Author :
Diya Lodha & Team
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
# Medical Procedure Master Data
# ==========================================================

PROCEDURES = [

    {
        "Reference_ID":"PROC_REF_001",
        "Procedure_Code":"PROC001",
        "Procedure_Name":"General Surgery",
        "Procedure_Category":"Surgical",
        "Department":"General Surgery",
        "Complexity_Level":"Medium",
        "Average_Duration_Minutes":120,
        "Requires_OT":"Yes",
        "Requires_Anesthesia":"Yes",
        "Common_Usage":"Abdominal and general operations",
        "Status":"Active",
        "Created_Source":"Ground_Truth_Reference"
    },

    {
        "Reference_ID":"PROC_REF_002",
        "Procedure_Code":"PROC002",
        "Procedure_Name":"Appendectomy",
        "Procedure_Category":"Surgical",
        "Department":"General Surgery",
        "Complexity_Level":"Medium",
        "Average_Duration_Minutes":90,
        "Requires_OT":"Yes",
        "Requires_Anesthesia":"Yes",
        "Common_Usage":"Appendicitis treatment",
        "Status":"Active",
        "Created_Source":"Ground_Truth_Reference"
    },

    {
        "Reference_ID":"PROC_REF_003",
        "Procedure_Code":"PROC003",
        "Procedure_Name":"Coronary Artery Bypass Surgery",
        "Procedure_Category":"Cardiac Surgery",
        "Department":"Cardiology",
        "Complexity_Level":"High",
        "Average_Duration_Minutes":360,
        "Requires_OT":"Yes",
        "Requires_Anesthesia":"Yes",
        "Common_Usage":"Blocked coronary artery treatment",
        "Status":"Active",
        "Created_Source":"Ground_Truth_Reference"
    },

    {
        "Reference_ID":"PROC_REF_004",
        "Procedure_Code":"PROC004",
        "Procedure_Name":"Angioplasty",
        "Procedure_Category":"Cardiac Procedure",
        "Department":"Cardiology",
        "Complexity_Level":"High",
        "Average_Duration_Minutes":120,
        "Requires_OT":"No",
        "Requires_Anesthesia":"Yes",
        "Common_Usage":"Coronary artery blockage",
        "Status":"Active",
        "Created_Source":"Ground_Truth_Reference"
    },

    {
        "Reference_ID":"PROC_REF_005",
        "Procedure_Code":"PROC005",
        "Procedure_Name":"MRI Scan",
        "Procedure_Category":"Diagnostic Imaging",
        "Department":"Radiology",
        "Complexity_Level":"Low",
        "Average_Duration_Minutes":60,
        "Requires_OT":"No",
        "Requires_Anesthesia":"Sometimes",
        "Common_Usage":"Disease diagnosis and imaging",
        "Status":"Active",
        "Created_Source":"Ground_Truth_Reference"
    },

    {
        "Reference_ID":"PROC_REF_006",
        "Procedure_Code":"PROC006",
        "Procedure_Name":"CT Scan",
        "Procedure_Category":"Diagnostic Imaging",
        "Department":"Radiology",
        "Complexity_Level":"Low",
        "Average_Duration_Minutes":30,
        "Requires_OT":"No",
        "Requires_Anesthesia":"No",
        "Common_Usage":"Internal body imaging",
        "Status":"Active",
        "Created_Source":"Ground_Truth_Reference"
    },

    {
        "Reference_ID":"PROC_REF_007",
        "Procedure_Code":"PROC007",
        "Procedure_Name":"ICU Ventilator Support",
        "Procedure_Category":"Critical Care",
        "Department":"ICU",
        "Complexity_Level":"High",
        "Average_Duration_Minutes":1440,
        "Requires_OT":"No",
        "Requires_Anesthesia":"No",
        "Common_Usage":"Respiratory failure management",
        "Status":"Active",
        "Created_Source":"Ground_Truth_Reference"
    },

    {
        "Reference_ID":"PROC_REF_008",
        "Procedure_Code":"PROC008",
        "Procedure_Name":"Blood Transfusion",
        "Procedure_Category":"Therapeutic",
        "Department":"Blood Bank",
        "Complexity_Level":"Medium",
        "Average_Duration_Minutes":180,
        "Requires_OT":"No",
        "Requires_Anesthesia":"No",
        "Common_Usage":"Blood component replacement",
        "Status":"Active",
        "Created_Source":"Ground_Truth_Reference"
    },

    {
        "Reference_ID":"PROC_REF_009",
        "Procedure_Code":"PROC009",
        "Procedure_Name":"Kidney Transplant",
        "Procedure_Category":"Transplant Surgery",
        "Department":"Nephrology",
        "Complexity_Level":"Very High",
        "Average_Duration_Minutes":480,
        "Requires_OT":"Yes",
        "Requires_Anesthesia":"Yes",
        "Common_Usage":"End stage kidney disease",
        "Status":"Active",
        "Created_Source":"Ground_Truth_Reference"
    },

    {
        "Reference_ID":"PROC_REF_010",
        "Procedure_Code":"PROC010",
        "Procedure_Name":"Chemotherapy",
        "Procedure_Category":"Therapeutic",
        "Department":"Oncology",
        "Complexity_Level":"Medium",
        "Average_Duration_Minutes":240,
        "Requires_OT":"No",
        "Requires_Anesthesia":"No",
        "Common_Usage":"Cancer treatment",
        "Status":"Active",
        "Created_Source":"Ground_Truth_Reference"
    }

]


# ==========================================================
# Generate Dataset
# ==========================================================

def generate_reference_procedures():

    dataframe = pd.DataFrame(
        PROCEDURES
    )

    required_columns = [

        "Reference_ID",
        "Procedure_Code",
        "Procedure_Name"

    ]

    for column in required_columns:

        if column not in dataframe.columns:

            raise Exception(
                f"Missing required column : {column}"
            )

    save_reference_dataframe(
        dataframe,
        "reference_procedures.csv"
    )

    print(
        "======================================="
    )

    print(
        f"Generated {len(dataframe)} procedure records."
    )

    print(
        "Stored in : reference/"
    )

    print(
        "======================================="
    )

    print(
        dataframe.head()
    )


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    generate_reference_procedures()