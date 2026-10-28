"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File :
generate_reference_blood_components.py

Purpose :
Generate reference master dataset for blood components.

Output :
reference_blood_components.csv

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



# ==========================================================
# Blood Component Master Data
# ==========================================================


BLOOD_COMPONENTS = [

    {
        "Reference_ID":"BC_REF_001",
        "Component_Code":"BC001",
        "Component_Name":"Whole Blood",
        "Component_Category":"Whole Blood",
        "Compatible_Blood_Groups":"All",
        "Storage_Temperature":"2-6°C",
        "Shelf_Life":"35 Days",
        "Common_Indications":"Massive Blood Loss",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },


    {
        "Reference_ID":"BC_REF_002",
        "Component_Code":"BC002",
        "Component_Name":"Packed Red Blood Cells",
        "Component_Category":"RBC",
        "Compatible_Blood_Groups":"A+,A-,B+,B-,AB+,AB-,O+,O-",
        "Storage_Temperature":"2-6°C",
        "Shelf_Life":"42 Days",
        "Common_Indications":"Anemia, Blood Loss",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },


    {
        "Reference_ID":"BC_REF_003",
        "Component_Code":"BC003",
        "Component_Name":"Fresh Frozen Plasma",
        "Component_Category":"Plasma",
        "Compatible_Blood_Groups":"AB Universal Plasma",
        "Storage_Temperature":"-30°C",
        "Shelf_Life":"1 Year",
        "Common_Indications":"Coagulation Disorders",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },


    {
        "Reference_ID":"BC_REF_004",
        "Component_Code":"BC004",
        "Component_Name":"Platelet Concentrate",
        "Component_Category":"Platelets",
        "Compatible_Blood_Groups":"Compatible",
        "Storage_Temperature":"20-24°C",
        "Shelf_Life":"5 Days",
        "Common_Indications":"Thrombocytopenia",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },


    {
        "Reference_ID":"BC_REF_005",
        "Component_Code":"BC005",
        "Component_Name":"Cryoprecipitate",
        "Component_Category":"Plasma Derivative",
        "Compatible_Blood_Groups":"Compatible",
        "Storage_Temperature":"-30°C",
        "Shelf_Life":"1 Year",
        "Common_Indications":"Factor VIII Deficiency",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },


    {
        "Reference_ID":"BC_REF_006",
        "Component_Code":"BC006",
        "Component_Name":"Leukocyte Reduced RBC",
        "Component_Category":"RBC Modified",
        "Compatible_Blood_Groups":"Compatible",
        "Storage_Temperature":"2-6°C",
        "Shelf_Life":"42 Days",
        "Common_Indications":"Immunocompromised Patients",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },


    {
        "Reference_ID":"BC_REF_007",
        "Component_Code":"BC007",
        "Component_Name":"Irradiated RBC",
        "Component_Category":"RBC Modified",
        "Compatible_Blood_Groups":"Compatible",
        "Storage_Temperature":"2-6°C",
        "Shelf_Life":"28 Days",
        "Common_Indications":"Cancer Patients, Transplant Patients",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },


    {
        "Reference_ID":"BC_REF_008",
        "Component_Code":"BC008",
        "Component_Name":"Single Donor Platelets",
        "Component_Category":"Platelets",
        "Compatible_Blood_Groups":"Compatible",
        "Storage_Temperature":"20-24°C",
        "Shelf_Life":"5 Days",
        "Common_Indications":"Critical Care",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },


    {
        "Reference_ID":"BC_REF_009",
        "Component_Code":"BC009",
        "Component_Name":"Granulocyte Concentrate",
        "Component_Category":"Cellular Component",
        "Compatible_Blood_Groups":"Compatible",
        "Storage_Temperature":"20-24°C",
        "Shelf_Life":"24 Hours",
        "Common_Indications":"Severe Infection, Neutropenia",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },


    {
        "Reference_ID":"BC_REF_010",
        "Component_Code":"BC010",
        "Component_Name":"Albumin",
        "Component_Category":"Plasma Protein",
        "Compatible_Blood_Groups":"Universal",
        "Storage_Temperature":"Room Temperature",
        "Shelf_Life":"3 Years",
        "Common_Indications":"Hypovolemia",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },


    {
        "Reference_ID":"BC_REF_011",
        "Component_Code":"BC011",
        "Component_Name":"Immunoglobulin",
        "Component_Category":"Plasma Derivative",
        "Compatible_Blood_Groups":"Universal",
        "Storage_Temperature":"2-8°C",
        "Shelf_Life":"2 Years",
        "Common_Indications":"Immune Disorders",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    },


    {
        "Reference_ID":"BC_REF_012",
        "Component_Code":"BC012",
        "Component_Name":"Stem Cell Product",
        "Component_Category":"Cellular Therapy",
        "Compatible_Blood_Groups":"Matched",
        "Storage_Temperature":"Liquid Nitrogen",
        "Shelf_Life":"Long Term",
        "Common_Indications":"Bone Marrow Transplant",
        "Status":"Active",
        "Created_Source":"Synthetic_Master_Data"
    }

]



# ==========================================================
# Generate Dataset
# ==========================================================


def generate_reference_blood_components():


    dataframe = pd.DataFrame(
        BLOOD_COMPONENTS
    )


    # Validation

    required_columns = [

        "Reference_ID",
        "Component_Code",
        "Component_Name"

    ]


    for column in required_columns:

        if column not in dataframe.columns:

            raise Exception(
                f"Missing required column : {column}"
            )


    path = os.path.join(
        config.REFERENCE_DIR,
        "reference_blood_components.csv"
    )

    dataframe.to_csv(
        path,
        index=False
    )

    print(
        "Created reference_blood_components.csv"
    )


    print(
        "======================================="
    )

    print(
        f"Generated {len(dataframe)} blood component records."
    )

    print(
        "File : reference_blood_components.csv"
    )

    print(
        "======================================="
    )


    print("\nDataset Preview:")
    print(
        dataframe.head()
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_reference_blood_components()