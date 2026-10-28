"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_reference_diagnosis_codes.py

Purpose :
Generate ICD-10 inspired diagnosis reference dataset.

Output :
reference_diagnosis_codes.csv

Author : Diya Lodha & Team
===========================================================
"""

import os
import sys
import pandas as pd


# ==========================================================
# Add Parent Directory
# ==========================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

import config


# ==========================================================
# Diagnosis Data
# ==========================================================

DIAGNOSIS_DATA = [

# ----------------------------------------------------------
# Cardiology
# ----------------------------------------------------------

("Cardiology","Hypertension","Medium"),
("Cardiology","Essential Hypertension","Medium"),
("Cardiology","Secondary Hypertension","High"),
("Cardiology","Coronary Artery Disease","High"),
("Cardiology","Acute Myocardial Infarction","Critical"),
("Cardiology","Old Myocardial Infarction","High"),
("Cardiology","Heart Failure","Critical"),
("Cardiology","Congestive Heart Failure","Critical"),
("Cardiology","Cardiomyopathy","High"),
("Cardiology","Atrial Fibrillation","High"),
("Cardiology","Bradycardia","Medium"),
("Cardiology","Tachycardia","Medium"),
("Cardiology","Heart Block","High"),
("Cardiology","Mitral Valve Disease","Medium"),
("Cardiology","Aortic Stenosis","High"),
("Cardiology","Pulmonary Hypertension","High"),
("Cardiology","Peripheral Artery Disease","Medium"),
("Cardiology","Deep Vein Thrombosis","High"),
("Cardiology","Hyperlipidemia","Medium"),
("Cardiology","Stable Angina","Medium"),


# ----------------------------------------------------------
# Neurology
# ----------------------------------------------------------

("Neurology","Stroke","Critical"),
("Neurology","Transient Ischemic Attack","High"),
("Neurology","Epilepsy","High"),
("Neurology","Migraine","Medium"),
("Neurology","Parkinson Disease","High"),
("Neurology","Alzheimer Disease","High"),
("Neurology","Dementia","High"),
("Neurology","Multiple Sclerosis","High"),
("Neurology","Bell Palsy","Medium"),
("Neurology","Peripheral Neuropathy","Medium"),
("Neurology","Brain Tumor","Critical"),
("Neurology","Meningitis","Critical"),
("Neurology","Encephalitis","Critical"),
("Neurology","Vertigo","Low"),
("Neurology","Cluster Headache","Medium"),
("Neurology","Trigeminal Neuralgia","Medium"),
("Neurology","Guillain Barre Syndrome","Critical"),
("Neurology","Cerebral Edema","Critical"),
("Neurology","Subarachnoid Hemorrhage","Critical"),
("Neurology","Intracerebral Hemorrhage","Critical"),


# ----------------------------------------------------------
# Pulmonology
# ----------------------------------------------------------

("Pulmonology","Asthma","Medium"),
("Pulmonology","Bronchial Asthma","Medium"),
("Pulmonology","COPD","High"),
("Pulmonology","Pneumonia","High"),
("Pulmonology","COVID-19","High"),
("Pulmonology","Tuberculosis","High"),
("Pulmonology","Pleural Effusion","High"),
("Pulmonology","Pulmonary Embolism","Critical"),
("Pulmonology","Pulmonary Fibrosis","High"),
("Pulmonology","Acute Respiratory Failure","Critical"),
("Pulmonology","Sleep Apnea","Medium"),
("Pulmonology","Acute Bronchitis","Low"),
("Pulmonology","Chronic Bronchitis","Medium"),
("Pulmonology","Lung Cancer","Critical"),
("Pulmonology","Interstitial Lung Disease","High"),
("Pulmonology","Pneumothorax","Critical"),
("Pulmonology","Hemoptysis","High"),
("Pulmonology","Respiratory Syncytial Virus Infection","Medium"),
("Pulmonology","Influenza","Medium"),
("Pulmonology","Empyema","High"),


# ----------------------------------------------------------
# Endocrinology
# ----------------------------------------------------------

("Endocrinology","Type 1 Diabetes Mellitus","High"),
("Endocrinology","Type 2 Diabetes Mellitus","High"),
("Endocrinology","Diabetic Ketoacidosis","Critical"),
("Endocrinology","Hypoglycemia","Medium"),
("Endocrinology","Hyperglycemia","Medium"),
("Endocrinology","Hypothyroidism","Medium"),
("Endocrinology","Hyperthyroidism","Medium"),
("Endocrinology","Goiter","Low"),
("Endocrinology","Cushing Syndrome","High"),
("Endocrinology","Addison Disease","High"),
("Endocrinology","Acromegaly","High"),
("Endocrinology","Pituitary Adenoma","High"),
("Endocrinology","Hyperparathyroidism","Medium"),
("Endocrinology","Hypoparathyroidism","Medium"),
("Endocrinology","Obesity","Medium"),
("Endocrinology","Metabolic Syndrome","Medium"),
("Endocrinology","Vitamin D Deficiency","Low"),
("Endocrinology","Osteoporosis","Medium"),
("Endocrinology","Gestational Diabetes","High"),
("Endocrinology","Insulin Resistance","Medium"),


# ----------------------------------------------------------
# Gastroenterology
# ----------------------------------------------------------

("Gastroenterology","GERD","Low"),
("Gastroenterology","Gastritis","Low"),
("Gastroenterology","Peptic Ulcer Disease","Medium"),
("Gastroenterology","Acute Pancreatitis","High"),
("Gastroenterology","Chronic Pancreatitis","High"),
("Gastroenterology","Hepatitis B","High"),
("Gastroenterology","Hepatitis C","High"),
("Gastroenterology","Liver Cirrhosis","Critical"),
("Gastroenterology","Fatty Liver Disease","Medium"),
("Gastroenterology","Gallstones","Medium"),
("Gastroenterology","Acute Cholecystitis","High"),
("Gastroenterology","Appendicitis","High"),
("Gastroenterology","Crohn Disease","High"),
("Gastroenterology","Ulcerative Colitis","High"),
("Gastroenterology","Irritable Bowel Syndrome","Low"),
("Gastroenterology","Constipation","Low"),
("Gastroenterology","Diarrhea","Low"),
("Gastroenterology","Hemorrhoids","Low"),
("Gastroenterology","Colon Cancer","Critical"),
("Gastroenterology","Rectal Bleeding","High"),
# ----------------------------------------------------------
# Nephrology
# ----------------------------------------------------------

("Nephrology","Acute Kidney Injury","Critical"),
("Nephrology","Chronic Kidney Disease Stage 1","Medium"),
("Nephrology","Chronic Kidney Disease Stage 2","Medium"),
("Nephrology","Chronic Kidney Disease Stage 3","High"),
("Nephrology","Chronic Kidney Disease Stage 4","High"),
("Nephrology","Chronic Kidney Disease Stage 5","Critical"),
("Nephrology","End Stage Renal Disease","Critical"),
("Nephrology","Nephrotic Syndrome","High"),
("Nephrology","Nephritic Syndrome","High"),
("Nephrology","Glomerulonephritis","High"),
("Nephrology","Pyelonephritis","Medium"),
("Nephrology","Urinary Tract Infection","Low"),
("Nephrology","Kidney Stones","Medium"),
("Nephrology","Hydronephrosis","Medium"),
("Nephrology","Renal Failure","Critical"),
("Nephrology","Polycystic Kidney Disease","High"),
("Nephrology","Proteinuria","Medium"),
("Nephrology","Hematuria","Medium"),
("Nephrology","Electrolyte Imbalance","Medium"),
("Nephrology","Hyperkalemia","Critical"),


# ----------------------------------------------------------
# Orthopedics
# ----------------------------------------------------------

("Orthopedics","Osteoarthritis","Medium"),
("Orthopedics","Rheumatoid Arthritis","High"),
("Orthopedics","Osteoporosis","Medium"),
("Orthopedics","Fracture Femur","High"),
("Orthopedics","Fracture Tibia","High"),
("Orthopedics","Fracture Radius","Medium"),
("Orthopedics","Shoulder Dislocation","Medium"),
("Orthopedics","ACL Tear","Medium"),
("Orthopedics","Meniscus Tear","Medium"),
("Orthopedics","Scoliosis","Medium"),
("Orthopedics","Spinal Stenosis","High"),
("Orthopedics","Cervical Spondylosis","Medium"),
("Orthopedics","Lumbar Disc Herniation","High"),
("Orthopedics","Frozen Shoulder","Low"),
("Orthopedics","Tennis Elbow","Low"),
("Orthopedics","Carpal Tunnel Syndrome","Medium"),
("Orthopedics","Bone Tumor","Critical"),
("Orthopedics","Hip Fracture","High"),
("Orthopedics","Pelvic Fracture","Critical"),
("Orthopedics","Ankle Sprain","Low"),


# ----------------------------------------------------------
# Dermatology
# ----------------------------------------------------------

("Dermatology","Psoriasis","Medium"),
("Dermatology","Eczema","Low"),
("Dermatology","Acne Vulgaris","Low"),
("Dermatology","Vitiligo","Low"),
("Dermatology","Melanoma","Critical"),
("Dermatology","Basal Cell Carcinoma","Medium"),
("Dermatology","Squamous Cell Carcinoma","High"),
("Dermatology","Cellulitis","High"),
("Dermatology","Fungal Infection","Low"),
("Dermatology","Urticaria","Low"),
("Dermatology","Contact Dermatitis","Low"),
("Dermatology","Herpes Zoster","Medium"),
("Dermatology","Scabies","Low"),
("Dermatology","Ringworm","Low"),
("Dermatology","Alopecia","Low"),
("Dermatology","Impetigo","Low"),
("Dermatology","Rosacea","Low"),
("Dermatology","Skin Abscess","Medium"),
("Dermatology","Drug Rash","Medium"),
("Dermatology","Pressure Ulcer","Medium"),


# ----------------------------------------------------------
# Ophthalmology
# ----------------------------------------------------------

("Ophthalmology","Cataract","Medium"),
("Ophthalmology","Glaucoma","High"),
("Ophthalmology","Diabetic Retinopathy","High"),
("Ophthalmology","Retinal Detachment","Critical"),
("Ophthalmology","Conjunctivitis","Low"),
("Ophthalmology","Corneal Ulcer","High"),
("Ophthalmology","Dry Eye Syndrome","Low"),
("Ophthalmology","Macular Degeneration","High"),
("Ophthalmology","Optic Neuritis","High"),
("Ophthalmology","Eye Trauma","High"),
("Ophthalmology","Myopia","Low"),
("Ophthalmology","Hypermetropia","Low"),
("Ophthalmology","Astigmatism","Low"),
("Ophthalmology","Color Blindness","Low"),
("Ophthalmology","Uveitis","Medium"),


# ----------------------------------------------------------
# ENT
# ----------------------------------------------------------

("ENT","Otitis Media","Low"),
("ENT","Otitis Externa","Low"),
("ENT","Sinusitis","Low"),
("ENT","Tonsillitis","Low"),
("ENT","Pharyngitis","Low"),
("ENT","Laryngitis","Low"),
("ENT","Deviated Nasal Septum","Medium"),
("ENT","Hearing Loss","Medium"),
("ENT","Vertigo","Medium"),
("ENT","Mastoiditis","High"),
("ENT","Nasal Polyps","Medium"),
("ENT","Epistaxis","Medium"),
("ENT","Cholesteatoma","High"),
("ENT","Vocal Cord Paralysis","High"),
("ENT","Sleep Apnea","Medium"),


# ----------------------------------------------------------
# Psychiatry
# ----------------------------------------------------------

("Psychiatry","Major Depressive Disorder","High"),
("Psychiatry","Generalized Anxiety Disorder","Medium"),
("Psychiatry","Bipolar Disorder","High"),
("Psychiatry","Schizophrenia","Critical"),
("Psychiatry","Panic Disorder","Medium"),
("Psychiatry","Obsessive Compulsive Disorder","Medium"),
("Psychiatry","Post Traumatic Stress Disorder","High"),
("Psychiatry","Attention Deficit Hyperactivity Disorder","Medium"),
("Psychiatry","Autism Spectrum Disorder","Medium"),
("Psychiatry","Insomnia","Low"),
("Psychiatry","Substance Use Disorder","High"),
("Psychiatry","Alcohol Dependence","High"),
("Psychiatry","Eating Disorder","Medium"),
("Psychiatry","Personality Disorder","Medium"),
("Psychiatry","Suicidal Ideation","Critical"),
# ----------------------------------------------------------
# Oncology
# ----------------------------------------------------------

("Oncology","Breast Cancer","Critical"),
("Oncology","Lung Cancer","Critical"),
("Oncology","Colorectal Cancer","Critical"),
("Oncology","Prostate Cancer","High"),
("Oncology","Cervical Cancer","High"),
("Oncology","Ovarian Cancer","High"),
("Oncology","Pancreatic Cancer","Critical"),
("Oncology","Liver Cancer","Critical"),
("Oncology","Leukemia","Critical"),
("Oncology","Lymphoma","Critical"),
("Oncology","Multiple Myeloma","Critical"),
("Oncology","Brain Cancer","Critical"),
("Oncology","Thyroid Cancer","High"),
("Oncology","Skin Melanoma","Critical"),
("Oncology","Bladder Cancer","High"),
("Oncology","Kidney Cancer","High"),
("Oncology","Esophageal Cancer","Critical"),
("Oncology","Gastric Cancer","Critical"),
("Oncology","Testicular Cancer","Medium"),
("Oncology","Benign Neoplasm","Low"),


# ----------------------------------------------------------
# Pediatrics
# ----------------------------------------------------------

("Pediatrics","Neonatal Jaundice","Medium"),
("Pediatrics","Bronchiolitis","Medium"),
("Pediatrics","Chickenpox","Low"),
("Pediatrics","Measles","Medium"),
("Pediatrics","Mumps","Low"),
("Pediatrics","Rubella","Low"),
("Pediatrics","Hand Foot Mouth Disease","Low"),
("Pediatrics","Rotavirus Infection","Medium"),
("Pediatrics","Whooping Cough","Medium"),
("Pediatrics","Failure To Thrive","High"),
("Pediatrics","Congenital Heart Disease","Critical"),
("Pediatrics","Cerebral Palsy","High"),
("Pediatrics","Down Syndrome","Medium"),
("Pediatrics","Neonatal Sepsis","Critical"),
("Pediatrics","Prematurity","Critical"),


# ----------------------------------------------------------
# Obstetrics & Gynecology
# ----------------------------------------------------------

("Obstetrics","Normal Pregnancy","Low"),
("Obstetrics","High Risk Pregnancy","High"),
("Obstetrics","Gestational Hypertension","High"),
("Obstetrics","Preeclampsia","Critical"),
("Obstetrics","Eclampsia","Critical"),
("Obstetrics","Placenta Previa","Critical"),
("Obstetrics","Placental Abruption","Critical"),
("Obstetrics","Preterm Labor","Critical"),
("Obstetrics","Postpartum Hemorrhage","Critical"),
("Obstetrics","Hyperemesis Gravidarum","Medium"),

("Gynecology","Polycystic Ovary Syndrome","Medium"),
("Gynecology","Endometriosis","Medium"),
("Gynecology","Uterine Fibroids","Medium"),
("Gynecology","Pelvic Inflammatory Disease","High"),
("Gynecology","Ovarian Cyst","Medium"),
("Gynecology","Menorrhagia","Medium"),
("Gynecology","Dysmenorrhea","Low"),
("Gynecology","Cervicitis","Medium"),
("Gynecology","Infertility","Medium"),
("Gynecology","Menopause","Low"),


# ----------------------------------------------------------
# Urology
# ----------------------------------------------------------

("Urology","Benign Prostatic Hyperplasia","Medium"),
("Urology","Prostatitis","Medium"),
("Urology","Urinary Retention","Medium"),
("Urology","Bladder Stones","Medium"),
("Urology","Hydrocele","Low"),
("Urology","Varicocele","Low"),
("Urology","Erectile Dysfunction","Low"),
("Urology","Urinary Incontinence","Medium"),
("Urology","Testicular Torsion","Critical"),
("Urology","Bladder Infection","Medium"),


# ----------------------------------------------------------
# Infectious Diseases
# ----------------------------------------------------------

("Infectious Diseases","Dengue Fever","High"),
("Infectious Diseases","Malaria","High"),
("Infectious Diseases","Typhoid Fever","Medium"),
("Infectious Diseases","Cholera","Critical"),
("Infectious Diseases","Leptospirosis","High"),
("Infectious Diseases","Rabies","Critical"),
("Infectious Diseases","HIV Infection","High"),
("Infectious Diseases","AIDS","Critical"),
("Infectious Diseases","Sepsis","Critical"),
("Infectious Diseases","Septic Shock","Critical"),
("Infectious Diseases","Influenza A","Medium"),
("Infectious Diseases","COVID-19 Pneumonia","Critical"),
("Infectious Diseases","Meningococcal Infection","Critical"),
("Infectious Diseases","Tuberculous Meningitis","Critical"),
("Infectious Diseases","Food Poisoning","Low"),


# ----------------------------------------------------------
# Emergency Medicine
# ----------------------------------------------------------

("Emergency","Polytrauma","Critical"),
("Emergency","Road Traffic Accident","Critical"),
("Emergency","Burn Injury","Critical"),
("Emergency","Electric Shock","Critical"),
("Emergency","Poisoning","Critical"),
("Emergency","Snake Bite","Critical"),
("Emergency","Cardiac Arrest","Critical"),
("Emergency","Anaphylactic Shock","Critical"),
("Emergency","Heat Stroke","High"),
("Emergency","Hypothermia","High"),


# ----------------------------------------------------------
# Critical Care
# ----------------------------------------------------------

("Critical Care","Acute Respiratory Distress Syndrome","Critical"),
("Critical Care","Multi Organ Failure","Critical"),
("Critical Care","Ventilator Associated Pneumonia","Critical"),
("Critical Care","Septic Shock","Critical"),
("Critical Care","Acute Liver Failure","Critical"),
("Critical Care","Acute Heart Failure","Critical"),
("Critical Care","Disseminated Intravascular Coagulation","Critical"),
("Critical Care","Severe Electrolyte Imbalance","Critical"),
("Critical Care","Coma","Critical"),
("Critical Care","Shock","Critical"),


# ----------------------------------------------------------
# Hematology
# ----------------------------------------------------------

("Hematology","Iron Deficiency Anemia","Medium"),
("Hematology","Megaloblastic Anemia","Medium"),
("Hematology","Hemolytic Anemia","High"),
("Hematology","Aplastic Anemia","Critical"),
("Hematology","Sickle Cell Disease","High"),
("Hematology","Hemophilia","High"),
("Hematology","Thrombocytopenia","High"),
("Hematology","Polycythemia Vera","High"),
("Hematology","Deep Vein Thrombosis","High"),
("Hematology","Pulmonary Embolism","Critical"),


# ----------------------------------------------------------
# Immunology
# ----------------------------------------------------------

("Immunology","Systemic Lupus Erythematosus","High"),
("Immunology","Sjogren Syndrome","Medium"),
("Immunology","Vasculitis","High"),
("Immunology","Ankylosing Spondylitis","High"),
("Immunology","Psoriatic Arthritis","Medium"),
("Immunology","Autoimmune Hepatitis","High"),
("Immunology","Primary Immunodeficiency","Critical"),
("Immunology","Allergic Rhinitis","Low"),
("Immunology","Drug Allergy","Medium"),
("Immunology","Anaphylaxis","Critical"),


# ----------------------------------------------------------
# General Medicine
# ----------------------------------------------------------

("General Medicine","Fever","Low"),
("General Medicine","Viral Fever","Low"),
("General Medicine","Dehydration","Medium"),
("General Medicine","Syncope","Medium"),
("General Medicine","Weight Loss","Medium"),
("General Medicine","Fatigue","Low"),
("General Medicine","General Weakness","Low"),
("General Medicine","Loss Of Appetite","Low"),
("General Medicine","Chest Pain","High"),
("General Medicine","Abdominal Pain","Medium"),
]
# ==========================================================
# Generate Dataset
# ==========================================================

def generate_reference_diagnosis_codes():

    # Remove duplicate diagnosis names if any
    global DIAGNOSIS_DATA
    DIAGNOSIS_DATA = list(dict.fromkeys(DIAGNOSIS_DATA))

    records = []

    for index, (department, diagnosis, severity) in enumerate(DIAGNOSIS_DATA, start=1):

        records.append({
            "Diagnosis_Code": f"DX{index:04d}",
            "Diagnosis_Name": diagnosis,
            "Department": department,
            "Severity": severity,
            "ICD_Version": "ICD-10",
            "Active_Status": "Yes"
        })

    dataframe = pd.DataFrame(records)

    dataframe = pd.DataFrame(records)


# ==========================================================
# Save To Reference Folder
# ==========================================================

    path = os.path.join(
        config.REFERENCE_DIR,
        "reference_diagnosis_codes.csv"
    )


    dataframe.to_csv(
        path,
        index=False
    )

    print(f"Generated {len(dataframe)} diagnosis code references.")


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":
    generate_reference_diagnosis_codes()