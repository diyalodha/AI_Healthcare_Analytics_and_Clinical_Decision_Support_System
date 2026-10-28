"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : config.py

Purpose :
Central configuration file for healthcare dataset generation.

Author : Diya Lodha & Team
===========================================================
"""

import os


# ==========================================================
# Random Seed
# ==========================================================

RANDOM_SEED = 42


# ==========================================================
# Project Directories
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_DIR = os.path.dirname(
    os.path.dirname(BASE_DIR)
)


# ==========================================================
# Dataset Directories
# ==========================================================

REFERENCE_DIR = os.path.join(
    BASE_DIR,
    "reference"
)

SYNTHETIC_DIR = os.path.join(
    PROJECT_DIR,
    "datasets",
    "synthetic"
)


# ==========================================================
# Create Directories
# ==========================================================

os.makedirs(
    REFERENCE_DIR,
    exist_ok=True
)

os.makedirs(
    SYNTHETIC_DIR,
    exist_ok=True
)


# ==========================================================
# Reference Dataset Sizes
# ==========================================================

NUM_DEPARTMENTS = 25
NUM_DOCTORS = 2000
NUM_DISEASES = 250
NUM_MEDICATIONS = 500
NUM_INSURANCE_PROVIDERS = 100
NUM_PATIENTS = 100000


# ==========================================================
# Clinical Dataset Sizes
# ==========================================================

NUM_ADMISSIONS = 300000
NUM_DIAGNOSES = 450000
NUM_VITAL_SIGNS = 2000000
NUM_LAB_RESULTS = 3000000
NUM_PRESCRIPTIONS = 800000
NUM_CLINICAL_NOTES = 500000
NUM_MEDICAL_PROCEDURES = 250000
NUM_IMAGING_REPORTS = 200000
NUM_ICU_STAYS = 50000
NUM_DISCHARGE_SUMMARY = 300000


# ==========================================================
# AI Dataset Sizes
# ==========================================================

NUM_AI_PREDICTIONS = 500000
NUM_HEALTH_SCORE = 100000
NUM_AI_RECOMMENDATIONS = 500000
NUM_EXPLAINABLE_AI = 500000


# ==========================================================
# Generation Optimization
# ==========================================================

GENERATION_CHUNK_SIZE = 100000

LAB_CHUNK_SIZE = 100000
DIAGNOSIS_CHUNK_SIZE = 100000
VITAL_CHUNK_SIZE = 100000
PRESCRIPTION_CHUNK_SIZE = 100000
CLINICAL_NOTE_CHUNK_SIZE = 100000
PROCEDURE_CHUNK_SIZE = 100000
IMAGING_CHUNK_SIZE = 100000
DISCHARGE_CHUNK_SIZE = 100000
AI_CHUNK_SIZE = 100000