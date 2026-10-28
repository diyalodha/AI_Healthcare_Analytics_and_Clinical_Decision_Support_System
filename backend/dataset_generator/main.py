"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : main.py

Purpose :
Run complete synthetic healthcare dataset generation pipeline.

Author : Diya Lodha & Team
===========================================================
"""


import os
import sys
import time



# ==========================================================
# Add generator folder
# ==========================================================


CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


GENERATORS_DIR = os.path.join(
    CURRENT_DIR,
    "generators"
)


sys.path.append(
    GENERATORS_DIR
)



# ==========================================================
# Import Generators
# ==========================================================


from generate_departments import generate_departments

from generate_doctors import generate_doctors

from generate_diseases import generate_diseases

from generate_medications import generate_medications

from generate_insurance_providers import generate_insurance_providers

from generate_patients import generate_patients

from generate_admissions import generate_admissions

from generate_diagnoses import generate_diagnoses

from generate_vital_signs import generate_vital_signs

from generate_lab_results import generate_lab_results

from generate_prescriptions import generate_prescriptions

from generate_clinical_notes import generate_clinical_notes

from generate_hospital_rooms import generate_hospital_rooms

from generate_beds import generate_beds

from generate_icu_stays import generate_icu_stays

from generate_discharge_summary import generate_discharge_summary

from generate_imaging_reports import generate_imaging_reports

from generate_medical_images_metadata import generate_medical_images_metadata

from generate_ai_predictions import generate_ai_predictions

from generate_health_scores import generate_health_scores

from generate_ai_recommendations import generate_ai_recommendations

from generate_explainable_ai import generate_explainable_ai



# ==========================================================
# Pipeline Runner
# ==========================================================


def run_pipeline():


    start_time = time.time()


    print("\n")
    print("="*70)
    print("AI HEALTHCARE SYNTHETIC DATA GENERATION STARTED")
    print("="*70)



    generators = [


        ("Departments",
         generate_departments),


        ("Doctors",
         generate_doctors),


        ("Diseases",
         generate_diseases),


        ("Medications",
         generate_medications),


        ("Insurance Providers",
         generate_insurance_providers),


        ("Patients",
         generate_patients),


        ("Admissions",
         generate_admissions),


        ("Diagnoses",
         generate_diagnoses),


        ("Vital Signs",
         generate_vital_signs),


        ("Lab Results",
         generate_lab_results),


        ("Prescriptions",
         generate_prescriptions),


        ("Clinical Notes",
         generate_clinical_notes),


        ("Hospital Rooms",
         generate_hospital_rooms),


        ("Beds",
         generate_beds),


        ("ICU Stays",
         generate_icu_stays),


        ("Discharge Summary",
         generate_discharge_summary),


        ("Imaging Reports",
         generate_imaging_reports),


        ("Medical Images Metadata",
         generate_medical_images_metadata),


        ("AI Predictions",
         generate_ai_predictions),


        ("Health Scores",
         generate_health_scores),


        ("AI Recommendations",
         generate_ai_recommendations),


        ("Explainable AI",
         generate_explainable_ai)

    ]



    for name, function in generators:


        print("\n")
        print("-"*70)
        print(
            f"Running : {name}"
        )
        print("-"*70)



        try:

            function()


        except Exception as error:

            print(
                f"ERROR in {name}"
            )

            print(error)

            break



    end_time = time.time()


    print("\n")
    print("="*70)

    print(
        "DATA GENERATION COMPLETED"
    )


    print(
        "Total Time:",
        round(
            (end_time-start_time)/60,
            2
        ),
        "minutes"
    )

    print("="*70)



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    run_pipeline()