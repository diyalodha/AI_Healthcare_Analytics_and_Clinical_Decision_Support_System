/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 65_Create_Patient_Clinical_Notes_Map.sql

Purpose : Create Patient Clinical Notes Mapping Table

Description:
Maps patients to their clinical notes and connects clinical
documentation with doctors, admissions and appointments.

Supports:
- Patient clinical history
- Clinical documentation analysis
- NLP processing
- AI summarization
- Diagnosis extraction
- Medication extraction
- Procedure extraction
- Clinical risk analysis
- Explainable AI
- Dataset tracking

Version : 2.2

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- ==========================================================
-- Remove Existing Table
-- Warning: This deletes existing data from this table.
-- ==========================================================

DROP TABLE IF EXISTS Patient_Clinical_Notes_Map;


-- ==========================================================
-- Create Patient Clinical Notes Mapping Table
-- ==========================================================

CREATE TABLE Patient_Clinical_Notes_Map (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Clinical_Notes_Map_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Key References
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Clinical_Note_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36)
        NOT NULL,

    Admission_ID CHAR(36)
        NULL,

    Appointment_ID CHAR(36)
        NULL,


    -- ======================================================
    -- Clinical Note Identification
    -- ======================================================

    Note_Number VARCHAR(30)
        NOT NULL,

    Note_Type ENUM(
        'Consultation',
        'Progress',
        'Discharge',
        'Nursing',
        'Emergency',
        'Follow-Up',
        'ICU',
        'General'
    )
        NOT NULL,

    Note_Title VARCHAR(200)
        NULL,


    -- ======================================================
    -- Clinical Documentation
    -- ======================================================

    Clinical_Note LONGTEXT
        NOT NULL,

    Diagnosis_Summary TEXT
        NULL,

    Treatment_Plan TEXT
        NULL,

    Follow_Up_Instructions TEXT
        NULL,

    Confidential BOOLEAN
        NOT NULL DEFAULT FALSE,


    -- ======================================================
    -- Note Status
    -- ======================================================

    Note_Status ENUM(
        'Draft',
        'Reviewed',
        'Approved',
        'Archived'
    )
        NOT NULL DEFAULT 'Draft',


    -- ======================================================
    -- NLP Processing
    -- ======================================================

    NLP_Processed BOOLEAN
        NOT NULL DEFAULT FALSE,

    NLP_Model_Name VARCHAR(150)
        NULL,

    Extracted_Entities LONGTEXT
        NULL,

    Extracted_Diagnosis TEXT
        NULL,

    Extracted_Medications TEXT
        NULL,

    Extracted_Procedures TEXT
        NULL,


    -- ======================================================
    -- AI Analysis
    -- ======================================================

    Sentiment_Score DECIMAL(5,2)
        NULL,

    AI_Summary TEXT
        NULL,

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
        NOT NULL DEFAULT 'Low',

    Reviewed_By_AI BOOLEAN
        NOT NULL DEFAULT FALSE,


    -- ======================================================
    -- Dataset Tracking
    -- ======================================================

    Data_Source ENUM(
        'MIMIC-IV',
        'Synthetic',
        'Hospital_Records',
        'Hybrid Dataset'
    )
        NOT NULL DEFAULT 'Synthetic',

    Used_For_Model_Training BOOLEAN
        NOT NULL DEFAULT FALSE,


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

    CONSTRAINT chk_pcn_sentiment_score
        CHECK (
            Sentiment_Score IS NULL
            OR Sentiment_Score BETWEEN -1 AND 1
        ),

    CONSTRAINT chk_pcn_record_version
        CHECK (
            Record_Version >= 1
        ),


    -- ======================================================
    -- Foreign Key Constraints
    -- ======================================================

    CONSTRAINT fk_pcn_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_pcn_clinical_note
        FOREIGN KEY (Clinical_Note_ID)
        REFERENCES Clinical_Notes(Clinical_Note_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_pcn_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_pcn_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_pcn_appointment
        FOREIGN KEY (Appointment_ID)
        REFERENCES Appointments(Appointment_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Duplicate Record Prevention
    -- Each clinical note can appear only once in mapping.
    -- ======================================================

    CONSTRAINT uk_pcn_clinical_note
        UNIQUE (
            Clinical_Note_ID
        )

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_pcn_patient
    ON Patient_Clinical_Notes_Map(Patient_ID);

CREATE INDEX idx_pcn_clinical_note
    ON Patient_Clinical_Notes_Map(Clinical_Note_ID);

CREATE INDEX idx_pcn_doctor
    ON Patient_Clinical_Notes_Map(Doctor_ID);

CREATE INDEX idx_pcn_admission
    ON Patient_Clinical_Notes_Map(Admission_ID);

CREATE INDEX idx_pcn_appointment
    ON Patient_Clinical_Notes_Map(Appointment_ID);

CREATE INDEX idx_pcn_note_number
    ON Patient_Clinical_Notes_Map(Note_Number);

CREATE INDEX idx_pcn_note_type
    ON Patient_Clinical_Notes_Map(Note_Type);

CREATE INDEX idx_pcn_note_status
    ON Patient_Clinical_Notes_Map(Note_Status);

CREATE INDEX idx_pcn_nlp
    ON Patient_Clinical_Notes_Map(NLP_Processed);

CREATE INDEX idx_pcn_ai_review
    ON Patient_Clinical_Notes_Map(Reviewed_By_AI);

CREATE INDEX idx_pcn_ai_risk
    ON Patient_Clinical_Notes_Map(AI_Risk_Level);

CREATE INDEX idx_pcn_training
    ON Patient_Clinical_Notes_Map(Used_For_Model_Training);

CREATE INDEX idx_pcn_data_source
    ON Patient_Clinical_Notes_Map(Data_Source);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Patient_Clinical_Notes_Map;