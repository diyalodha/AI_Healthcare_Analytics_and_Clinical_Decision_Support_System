"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_reference_medications.py

Purpose :
Create ground-truth medication reference master data.

Output:
reference/medications_master.csv

Author : Diya Lodha & Team
===========================================================
"""

import os
import pandas as pd


# ==========================================================
# Paths
# ==========================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_DIR = os.path.dirname(
    CURRENT_DIR
)

REFERENCE_DIR = os.path.join(
    PROJECT_DIR,
    "reference"
)

os.makedirs(
    REFERENCE_DIR,
    exist_ok=True
)


# ==========================================================
# Ground Truth Medication Data
# ==========================================================

MEDICATIONS = [

{
"Medication_Name":"Metformin",
"Generic_Name":"Metformin Hydrochloride",
"Drug_Class":"Antidiabetic",
"Used_For":"Type 2 Diabetes Mellitus",
"Route":"Oral",
"Dosage_Form":"Tablet",
"Strength":"500 mg",
"Risk_Level":"Low"
},

{
"Medication_Name":"Insulin",
"Generic_Name":"Human Insulin",
"Drug_Class":"Antidiabetic",
"Used_For":"Diabetes Mellitus",
"Route":"Injection",
"Dosage_Form":"Injection",
"Strength":"100 IU/ml",
"Risk_Level":"High"
},

{
"Medication_Name":"Amlodipine",
"Generic_Name":"Amlodipine",
"Drug_Class":"Calcium Channel Blocker",
"Used_For":"Hypertension",
"Route":"Oral",
"Dosage_Form":"Tablet",
"Strength":"5 mg",
"Risk_Level":"Low"
},

{
"Medication_Name":"Losartan",
"Generic_Name":"Losartan Potassium",
"Drug_Class":"ARB",
"Used_For":"Hypertension",
"Route":"Oral",
"Dosage_Form":"Tablet",
"Strength":"50 mg",
"Risk_Level":"Low"
},

{
"Medication_Name":"Atorvastatin",
"Generic_Name":"Atorvastatin Calcium",
"Drug_Class":"Statin",
"Used_For":"High Cholesterol",
"Route":"Oral",
"Dosage_Form":"Tablet",
"Strength":"20 mg",
"Risk_Level":"Low"
},

{
"Medication_Name":"Aspirin",
"Generic_Name":"Acetylsalicylic Acid",
"Drug_Class":"Antiplatelet",
"Used_For":"Cardiovascular Disease",
"Route":"Oral",
"Dosage_Form":"Tablet",
"Strength":"75 mg",
"Risk_Level":"Medium"
},

{
"Medication_Name":"Salbutamol",
"Generic_Name":"Albuterol",
"Drug_Class":"Bronchodilator",
"Used_For":"Asthma",
"Route":"Inhalation",
"Dosage_Form":"Inhaler",
"Strength":"100 mcg",
"Risk_Level":"Medium"
},

{
"Medication_Name":"Budesonide",
"Generic_Name":"Budesonide",
"Drug_Class":"Corticosteroid",
"Used_For":"Respiratory Disease",
"Route":"Inhalation",
"Dosage_Form":"Inhaler",
"Strength":"200 mcg",
"Risk_Level":"Medium"
},

{
"Medication_Name":"Azithromycin",
"Generic_Name":"Azithromycin",
"Drug_Class":"Antibiotic",
"Used_For":"Bacterial Infection",
"Route":"Oral",
"Dosage_Form":"Tablet",
"Strength":"500 mg",
"Risk_Level":"Medium"
},

{
"Medication_Name":"Ceftriaxone",
"Generic_Name":"Ceftriaxone Sodium",
"Drug_Class":"Antibiotic",
"Used_For":"Severe Infection",
"Route":"Injection",
"Dosage_Form":"Injection",
"Strength":"1 g",
"Risk_Level":"High"
},

{
"Medication_Name":"Levetiracetam",
"Generic_Name":"Levetiracetam",
"Drug_Class":"Antiepileptic",
"Used_For":"Epilepsy",
"Route":"Oral",
"Dosage_Form":"Tablet",
"Strength":"500 mg",
"Risk_Level":"Medium"
},

{
"Medication_Name":"Furosemide",
"Generic_Name":"Furosemide",
"Drug_Class":"Diuretic",
"Used_For":"Heart Failure",
"Route":"Oral",
"Dosage_Form":"Tablet",
"Strength":"40 mg",
"Risk_Level":"Medium"
},

{
"Medication_Name":"Pantoprazole",
"Generic_Name":"Pantoprazole",
"Drug_Class":"Proton Pump Inhibitor",
"Used_For":"Acidity and Gastric Disorders",
"Route":"Oral",
"Dosage_Form":"Tablet",
"Strength":"40 mg",
"Risk_Level":"Low"
},

{
"Medication_Name":"Paracetamol",
"Generic_Name":"Acetaminophen",
"Drug_Class":"Analgesic",
"Used_For":"Pain and Fever",
"Route":"Oral",
"Dosage_Form":"Tablet",
"Strength":"650 mg",
"Risk_Level":"Low"
},

{
"Medication_Name":"Ondansetron",
"Generic_Name":"Ondansetron",
"Drug_Class":"Antiemetic",
"Used_For":"Nausea and Vomiting",
"Route":"Oral",
"Dosage_Form":"Tablet",
"Strength":"4 mg",
"Risk_Level":"Low"
}

]


# ==========================================================
# Generate Reference Medications
# ==========================================================

def generate_reference_medications():

    base = pd.DataFrame(
        MEDICATIONS
    )

    expanded = []

    counter = 1

    while len(expanded) < 500:

        for _, row in base.iterrows():

            if len(expanded) >= 500:
                break

            new_row = row.copy()

            new_row["Medication_Name"] = (
                row["Medication_Name"]
                + " "
                + str(counter)
            )

            expanded.append(
                new_row
            )

            counter += 1

    medications = pd.DataFrame(
        expanded
    )

    output = os.path.join(
        REFERENCE_DIR,
        "medications_master.csv"
    )

    medications.to_csv(
        output,
        index=False
    )

    print(
        "======================================="
    )

    print(
        "Created medications_master.csv"
    )

    print(
        f"Generated {len(medications)} medication references."
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

    generate_reference_medications()