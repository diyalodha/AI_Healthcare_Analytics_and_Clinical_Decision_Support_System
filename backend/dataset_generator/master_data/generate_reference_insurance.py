"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_reference_insurance.py

Purpose :
Create ground-truth insurance provider master data.

Output:
reference/insurance_master.csv

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
# Ground Truth Insurance Providers
# ==========================================================


INSURANCE_PROVIDERS = [

{
"Provider_Name":"Star Health Insurance",
"Provider_Type":"Private",
"Coverage_Type":"Health Insurance",
"Network_Size":14000,
"Claim_Ratio":95.2
},

{
"Provider_Name":"HDFC ERGO Health Insurance",
"Provider_Type":"Private",
"Coverage_Type":"Health Insurance",
"Network_Size":12000,
"Claim_Ratio":92.5
},

{
"Provider_Name":"ICICI Lombard Health Insurance",
"Provider_Type":"Private",
"Coverage_Type":"Health Insurance",
"Network_Size":10000,
"Claim_Ratio":91.8
},

{
"Provider_Name":"Bajaj Allianz Health Insurance",
"Provider_Type":"Private",
"Coverage_Type":"Health Insurance",
"Network_Size":11000,
"Claim_Ratio":93.4
},

{
"Provider_Name":"Niva Bupa Health Insurance",
"Provider_Type":"Private",
"Coverage_Type":"Health Insurance",
"Network_Size":9000,
"Claim_Ratio":94.1
},

{
"Provider_Name":"Care Health Insurance",
"Provider_Type":"Private",
"Coverage_Type":"Health Insurance",
"Network_Size":9500,
"Claim_Ratio":93.9
},

{
"Provider_Name":"Aditya Birla Health Insurance",
"Provider_Type":"Private",
"Coverage_Type":"Health Insurance",
"Network_Size":8000,
"Claim_Ratio":91.2
},

{
"Provider_Name":"Government Health Scheme",
"Provider_Type":"Government",
"Coverage_Type":"Public Healthcare",
"Network_Size":20000,
"Claim_Ratio":98.0
},

{
"Provider_Name":"Ayushman Bharat",
"Provider_Type":"Government",
"Coverage_Type":"Public Healthcare",
"Network_Size":25000,
"Claim_Ratio":97.5
},

{
"Provider_Name":"Employee State Insurance",
"Provider_Type":"Government",
"Coverage_Type":"Employee Healthcare",
"Network_Size":15000,
"Claim_Ratio":96.8
}

]



# ==========================================================
# Expand to 100 Providers
# ==========================================================


base = pd.DataFrame(
    INSURANCE_PROVIDERS
)


expanded = []


counter = 1


while len(expanded) < 100:


    for _, row in base.iterrows():


        if len(expanded) >= 100:
            break


        new_row = row.copy()


        new_row["Provider_Name"] = (
            row["Provider_Name"]
            +
            " - Branch "
            +
            str(counter)
        )


        expanded.append(
            new_row
        )


        counter += 1



insurance = pd.DataFrame(
    expanded
)



# ==========================================================
# Save
# ==========================================================


output = os.path.join(
    REFERENCE_DIR,
    "insurance_master.csv"
)


insurance.to_csv(
    output,
    index=False
)


print(
    "Created insurance_master.csv"
)


print(
    "Total providers:",
    len(insurance)
)