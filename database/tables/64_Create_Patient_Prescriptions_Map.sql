/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 64_Create_Patient_Prescriptions_Map.sql

Purpose : Create Patient Prescriptions Mapping Table

Description:
Stores the relationship between patients and prescription
records. This mapping captures prescription information,
diagnosis, prescribing doctor, appointment/admission context,
prescription type, advice, follow-up information, AI support,
prescription status, and dataset source.

The Prescriptions table is the main transaction table.

Version : 2.3

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- ==========================================================
-- Remove Existing Table
-- Warning: This deletes existing data from this table.
-- ==========================================================

DROP TABLE IF EXISTS Patient_Prescriptions_Map;


-- ==========================================================
-- Create Patient Prescriptions Mapping Table
-- ==========================================================

CREATE TABLE Patient_Prescriptions_Map (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Prescription_Map_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Key References
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Prescription_ID CHAR(36)
        NOT NULL,

    Diagnosis_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36)
        NOT NULL,

    Appointment_ID CHAR(36)
        NULL,

    Admission_ID CHAR(36)
        NULL,


    -- ======================================================
    -- Prescription Identification
    -- ======================================================

    Prescription_Number VARCHAR(30)
        NOT NULL,


    -- ======================================================
    -- Prescription Timeline
    -- ======================================================

    Prescription_Date DATETIME
        NOT NULL,

    Follow_Up_Date DATE
        NULL,


    -- ======================================================
    -- Prescription Classification
    -- ======================================================

    Prescription_Type ENUM(
        'OPD',
        'IPD',
        'Emergency',
        'Discharge'
    )
        NOT NULL DEFAULT 'OPD',


    Prescription_Status ENUM(
        'Active',
        'Completed',
        'Cancelled'
    )
        NOT NULL DEFAULT 'Active',


    -- ======================================================
    -- Clinical Advice
    -- ======================================================

    Advice TEXT
        NULL,

    Lifestyle_Advice TEXT
        NULL,

    Diet_Advice TEXT
        NULL,

    Prescription_Notes TEXT
        NULL,

    Digital_Signature VARCHAR(255)
        NULL,


    -- ======================================================
    -- Follow-Up Information
    -- ======================================================

    Requires_Followup BOOLEAN
        NOT NULL DEFAULT FALSE,


    -- ======================================================
    -- AI Decision Support
    -- ======================================================

    AI_Generated BOOLEAN
        NOT NULL DEFAULT FALSE,

    AI_Recommendation_Score DECIMAL(5,2)
        NULL,


    -- ======================================================
    -- Status Information
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

    CONSTRAINT chk_ppresm_followup_date
        CHECK (
            Follow_Up_Date IS NULL
            OR Follow_Up_Date >= DATE(Prescription_Date)
        ),


    CONSTRAINT chk_ppresm_ai_score
        CHECK (
            AI_Recommendation_Score IS NULL
            OR AI_Recommendation_Score BETWEEN 0 AND 100
        ),


    CONSTRAINT chk_ppresm_record_version
        CHECK (
            Record_Version >= 1
        ),


    -- ======================================================
    -- Foreign Key Constraints
    --
    -- Unique fk_ppresm_* names prevent conflicts with
    -- existing constraints in healthcare_ai_db.
    -- ======================================================

    CONSTRAINT fk_ppresm_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,


    CONSTRAINT fk_ppresm_prescription
        FOREIGN KEY (Prescription_ID)
        REFERENCES Prescriptions(Prescription_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,


    CONSTRAINT fk_ppresm_diagnosis
        FOREIGN KEY (Diagnosis_ID)
        REFERENCES Diagnoses(Diagnosis_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,


    CONSTRAINT fk_ppresm_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,


    CONSTRAINT fk_ppresm_appointment
        FOREIGN KEY (Appointment_ID)
        REFERENCES Appointments(Appointment_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_ppresm_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Duplicate Record Prevention
    --
    -- Each prescription can appear only once in the
    -- Patient Prescriptions Mapping table.
    -- ======================================================

    CONSTRAINT uk_ppresm_prescription
        UNIQUE (
            Prescription_ID
        )

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_ppresm_patient
    ON Patient_Prescriptions_Map(Patient_ID);

CREATE INDEX idx_ppresm_prescription
    ON Patient_Prescriptions_Map(Prescription_ID);

CREATE INDEX idx_ppresm_diagnosis
    ON Patient_Prescriptions_Map(Diagnosis_ID);

CREATE INDEX idx_ppresm_doctor
    ON Patient_Prescriptions_Map(Doctor_ID);

CREATE INDEX idx_ppresm_appointment
    ON Patient_Prescriptions_Map(Appointment_ID);

CREATE INDEX idx_ppresm_admission
    ON Patient_Prescriptions_Map(Admission_ID);

CREATE INDEX idx_ppresm_number
    ON Patient_Prescriptions_Map(Prescription_Number);

CREATE INDEX idx_ppresm_date
    ON Patient_Prescriptions_Map(Prescription_Date);

CREATE INDEX idx_ppresm_followup_date
    ON Patient_Prescriptions_Map(Follow_Up_Date);

CREATE INDEX idx_ppresm_type
    ON Patient_Prescriptions_Map(Prescription_Type);

CREATE INDEX idx_ppresm_status
    ON Patient_Prescriptions_Map(Prescription_Status);

CREATE INDEX idx_ppresm_requires_followup
    ON Patient_Prescriptions_Map(Requires_Followup);

CREATE INDEX idx_ppresm_ai_generated
    ON Patient_Prescriptions_Map(AI_Generated);

CREATE INDEX idx_ppresm_ai_score
    ON Patient_Prescriptions_Map(AI_Recommendation_Score);

CREATE INDEX idx_ppresm_active
    ON Patient_Prescriptions_Map(Is_Active);

CREATE INDEX idx_ppresm_data_source
    ON Patient_Prescriptions_Map(Data_Source);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Patient_Prescriptions_Map;