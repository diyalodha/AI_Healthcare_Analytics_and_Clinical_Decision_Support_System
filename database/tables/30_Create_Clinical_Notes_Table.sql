/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 30_Create_Clinical_Notes_Table.sql

Purpose : Create Clinical Notes Table

Description:
Stores doctor clinical notes, nursing notes, discharge
summaries, NLP extracted entities, AI processing
information, and clinical documentation.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Clinical_Notes;

CREATE TABLE Clinical_Notes (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Clinical_Note_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Keys
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36)
        NOT NULL,

    Admission_ID CHAR(36),

    Appointment_ID CHAR(36),


    -- ======================================================
    -- Note Information
    -- ======================================================

    Note_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

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

    Note_Title VARCHAR(200),

    Clinical_Note LONGTEXT
        NOT NULL,

    Diagnosis_Summary TEXT,

    Treatment_Plan TEXT,

    Follow_Up_Instructions TEXT,

    Confidential BOOLEAN
        DEFAULT FALSE,

    Note_Status ENUM(
        'Draft',
        'Reviewed',
        'Approved',
        'Archived'
    )
    DEFAULT 'Draft',


    -- ======================================================
    -- NLP & AI Processing
    -- ======================================================

    NLP_Processed BOOLEAN
        DEFAULT FALSE,

    NLP_Model_Name VARCHAR(150),

    Extracted_Entities LONGTEXT,

    Extracted_Diagnosis TEXT,

    Extracted_Medications TEXT,

    Extracted_Procedures TEXT,

    Sentiment_Score DECIMAL(5,2),

    AI_Summary TEXT,

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

    Reviewed_By_AI BOOLEAN
        DEFAULT FALSE,


    -- ======================================================
    -- Dataset Tracking
    -- ======================================================

    Data_Source ENUM(
        'MIMIC-IV',
        'Synthetic',
        'Hospital_Records',
        'Hybrid Dataset'
    )
    DEFAULT 'Synthetic',


    Used_For_Model_Training BOOLEAN
        DEFAULT FALSE,


    -- ======================================================
    -- Status Information
    -- ======================================================

    Is_Active BOOLEAN
        DEFAULT TRUE,

    Is_Deleted BOOLEAN
        DEFAULT FALSE,

    Record_Version INT
        DEFAULT 1,


    -- ======================================================
    -- Audit Information
    -- ======================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,


    -- ======================================================
    -- Foreign Keys
    -- ======================================================

    CONSTRAINT fk_notes_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_notes_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_notes_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_notes_appointment
        FOREIGN KEY (Appointment_ID)
        REFERENCES Appointments(Appointment_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT chk_notes_sentiment_score
        CHECK (
            Sentiment_Score IS NULL
            OR (Sentiment_Score >= -1 AND Sentiment_Score <= 1)
        )

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_notes_number
ON Clinical_Notes(Note_Number);

CREATE INDEX idx_notes_patient
ON Clinical_Notes(Patient_ID);

CREATE INDEX idx_notes_doctor
ON Clinical_Notes(Doctor_ID);

CREATE INDEX idx_notes_admission
ON Clinical_Notes(Admission_ID);

CREATE INDEX idx_notes_appointment
ON Clinical_Notes(Appointment_ID);

CREATE INDEX idx_notes_type
ON Clinical_Notes(Note_Type);

CREATE INDEX idx_notes_status
ON Clinical_Notes(Note_Status);

CREATE INDEX idx_notes_created
ON Clinical_Notes(Created_At);

CREATE INDEX idx_notes_nlp
ON Clinical_Notes(NLP_Processed);

CREATE INDEX idx_notes_ai_review
ON Clinical_Notes(Reviewed_By_AI);

CREATE INDEX idx_notes_ai_risk
ON Clinical_Notes(AI_Risk_Level);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Clinical_Notes;