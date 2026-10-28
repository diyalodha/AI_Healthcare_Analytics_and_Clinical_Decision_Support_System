"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File :
move_reference_files.py

Purpose :
Move reference master CSV files from synthetic folder
to reference folder.

Author : Diya Lodha & Team
===========================================================
"""


import os
import shutil


# ==========================================================
# Paths
# ==========================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


DATASET_GENERATOR_DIR = os.path.dirname(
    CURRENT_DIR
)


SYNTHETIC_DIR = os.path.join(
    DATASET_GENERATOR_DIR,
    "synthetic"
)


REFERENCE_DIR = os.path.join(
    DATASET_GENERATOR_DIR,
    "reference"
)


# Create reference folder if missing

os.makedirs(
    REFERENCE_DIR,
    exist_ok=True
)



# ==========================================================
# Files To Move
# ==========================================================

REFERENCE_FILES = [

    "reference_ai_models.csv",

    "reference_allergies.csv",

    "reference_blood_components.csv",

    "reference_departments.csv",

    "reference_diagnosis_codes.csv",

    "diseases_master.csv",

    "reference_lab_tests.csv"

]



# ==========================================================
# Move Files
# ==========================================================


def move_reference_files():


    print(
        "\nMoving reference files...\n"
    )


    for file in REFERENCE_FILES:


        source = os.path.join(
            SYNTHETIC_DIR,
            file
        )


        destination = os.path.join(
            REFERENCE_DIR,
            file
        )


        if os.path.exists(source):


            shutil.move(
                source,
                destination
            )


            print(
                f"Moved : {file}"
            )


        else:


            print(
                f"Not Found : {file}"
            )


    print(
        "\nReference file movement completed."
    )



# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    move_reference_files()