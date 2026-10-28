/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 60_Create_Patient_Diagnoses_Map.sql

Purpose : Create Patient Diagnoses Mapping Table

Description:
Stores the relationship between patients and their diagnosis
records. This mapping captures disease information, diagnosing
doctor, appointment/admission association, diagnosis details,
severity, status, diagnostic method, follow-up information,
AI prediction usage, confidence, model information, and
ground-truth verification status.

Version : 2.4
===========================================================
*/

USE healthcare_ai_db;


-- ==========================================================
-- Remove Existing Table
-- Warning: This deletes existing data from this table.
-- ==========================================================

DROP TABLE IF EXISTS Patient_Diagnoses_Map;


-- ==========================================================
-- Create Patient Diagnoses Mapping Table
-- ==========================================================

CREATE TABLE Patient_Diagnoses_Map (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Diagnosis_Map_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Key References
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Diagnosis_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36)
        NOT NULL,

    Disease_ID CHAR(36)
        NOT NULL,

    Appointment_ID CHAR(36)
        NULL,

    Admission_ID CHAR(36)
        NULL,


    -- ======================================================
    -- Diagnosis Identification
    -- ======================================================

    Diagnosis_Number VARCHAR(30)
        NOT NULL,


    -- ======================================================
    -- Diagnosis Timeline
    -- ======================================================

    Diagnosis_Date DATETIME
        NOT NULL,


    -- ======================================================
    -- Clinical Diagnosis Information
    -- ======================================================

    Chief_Complaint TEXT
        NULL,

    Symptoms TEXT
        NULL,

    Clinical_Notes TEXT
        NULL,

    Severity ENUM(
        'Low',
        'Moderate',
        'High',
        'Critical'
    )
        NULL,

    Diagnosis_Status ENUM(
        'Confirmed',
        'Suspected',
        'Ruled Out'
    )
        NOT NULL DEFAULT 'Confirmed',

    Diagnosis_Method ENUM(
        'Clinical Examination',
        'Laboratory',
        'Radiology',
        'AI Prediction',
        'Combined'
    )
        NOT NULL DEFAULT 'Clinical Examination',

    Stage VARCHAR(50)
        NULL,


    -- ======================================================
    -- Diagnosis Classification
    -- ======================================================

    Is_Primary_Diagnosis BOOLEAN
        NOT NULL DEFAULT TRUE,

    Follow_Up_Required BOOLEAN
        NOT NULL DEFAULT FALSE,

    Follow_Up_Date DATE
        NULL,


    -- ======================================================
    -- AI Support
    -- ======================================================

    AI_Prediction_Used BOOLEAN
        NOT NULL DEFAULT FALSE,

    AI_Confidence DECIMAL(5,2)
        NULL,

    AI_Model_Name VARCHAR(100)
        NULL,

    Ground_Truth_Verified BOOLEAN
        NOT NULL DEFAULT FALSE,


    -- ======================================================
    -- Status Tracking
    -- ======================================================

    Is_Active BOOLEAN
        NOT NULL DEFAULT TRUE,

    Is_Deleted BOOLEAN
        NOT NULL DEFAULT FALSE,

    Record_Version INT
        NOT NULL DEFAULT 1,


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

    CONSTRAINT chk_pdiag_ai_confidence
        CHECK (
            AI_Confidence IS NULL
            OR AI_Confidence BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_pdiag_followup_required
        CHECK (
            Follow_Up_Required = FALSE
            OR Follow_Up_Date IS NOT NULL
        ),

    CONSTRAINT chk_pdiag_followup_date
        CHECK (
            Follow_Up_Date IS NULL
            OR Follow_Up_Date >= DATE(Diagnosis_Date)
        ),

    CONSTRAINT chk_pdiag_record_version
        CHECK (
            Record_Version >= 1
        ),


    -- ======================================================
    -- Foreign Key Constraints
    -- Unique names are used to prevent conflicts with
    -- foreign-key constraints in other project tables.
    -- ======================================================

    CONSTRAINT fk_pdiag_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_pdiag_diagnosis
        FOREIGN KEY (Diagnosis_ID)
        REFERENCES Diagnoses(Diagnosis_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_pdiag_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_pdiag_disease
        FOREIGN KEY (Disease_ID)
        REFERENCES Diseases(Disease_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_pdiag_appointment
        FOREIGN KEY (Appointment_ID)
        REFERENCES Appointments(Appointment_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_pdiag_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Duplicate Record Prevention
    -- Each diagnosis record can appear only once.
    -- ======================================================

    CONSTRAINT uk_pdiag_diagnosis
        UNIQUE (
            Diagnosis_ID
        )

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_pdiag_patient
    ON Patient_Diagnoses_Map(Patient_ID);

CREATE INDEX idx_pdiag_diagnosis
    ON Patient_Diagnoses_Map(Diagnosis_ID);

CREATE INDEX idx_pdiag_diagnosis_number
    ON Patient_Diagnoses_Map(Diagnosis_Number);

CREATE INDEX idx_pdiag_doctor
    ON Patient_Diagnoses_Map(Doctor_ID);

CREATE INDEX idx_pdiag_disease
    ON Patient_Diagnoses_Map(Disease_ID);

CREATE INDEX idx_pdiag_appointment
    ON Patient_Diagnoses_Map(Appointment_ID);

CREATE INDEX idx_pdiag_admission
    ON Patient_Diagnoses_Map(Admission_ID);

CREATE INDEX idx_pdiag_diagnosis_date
    ON Patient_Diagnoses_Map(Diagnosis_Date);

CREATE INDEX idx_pdiag_status
    ON Patient_Diagnoses_Map(Diagnosis_Status);

CREATE INDEX idx_pdiag_severity
    ON Patient_Diagnoses_Map(Severity);

CREATE INDEX idx_pdiag_method
    ON Patient_Diagnoses_Map(Diagnosis_Method);

CREATE INDEX idx_pdiag_primary
    ON Patient_Diagnoses_Map(Is_Primary_Diagnosis);

CREATE INDEX idx_pdiag_followup
    ON Patient_Diagnoses_Map(Follow_Up_Required);

CREATE INDEX idx_pdiag_followup_date
    ON Patient_Diagnoses_Map(Follow_Up_Date);

CREATE INDEX idx_pdiag_ai_prediction
    ON Patient_Diagnoses_Map(AI_Prediction_Used);

CREATE INDEX idx_pdiag_ai_confidence
    ON Patient_Diagnoses_Map(AI_Confidence);

CREATE INDEX idx_pdiag_ground_truth
    ON Patient_Diagnoses_Map(Ground_Truth_Verified);

CREATE INDEX idx_pdiag_active
    ON Patient_Diagnoses_Map(Is_Active);

CREATE INDEX idx_pdiag_deleted
    ON Patient_Diagnoses_Map(Is_Deleted);

CREATE INDEX idx_pdiag_record_version
    ON Patient_Diagnoses_Map(Record_Version);

CREATE INDEX idx_pdiag_data_source
    ON Patient_Diagnoses_Map(Data_Source);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Patient_Diagnoses_Map;