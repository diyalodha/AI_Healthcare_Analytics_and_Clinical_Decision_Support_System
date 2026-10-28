"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File :
cleanup_synthetic_reference_files.py

Purpose :
Remove reference master CSV files accidentally generated
inside synthetic folder.

Author : Diya Lodha & Team
===========================================================
"""


import os


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



# ==========================================================
# Files To Remove
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
# Cleanup
# ==========================================================


def cleanup_synthetic_reference_files():


    print(
        "\nCleaning synthetic folder...\n"
    )


    for file in REFERENCE_FILES:


        file_path = os.path.join(
            SYNTHETIC_DIR,
            file
        )


        if os.path.exists(file_path):


            os.remove(
                file_path
            )


            print(
                f"Deleted : {file}"
            )


        else:


            print(
                f"Not Found : {file}"
            )


    print(
        "\nSynthetic cleanup completed."
    )



# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    cleanup_synthetic_reference_files()