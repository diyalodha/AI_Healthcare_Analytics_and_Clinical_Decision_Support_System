/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 54_Create_Patient_Medications_Map.sql

Purpose : Create Patient-Medications Mapping Table

Description:
Stores a patient's medication history, including medication
details, dosage, duration, prescribing doctor, treatment
response, adverse reactions, adherence, and AI-related
effectiveness and risk information.

Important:
This file corresponds to the existing
Patient_Medications_Map table.

Version : 2.3
===========================================================
*/

USE healthcare_ai_db;


-- ==========================================================
-- Remove Existing Table
-- WARNING:
-- This deletes existing data from Patient_Medications_Map.
-- Execute only during schema creation/reset.
-- ==========================================================

DROP TABLE IF EXISTS Patient_Medications_Map;


-- ==========================================================
-- Create Patient Medication Mapping Table
-- ==========================================================

CREATE TABLE Patient_Medications_Map (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Patient_Medication_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Key References
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Medication_ID CHAR(36)
        NOT NULL,

    Prescribed_By_Doctor_ID CHAR(36)
        NULL,


    -- ======================================================
    -- Medication Timeline
    -- ======================================================

    Prescription_Date DATE
        NOT NULL,

    Start_Date DATE
        NOT NULL,

    End_Date DATE
        NULL,

    Duration_Days INT
        NULL,


    -- ======================================================
    -- Dosage and Administration
    -- ======================================================

    Dosage VARCHAR(100)
        NULL,

    Dosage_Unit VARCHAR(50)
        NULL,

    Frequency VARCHAR(100)
        NULL,

    Route ENUM(
        'Oral',
        'Intravenous',
        'Intramuscular',
        'Subcutaneous',
        'Topical',
        'Inhalation',
        'Sublingual',
        'Rectal',
        'Other'
    )
        DEFAULT 'Oral',

    Quantity_Prescribed INT
        NULL,

    Refills_Allowed INT
        NOT NULL DEFAULT 0,


    -- ======================================================
    -- Treatment Information
    -- ======================================================

    Treatment_Indication TEXT
        NULL,

    Treatment_Purpose ENUM(
        'Primary Treatment',
        'Supportive Treatment',
        'Preventive',
        'Chronic Management',
        'Emergency',
        'Other'
    )
        DEFAULT 'Primary Treatment',

    Medication_Status ENUM(
        'Active',
        'Completed',
        'Discontinued',
        'On Hold',
        'Cancelled'
    )
        DEFAULT 'Active',

    Discontinuation_Reason TEXT
        NULL,


    -- ======================================================
    -- Patient Response and Safety
    -- ======================================================

    Patient_Response ENUM(
        'Effective',
        'Partially Effective',
        'Ineffective',
        'Adverse Reaction',
        'Unknown'
    )
        DEFAULT 'Unknown',

    Adverse_Reaction BOOLEAN
        NOT NULL DEFAULT FALSE,

    Adverse_Reaction_Details TEXT
        NULL,

    Medication_Adherence_Percentage DECIMAL(5,2)
        NULL,


    -- ======================================================
    -- Notes
    -- ======================================================

    Doctor_Notes TEXT
        NULL,

    Patient_Notes TEXT
        NULL,


    -- ======================================================
    -- AI Analytics
    -- ======================================================

    AI_Effectiveness_Score DECIMAL(5,2)
        NULL,

    AI_Adverse_Risk_Score DECIMAL(5,2)
        NULL,

    AI_Recommendation TEXT
        NULL,


    -- ======================================================
    -- Dataset Source Tracking
    -- ======================================================

    Data_Source ENUM(
        'MIMIC-IV',
        'Synthetic',
        'Hospital_Records',
        'Hybrid Dataset'
    )
        NOT NULL DEFAULT 'Synthetic',


    -- ======================================================
    -- Audit Information
    -- ======================================================

    Created_By VARCHAR(50)
        NULL,

    Updated_By VARCHAR(50)
        NULL,

    Created_At TIMESTAMP
        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,


    -- ======================================================
    -- Validation Constraints
    -- ======================================================

    CONSTRAINT chk_pm_end_date
        CHECK (
            End_Date IS NULL
            OR End_Date >= Start_Date
        ),

    CONSTRAINT chk_pm_duration_days
        CHECK (
            Duration_Days IS NULL
            OR Duration_Days >= 0
        ),

    CONSTRAINT chk_pm_quantity
        CHECK (
            Quantity_Prescribed IS NULL
            OR Quantity_Prescribed >= 0
        ),

    CONSTRAINT chk_pm_refills
        CHECK (
            Refills_Allowed >= 0
        ),

    CONSTRAINT chk_pm_adherence
        CHECK (
            Medication_Adherence_Percentage IS NULL
            OR Medication_Adherence_Percentage BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_pm_effectiveness
        CHECK (
            AI_Effectiveness_Score IS NULL
            OR AI_Effectiveness_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_pm_adverse_risk
        CHECK (
            AI_Adverse_Risk_Score IS NULL
            OR AI_Adverse_Risk_Score BETWEEN 0 AND 100
        ),


    -- ======================================================
    -- Foreign Key Constraints
    -- ======================================================

    CONSTRAINT fk_pm_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_pm_medication
        FOREIGN KEY (Medication_ID)
        REFERENCES Medications(Medication_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_pm_doctor
        FOREIGN KEY (Prescribed_By_Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Duplicate Protection
    -- ======================================================

    CONSTRAINT uk_pm_prescription
        UNIQUE (
            Patient_ID,
            Medication_ID,
            Prescription_Date,
            Prescribed_By_Doctor_ID
        )

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_pm_patient
    ON Patient_Medications_Map(Patient_ID);

CREATE INDEX idx_pm_medication
    ON Patient_Medications_Map(Medication_ID);

CREATE INDEX idx_pm_doctor
    ON Patient_Medications_Map(Prescribed_By_Doctor_ID);

CREATE INDEX idx_pm_status
    ON Patient_Medications_Map(Medication_Status);

CREATE INDEX idx_pm_start_date
    ON Patient_Medications_Map(Start_Date);

CREATE INDEX idx_pm_end_date
    ON Patient_Medications_Map(End_Date);

CREATE INDEX idx_pm_adverse_reaction
    ON Patient_Medications_Map(Adverse_Reaction);

CREATE INDEX idx_pm_adverse_risk
    ON Patient_Medications_Map(AI_Adverse_Risk_Score);

CREATE INDEX idx_pm_data_source
    ON Patient_Medications_Map(Data_Source);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Patient_Medications_Map;