"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_reference_locations.py

Purpose :
Generate reference locations dataset.

Output:
reference_locations.csv

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


from utils import (
    generate_uuid,
    save_reference_dataframe,
    show_progress
)


# ==========================================================
# Location Data
# ==========================================================

LOCATIONS = [

    ("Mumbai", "Maharashtra", "India", "400001"),
    ("Pune", "Maharashtra", "India", "411001"),
    ("Nagpur", "Maharashtra", "India", "440001"),
    ("Nashik", "Maharashtra", "India", "422001"),
    ("Solapur", "Maharashtra", "India", "413001"),
    ("Kolhapur", "Maharashtra", "India", "416001"),
    ("Aurangabad", "Maharashtra", "India", "431001"),
    ("Ahmedabad", "Gujarat", "India", "380001"),
    ("Surat", "Gujarat", "India", "395001"),
    ("Vadodara", "Gujarat", "India", "390001"),
    ("Rajkot", "Gujarat", "India", "360001"),
    ("Jaipur", "Rajasthan", "India", "302001"),
    ("Udaipur", "Rajasthan", "India", "313001"),
    ("Jodhpur", "Rajasthan", "India", "342001"),
    ("Delhi", "Delhi", "India", "110001"),
    ("Bengaluru", "Karnataka", "India", "560001"),
    ("Hyderabad", "Telangana", "India", "500001"),
    ("Chennai", "Tamil Nadu", "India", "600001"),
    ("Kolkata", "West Bengal", "India", "700001"),
    ("Lucknow", "Uttar Pradesh", "India", "226001")

]


# ==========================================================
# Generate Reference Locations
# ==========================================================

def generate_reference_locations():

    show_progress(
        "Generating Reference Locations"
    )

    records = []

    for city, state, country, pincode in LOCATIONS:

        record = {

            "Location_ID":
                generate_uuid(),

            "City":
                city,

            "State":
                state,

            "Country":
                country,

            "Postal_Code":
                pincode,

            "Latitude":
                "",

            "Longitude":
                ""

        }

        records.append(
            record
        )

    dataframe = pd.DataFrame(
        records
    )

    save_reference_dataframe(
        dataframe,
        "reference_locations.csv"
    )

    print(
        f"Generated {len(dataframe)} reference locations."
    )


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    generate_reference_locations()