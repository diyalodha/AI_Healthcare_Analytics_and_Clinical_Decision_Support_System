/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 11_Create_Diagnoses_Table.sql
Purpose : Create Diagnoses Transaction Table
Version : 3.0
Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Diagnoses;

-- ===========================================================
-- Create Diagnoses Table
-- ===========================================================

CREATE TABLE Diagnoses (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Diagnosis_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =======================================================
    -- Foreign Keys
    -- =======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36)
        NOT NULL,

    Disease_ID CHAR(36)
        NOT NULL,

    Appointment_ID CHAR(36),

    Admission_ID CHAR(36),


    -- =======================================================
    -- Diagnosis Information
    -- =======================================================

    Diagnosis_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Diagnosis_Date DATETIME
        NOT NULL,

    Chief_Complaint TEXT,

    Symptoms TEXT,

    Clinical_Notes TEXT,

    Severity ENUM(
        'Low',
        'Moderate',
        'High',
        'Critical'
    ),

    Diagnosis_Status ENUM(
        'Confirmed',
        'Suspected',
        'Ruled Out'
    )
    DEFAULT 'Confirmed',

    Diagnosis_Method ENUM(
        'Clinical Examination',
        'Laboratory',
        'Radiology',
        'AI Prediction',
        'Combined'
    )
    DEFAULT 'Clinical Examination',

    Stage VARCHAR(50),

    Is_Primary_Diagnosis BOOLEAN
        DEFAULT TRUE,

    Follow_Up_Required BOOLEAN
        DEFAULT FALSE,

    Follow_Up_Date DATE,


    -- =======================================================
    -- AI Support
    -- =======================================================

    AI_Prediction_Used BOOLEAN
        DEFAULT FALSE,

    AI_Confidence DECIMAL(5,2),

    AI_Model_Name VARCHAR(100),

    Ground_Truth_Verified BOOLEAN
        DEFAULT FALSE,


    -- =======================================================
    -- Status
    -- =======================================================

    Is_Active BOOLEAN
        DEFAULT TRUE,

    Is_Deleted BOOLEAN
        DEFAULT FALSE,

    Record_Version INT
        DEFAULT 1,


    -- =======================================================
    -- Audit Information
    -- =======================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,


    -- =======================================================
    -- Foreign Keys
    -- =======================================================

    FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (Disease_ID)
        REFERENCES Diseases(Disease_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (Appointment_ID)
        REFERENCES Appointments(Appointment_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CHECK (
        AI_Confidence IS NULL
        OR AI_Confidence BETWEEN 0 AND 100
    )

);

-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_diagnosis_number
ON Diagnoses(Diagnosis_Number);

CREATE INDEX idx_diagnosis_patient
ON Diagnoses(Patient_ID);

CREATE INDEX idx_diagnosis_doctor
ON Diagnoses(Doctor_ID);

CREATE INDEX idx_diagnosis_disease
ON Diagnoses(Disease_ID);

CREATE INDEX idx_diagnosis_date
ON Diagnoses(Diagnosis_Date);

CREATE INDEX idx_diagnosis_status
ON Diagnoses(Diagnosis_Status);

CREATE INDEX idx_diagnosis_severity
ON Diagnoses(Severity);

CREATE INDEX idx_ground_truth
ON Diagnoses(Ground_Truth_Verified);

CREATE INDEX idx_ai_prediction
ON Diagnoses(AI_Prediction_Used);

-- ===========================================================
-- Verification
-- ===========================================================

SHOW TABLES;

DESCRIBE Diagnoses;