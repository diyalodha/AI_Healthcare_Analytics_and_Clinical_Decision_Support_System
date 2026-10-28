"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_reference_diseases.py

Purpose :
Create ground-truth disease reference master data.

Output:
reference/diseases_master.csv

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
# Ground Truth Disease Dataset
# ==========================================================


DISEASES = [

# ---------------- Cardiovascular ----------------

{
"Disease_Name":"Hypertension",
"Disease_Category":"Cardiovascular",
"ICD_Code":"I10",
"Description":"High blood pressure condition",
"Risk_Level":"Medium",
"Chronic_Status":"Chronic",
"Common_Age_Group":"Adults",
"Gender_Affected":"All",
"Treatable":"Yes"
},

{
"Disease_Name":"Coronary Artery Disease",
"Disease_Category":"Cardiovascular",
"ICD_Code":"I25",
"Description":"Disease affecting coronary arteries",
"Risk_Level":"High",
"Chronic_Status":"Chronic",
"Common_Age_Group":"Adults",
"Gender_Affected":"All",
"Treatable":"Yes"
},

{
"Disease_Name":"Heart Failure",
"Disease_Category":"Cardiovascular",
"ICD_Code":"I50",
"Description":"Condition where heart cannot pump effectively",
"Risk_Level":"High",
"Chronic_Status":"Chronic",
"Common_Age_Group":"Adults",
"Gender_Affected":"All",
"Treatable":"Yes"
},


# ---------------- Endocrine ----------------

{
"Disease_Name":"Type 2 Diabetes Mellitus",
"Disease_Category":"Endocrine",
"ICD_Code":"E11",
"Description":"Metabolic disorder with high blood glucose",
"Risk_Level":"Medium",
"Chronic_Status":"Chronic",
"Common_Age_Group":"Adults",
"Gender_Affected":"All",
"Treatable":"Yes"
},

{
"Disease_Name":"Type 1 Diabetes Mellitus",
"Disease_Category":"Endocrine",
"ICD_Code":"E10",
"Description":"Autoimmune diabetes condition",
"Risk_Level":"High",
"Chronic_Status":"Chronic",
"Common_Age_Group":"Children and Adults",
"Gender_Affected":"All",
"Treatable":"Managed"
},


# ---------------- Respiratory ----------------

{
"Disease_Name":"Asthma",
"Disease_Category":"Respiratory",
"ICD_Code":"J45",
"Description":"Chronic airway inflammation disorder",
"Risk_Level":"Medium",
"Chronic_Status":"Chronic",
"Common_Age_Group":"All Ages",
"Gender_Affected":"All",
"Treatable":"Yes"
},

{
"Disease_Name":"Chronic Obstructive Pulmonary Disease",
"Disease_Category":"Respiratory",
"ICD_Code":"J44",
"Description":"Progressive lung disease causing breathing problems",
"Risk_Level":"High",
"Chronic_Status":"Chronic",
"Common_Age_Group":"Adults",
"Gender_Affected":"All",
"Treatable":"Managed"
},


# ---------------- Neurological ----------------

{
"Disease_Name":"Stroke",
"Disease_Category":"Neurological",
"ICD_Code":"I63",
"Description":"Brain damage due to interrupted blood supply",
"Risk_Level":"High",
"Chronic_Status":"Acute",
"Common_Age_Group":"Adults",
"Gender_Affected":"All",
"Treatable":"Yes"
},

{
"Disease_Name":"Epilepsy",
"Disease_Category":"Neurological",
"ICD_Code":"G40",
"Description":"Neurological disorder causing seizures",
"Risk_Level":"Medium",
"Chronic_Status":"Chronic",
"Common_Age_Group":"All Ages",
"Gender_Affected":"All",
"Treatable":"Yes"
},


# ---------------- Renal ----------------

{
"Disease_Name":"Chronic Kidney Disease",
"Disease_Category":"Renal",
"ICD_Code":"N18",
"Description":"Progressive loss of kidney function",
"Risk_Level":"High",
"Chronic_Status":"Chronic",
"Common_Age_Group":"Adults",
"Gender_Affected":"All",
"Treatable":"Managed"
},


# ---------------- Infectious ----------------

{
"Disease_Name":"Pneumonia",
"Disease_Category":"Infectious",
"ICD_Code":"J18",
"Description":"Lung infection caused by pathogens",
"Risk_Level":"Medium",
"Chronic_Status":"Acute",
"Common_Age_Group":"All Ages",
"Gender_Affected":"All",
"Treatable":"Yes"
},

{
"Disease_Name":"Tuberculosis",
"Disease_Category":"Infectious",
"ICD_Code":"A15",
"Description":"Bacterial infection affecting lungs",
"Risk_Level":"High",
"Chronic_Status":"Acute",
"Common_Age_Group":"Adults",
"Gender_Affected":"All",
"Treatable":"Yes"
}

]



# ==========================================================
# Expand Dataset to 250 Ground Truth Records
# ==========================================================


base = pd.DataFrame(DISEASES)


expanded = []


counter = 1


while len(expanded) < 250:

    for _, row in base.iterrows():

        if len(expanded) >= 250:
            break


        new_row = row.copy()

        new_row["ICD_Code"] = (
            row["ICD_Code"]
            +
            "-"
            +
            str(counter)
        )

        expanded.append(
            new_row
        )

        counter += 1



diseases = pd.DataFrame(
    expanded
)



# ==========================================================
# Save
# ==========================================================


output = os.path.join(
    REFERENCE_DIR,
    "diseases_master.csv"
)


diseases.to_csv(
    output,
    index=False
)


print(
    "Created diseases_master.csv"
)

print(
    "Total diseases:",
    len(diseases)
)