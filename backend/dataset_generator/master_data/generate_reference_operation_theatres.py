"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File :
generate_reference_operation_theatres.py

Purpose :
Generate reference dataset for operation theatres.

Output :
reference_operation_theatres.csv

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
# Operation Theatre Master Data
# ==========================================================

OPERATION_THEATRES = [

    {
        "Reference_ID":"OT_REF_001",
        "OT_Code":"OT001",
        "OT_Name":"General Surgery OT",
        "OT_Category":"General",
        "Specialization":"General Surgery",
        "Capacity":"Major Procedures",
        "Floor_Number":2,
        "Equipment_Availability":"Standard Surgical Equipment",
        "Ventilation_System":"HEPA Filter",
        "Infection_Control_Level":"Level II",
        "Emergency_Available":"Yes",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },

    {
        "Reference_ID":"OT_REF_002",
        "OT_Code":"OT002",
        "OT_Name":"Cardiac Surgery OT",
        "OT_Category":"Specialized",
        "Specialization":"Cardiology & Cardiac Surgery",
        "Capacity":"Complex Cardiac Procedures",
        "Floor_Number":3,
        "Equipment_Availability":"Heart Lung Machine, Cardiac Monitor",
        "Ventilation_System":"Laminar Air Flow",
        "Infection_Control_Level":"Level III",
        "Emergency_Available":"Yes",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },

    {
        "Reference_ID":"OT_REF_003",
        "OT_Code":"OT003",
        "OT_Name":"Neurosurgery OT",
        "OT_Category":"Specialized",
        "Specialization":"Neurosurgery",
        "Capacity":"Brain & Spine Procedures",
        "Floor_Number":3,
        "Equipment_Availability":"Microscope, Neuro Navigation System",
        "Ventilation_System":"Laminar Air Flow",
        "Infection_Control_Level":"Level III",
        "Emergency_Available":"Yes",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },

    {
        "Reference_ID":"OT_REF_004",
        "OT_Code":"OT004",
        "OT_Name":"Orthopedic OT",
        "OT_Category":"Specialized",
        "Specialization":"Orthopedics",
        "Capacity":"Bone & Joint Procedures",
        "Floor_Number":2,
        "Equipment_Availability":"C-Arm, Orthopedic Tools",
        "Ventilation_System":"HEPA Filter",
        "Infection_Control_Level":"Level II",
        "Emergency_Available":"Yes",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },

    {
        "Reference_ID":"OT_REF_005",
        "OT_Code":"OT005",
        "OT_Name":"Emergency Trauma OT",
        "OT_Category":"Emergency",
        "Specialization":"Trauma Surgery",
        "Capacity":"Emergency Critical Procedures",
        "Floor_Number":1,
        "Equipment_Availability":"Advanced Trauma Equipment",
        "Ventilation_System":"HEPA Filter",
        "Infection_Control_Level":"Level III",
        "Emergency_Available":"Yes",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },

    {
        "Reference_ID":"OT_REF_006",
        "OT_Code":"OT006",
        "OT_Name":"Obstetrics & Gynecology OT",
        "OT_Category":"Specialized",
        "Specialization":"Obstetrics & Gynecology",
        "Capacity":"Delivery & Gynecological Procedures",
        "Floor_Number":4,
        "Equipment_Availability":"Delivery Equipment, Ultrasound",
        "Ventilation_System":"HEPA Filter",
        "Infection_Control_Level":"Level II",
        "Emergency_Available":"Yes",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },

    {
        "Reference_ID":"OT_REF_007",
        "OT_Code":"OT007",
        "OT_Name":"Ophthalmology OT",
        "OT_Category":"Specialized",
        "Specialization":"Eye Surgery",
        "Capacity":"Micro Surgical Procedures",
        "Floor_Number":2,
        "Equipment_Availability":"Operating Microscope",
        "Ventilation_System":"HEPA Filter",
        "Infection_Control_Level":"Level II",
        "Emergency_Available":"No",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },

    {
        "Reference_ID":"OT_REF_008",
        "OT_Code":"OT008",
        "OT_Name":"Robotic Surgery OT",
        "OT_Category":"Advanced",
        "Specialization":"Robotic Surgery",
        "Capacity":"Advanced Minimally Invasive Procedures",
        "Floor_Number":5,
        "Equipment_Availability":"Robotic Surgical System",
        "Ventilation_System":"Laminar Air Flow",
        "Infection_Control_Level":"Level III",
        "Emergency_Available":"Yes",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    }

]


# ==========================================================
# Generate Dataset
# ==========================================================

def generate_reference_operation_theatres():

    dataframe = pd.DataFrame(
        OPERATION_THEATRES
    )

    required_columns = [

        "Reference_ID",
        "OT_Code",
        "OT_Name"

    ]

    for column in required_columns:

        if column not in dataframe.columns:

            raise Exception(
                f"Missing required column : {column}"
            )

    save_reference_dataframe(
        dataframe,
        "reference_operation_theatres.csv"
    )

    print(
        "======================================="
    )

    print(
        f"Generated {len(dataframe)} operation theatre records."
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

    generate_reference_operation_theatres()