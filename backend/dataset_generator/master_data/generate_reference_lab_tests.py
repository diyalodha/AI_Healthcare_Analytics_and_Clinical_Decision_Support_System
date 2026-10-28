"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_reference_lab_tests.py

Purpose :
Generate reference dataset for laboratory tests.

Output :
reference_lab_tests.csv

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


from utils import save_reference_dataframe


# ==========================================================
# Laboratory Test Reference Data
# ==========================================================

LAB_TESTS = [

    {
        "Lab_Test_Code":"LT001",
        "Lab_Test_Name":"Complete Blood Count",
        "Category":"Hematology",
        "Specimen":"Blood",
        "Unit":"Cells/uL",
        "Normal_Range":"Normal",
        "Department":"Pathology"
    },

    {
        "Lab_Test_Code":"LT002",
        "Lab_Test_Name":"Blood Glucose",
        "Category":"Biochemistry",
        "Specimen":"Blood",
        "Unit":"mg/dL",
        "Normal_Range":"70-110",
        "Department":"Biochemistry"
    },

    {
        "Lab_Test_Code":"LT003",
        "Lab_Test_Name":"HbA1c",
        "Category":"Diabetes",
        "Specimen":"Blood",
        "Unit":"%",
        "Normal_Range":"4.0-5.6",
        "Department":"Biochemistry"
    },

    {
        "Lab_Test_Code":"LT004",
        "Lab_Test_Name":"Serum Creatinine",
        "Category":"Kidney",
        "Specimen":"Blood",
        "Unit":"mg/dL",
        "Normal_Range":"0.7-1.3",
        "Department":"Biochemistry"
    },

    {
        "Lab_Test_Code":"LT005",
        "Lab_Test_Name":"Blood Urea Nitrogen",
        "Category":"Kidney",
        "Specimen":"Blood",
        "Unit":"mg/dL",
        "Normal_Range":"7-20",
        "Department":"Biochemistry"
    },

    {
        "Lab_Test_Code":"LT006",
        "Lab_Test_Name":"Serum Sodium",
        "Category":"Electrolytes",
        "Specimen":"Blood",
        "Unit":"mmol/L",
        "Normal_Range":"135-145",
        "Department":"Biochemistry"
    },

    {
        "Lab_Test_Code":"LT007",
        "Lab_Test_Name":"Serum Potassium",
        "Category":"Electrolytes",
        "Specimen":"Blood",
        "Unit":"mmol/L",
        "Normal_Range":"3.5-5.1",
        "Department":"Biochemistry"
    },

    {
        "Lab_Test_Code":"LT008",
        "Lab_Test_Name":"Serum Calcium",
        "Category":"Electrolytes",
        "Specimen":"Blood",
        "Unit":"mg/dL",
        "Normal_Range":"8.5-10.5",
        "Department":"Biochemistry"
    },

    {
        "Lab_Test_Code":"LT009",
        "Lab_Test_Name":"Liver Function Test",
        "Category":"Liver",
        "Specimen":"Blood",
        "Unit":"IU/L",
        "Normal_Range":"Normal",
        "Department":"Biochemistry"
    },

    {
        "Lab_Test_Code":"LT010",
        "Lab_Test_Name":"Lipid Profile",
        "Category":"Cardiology",
        "Specimen":"Blood",
        "Unit":"mg/dL",
        "Normal_Range":"Normal",
        "Department":"Biochemistry"
    },

    {
        "Lab_Test_Code":"LT011",
        "Lab_Test_Name":"Troponin I",
        "Category":"Cardiology",
        "Specimen":"Blood",
        "Unit":"ng/mL",
        "Normal_Range":"<0.04",
        "Department":"Cardiology"
    },

    {
        "Lab_Test_Code":"LT012",
        "Lab_Test_Name":"D-Dimer",
        "Category":"Coagulation",
        "Specimen":"Blood",
        "Unit":"ng/mL",
        "Normal_Range":"<500",
        "Department":"Pathology"
    },

    {
        "Lab_Test_Code":"LT013",
        "Lab_Test_Name":"C-Reactive Protein",
        "Category":"Inflammation",
        "Specimen":"Blood",
        "Unit":"mg/L",
        "Normal_Range":"<5",
        "Department":"Pathology"
    },

    {
        "Lab_Test_Code":"LT014",
        "Lab_Test_Name":"Urine Routine Examination",
        "Category":"Urinalysis",
        "Specimen":"Urine",
        "Unit":"N/A",
        "Normal_Range":"Normal",
        "Department":"Pathology"
    },

    {
        "Lab_Test_Code":"LT015",
        "Lab_Test_Name":"Thyroid Profile",
        "Category":"Endocrinology",
        "Specimen":"Blood",
        "Unit":"uIU/mL",
        "Normal_Range":"Normal",
        "Department":"Endocrinology"
    },

    {
        "Lab_Test_Code":"LT016",
        "Lab_Test_Name":"Vitamin D",
        "Category":"Nutrition",
        "Specimen":"Blood",
        "Unit":"ng/mL",
        "Normal_Range":"30-100",
        "Department":"Biochemistry"
    },

    {
        "Lab_Test_Code":"LT017",
        "Lab_Test_Name":"Vitamin B12",
        "Category":"Nutrition",
        "Specimen":"Blood",
        "Unit":"pg/mL",
        "Normal_Range":"200-900",
        "Department":"Biochemistry"
    },

    {
        "Lab_Test_Code":"LT018",
        "Lab_Test_Name":"COVID-19 RT-PCR",
        "Category":"Virology",
        "Specimen":"Nasopharyngeal Swab",
        "Unit":"N/A",
        "Normal_Range":"Negative",
        "Department":"Microbiology"
    },

    {
        "Lab_Test_Code":"LT019",
        "Lab_Test_Name":"Blood Culture",
        "Category":"Microbiology",
        "Specimen":"Blood",
        "Unit":"N/A",
        "Normal_Range":"No Growth",
        "Department":"Microbiology"
    },

    {
        "Lab_Test_Code":"LT020",
        "Lab_Test_Name":"Pregnancy Test (hCG)",
        "Category":"Obstetrics",
        "Specimen":"Urine",
        "Unit":"N/A",
        "Normal_Range":"Negative",
        "Department":"Gynecology"
    }

]


# ==========================================================
# Generate Dataset
# ==========================================================

def generate_reference_lab_tests():

    dataframe = pd.DataFrame(
        LAB_TESTS
    )

    save_reference_dataframe(
        dataframe,
        "reference_lab_tests.csv"
    )

    print(
        "======================================="
    )

    print(
        f"Generated {len(dataframe)} laboratory test references."
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

    generate_reference_lab_tests()