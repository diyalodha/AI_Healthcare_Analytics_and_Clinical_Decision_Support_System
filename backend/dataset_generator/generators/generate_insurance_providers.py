"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_insurance_providers.py

Purpose :
Generate ground-truth based insurance provider dataset.

Input:
reference/insurance_master.csv

Output:
datasets/synthetic/insurance_providers.csv

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


from utils import (
    generate_uuid,
    save_dataframe,
    show_progress
)



# ==========================================================
# Reference File
# ==========================================================

REFERENCE_FILE = os.path.join(
    PARENT_DIR,
    "reference",
    "insurance_master.csv"
)



# ==========================================================
# Generate Insurance Providers
# ==========================================================

def generate_insurance_providers():

    show_progress(
        "Generating Insurance Providers Dataset"
    )


    # Load Master Data

    insurance_df = pd.read_csv(
        REFERENCE_FILE
    )


    # Limit according to config

    insurance_df = insurance_df.head(
        config.NUM_INSURANCE_PROVIDERS
    )



    records = []



    for _, provider in insurance_df.iterrows():


        record = {


            "Insurance_Provider_ID":
                generate_uuid(),


            "Provider_Name":
                provider["Provider_Name"],


            "Provider_Type":
                provider["Provider_Type"],


            "Coverage_Type":
                provider["Coverage_Type"],


            "Network_Size":
                provider["Network_Size"],


            "Claim_Ratio":
                provider["Claim_Ratio"],


            "Status":
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
        "insurance_providers.csv"
    )



    print(
        f"Generated {len(dataframe)} insurance providers"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_insurance_providers()