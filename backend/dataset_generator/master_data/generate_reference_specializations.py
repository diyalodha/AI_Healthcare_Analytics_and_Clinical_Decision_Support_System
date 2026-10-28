"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_reference_specializations.py

Purpose :
Generate reference dataset for medical specializations.

Output :
reference_specializations.csv

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
# Medical Specializations
# ==========================================================

SPECIALIZATIONS = [

    {"Specialization_Code":"SP001","Specialization_Name":"General Medicine","Department":"General Medicine"},
    {"Specialization_Code":"SP002","Specialization_Name":"Cardiology","Department":"Cardiology"},
    {"Specialization_Code":"SP003","Specialization_Name":"Neurology","Department":"Neurology"},
    {"Specialization_Code":"SP004","Specialization_Name":"Neurosurgery","Department":"Neurology"},
    {"Specialization_Code":"SP005","Specialization_Name":"Orthopedics","Department":"Orthopedics"},
    {"Specialization_Code":"SP006","Specialization_Name":"Pediatrics","Department":"Pediatrics"},
    {"Specialization_Code":"SP007","Specialization_Name":"Dermatology","Department":"Dermatology"},
    {"Specialization_Code":"SP008","Specialization_Name":"Psychiatry","Department":"Psychiatry"},
    {"Specialization_Code":"SP009","Specialization_Name":"Clinical Psychology","Department":"Psychiatry"},
    {"Specialization_Code":"SP010","Specialization_Name":"Gynecology","Department":"Gynecology"},
    {"Specialization_Code":"SP011","Specialization_Name":"Obstetrics","Department":"Gynecology"},
    {"Specialization_Code":"SP012","Specialization_Name":"Ophthalmology","Department":"Ophthalmology"},
    {"Specialization_Code":"SP013","Specialization_Name":"ENT","Department":"ENT"},
    {"Specialization_Code":"SP014","Specialization_Name":"Pulmonology","Department":"Pulmonology"},
    {"Specialization_Code":"SP015","Specialization_Name":"Nephrology","Department":"Nephrology"},
    {"Specialization_Code":"SP016","Specialization_Name":"Urology","Department":"Urology"},
    {"Specialization_Code":"SP017","Specialization_Name":"Gastroenterology","Department":"Gastroenterology"},
    {"Specialization_Code":"SP018","Specialization_Name":"Endocrinology","Department":"Endocrinology"},
    {"Specialization_Code":"SP019","Specialization_Name":"Oncology","Department":"Oncology"},
    {"Specialization_Code":"SP020","Specialization_Name":"Radiation Oncology","Department":"Oncology"},
    {"Specialization_Code":"SP021","Specialization_Name":"Radiology","Department":"Radiology"},
    {"Specialization_Code":"SP022","Specialization_Name":"Interventional Radiology","Department":"Radiology"},
    {"Specialization_Code":"SP023","Specialization_Name":"Pathology","Department":"Pathology"},
    {"Specialization_Code":"SP024","Specialization_Name":"Microbiology","Department":"Pathology"},
    {"Specialization_Code":"SP025","Specialization_Name":"Anesthesiology","Department":"Anesthesiology"},
    {"Specialization_Code":"SP026","Specialization_Name":"Emergency Medicine","Department":"Emergency"},
    {"Specialization_Code":"SP027","Specialization_Name":"Critical Care","Department":"ICU"},
    {"Specialization_Code":"SP028","Specialization_Name":"Trauma Surgery","Department":"Emergency"},
    {"Specialization_Code":"SP029","Specialization_Name":"Plastic Surgery","Department":"Surgery"},
    {"Specialization_Code":"SP030","Specialization_Name":"General Surgery","Department":"Surgery"},
    {"Specialization_Code":"SP031","Specialization_Name":"Cardiothoracic Surgery","Department":"Cardiology"},
    {"Specialization_Code":"SP032","Specialization_Name":"Vascular Surgery","Department":"Surgery"},
    {"Specialization_Code":"SP033","Specialization_Name":"Pediatric Surgery","Department":"Pediatrics"},
    {"Specialization_Code":"SP034","Specialization_Name":"Sports Medicine","Department":"Orthopedics"},
    {"Specialization_Code":"SP035","Specialization_Name":"Rheumatology","Department":"Rheumatology"},
    {"Specialization_Code":"SP036","Specialization_Name":"Immunology","Department":"Immunology"},
    {"Specialization_Code":"SP037","Specialization_Name":"Allergy Medicine","Department":"Immunology"},
    {"Specialization_Code":"SP038","Specialization_Name":"Infectious Diseases","Department":"Infectious Diseases"},
    {"Specialization_Code":"SP039","Specialization_Name":"Nuclear Medicine","Department":"Radiology"},
    {"Specialization_Code":"SP040","Specialization_Name":"Sleep Medicine","Department":"Pulmonology"},
    {"Specialization_Code":"SP041","Specialization_Name":"Pain Medicine","Department":"Anesthesiology"},
    {"Specialization_Code":"SP042","Specialization_Name":"Rehabilitation Medicine","Department":"Rehabilitation"},
    {"Specialization_Code":"SP043","Specialization_Name":"Physiotherapy","Department":"Rehabilitation"},
    {"Specialization_Code":"SP044","Specialization_Name":"Occupational Therapy","Department":"Rehabilitation"},
    {"Specialization_Code":"SP045","Specialization_Name":"Speech Therapy","Department":"Rehabilitation"},
    {"Specialization_Code":"SP046","Specialization_Name":"Dentistry","Department":"Dental"},
    {"Specialization_Code":"SP047","Specialization_Name":"Oral Surgery","Department":"Dental"},
    {"Specialization_Code":"SP048","Specialization_Name":"Periodontics","Department":"Dental"},
    {"Specialization_Code":"SP049","Specialization_Name":"Orthodontics","Department":"Dental"},
    {"Specialization_Code":"SP050","Specialization_Name":"Public Health","Department":"Community Medicine"},
    {"Specialization_Code":"SP051","Specialization_Name":"Community Medicine","Department":"Community Medicine"},
    {"Specialization_Code":"SP052","Specialization_Name":"Preventive Medicine","Department":"Community Medicine"},
    {"Specialization_Code":"SP053","Specialization_Name":"Forensic Medicine","Department":"Forensic Medicine"},
    {"Specialization_Code":"SP054","Specialization_Name":"Medical Genetics","Department":"Genetics"},
    {"Specialization_Code":"SP055","Specialization_Name":"Geriatrics","Department":"General Medicine"},
    {"Specialization_Code":"SP056","Specialization_Name":"Adolescent Medicine","Department":"Pediatrics"},
    {"Specialization_Code":"SP057","Specialization_Name":"Palliative Care","Department":"Oncology"},
    {"Specialization_Code":"SP058","Specialization_Name":"Diabetology","Department":"Endocrinology"},
    {"Specialization_Code":"SP059","Specialization_Name":"Clinical Pharmacology","Department":"Pharmacy"},
    {"Specialization_Code":"SP060","Specialization_Name":"Transfusion Medicine","Department":"Blood Bank"}

]


# ==========================================================
# Generate Dataset
# ==========================================================

def generate_reference_specializations():

    dataframe = pd.DataFrame(
        SPECIALIZATIONS
    )

    save_reference_dataframe(
        dataframe,
        "reference_specializations.csv"
    )

    print(
        "======================================="
    )

    print(
        f"Generated {len(dataframe)} specialization references."
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

    generate_reference_specializations()