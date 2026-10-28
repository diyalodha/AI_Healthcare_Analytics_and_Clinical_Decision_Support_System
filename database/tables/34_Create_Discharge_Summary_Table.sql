/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 34_Create_Discharge_Summary_Table.sql

Purpose : Create Discharge Summary Table

Description:
Stores complete discharge information used for
clinical analytics, patient recovery assessment,
AI-based readmission prediction, and healthcare
decision support.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

-- ==========================================================
-- Create Discharge Summary Table
-- ==========================================================

CREATE TABLE IF NOT EXISTS Discharge_Summary (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Discharge_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Keys
    -- ======================================================

    Admission_ID CHAR(36)
        NOT NULL,

    Patient_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36),


    -- ======================================================
    -- Discharge Information
    -- ======================================================

    Discharge_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Admission_Date DATE,

    Discharge_Date DATE
        NOT NULL,

    Length_Of_Stay_Days INT,

    Final_Diagnosis LONGTEXT
        NOT NULL,

    Secondary_Diagnosis TEXT,

    Treatment_Provided TEXT,

    Procedures_Performed TEXT,

    Medications_At_Discharge TEXT,

    Follow_Up_Instructions TEXT,

    Follow_Up_Date DATE,

    Diet_Advice TEXT,

    Activity_Advice TEXT,

    Condition_At_Discharge VARCHAR(200),

    Discharge_Status ENUM(
        'Recovered',
        'Improved',
        'Referred',
        'Expired',
        'NotSpecified'
    )
    NOT NULL,

    Readmission_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

    Doctor_Remarks TEXT,


    -- ======================================================
    -- AI Analytics
    -- ======================================================

    AI_Readmission_Probability DECIMAL(5,2),

    AI_Recommendation TEXT,

    Recovery_Score DECIMAL(5,2),

    Discharge_Approved_By_AI BOOLEAN
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


    -- ======================================================
    -- Status Information
    -- ======================================================

    Is_Active BOOLEAN
        DEFAULT TRUE,

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

    CONSTRAINT fk_discharge_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_discharge_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_discharge_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Check Constraints
    -- ======================================================

    CONSTRAINT chk_discharge_dates
        CHECK (
            Admission_Date IS NULL
            OR Discharge_Date >= Admission_Date
        ),

    CONSTRAINT chk_recovery_score
        CHECK (
            Recovery_Score IS NULL
            OR Recovery_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_readmission_probability
        CHECK (
            AI_Readmission_Probability IS NULL
            OR AI_Readmission_Probability BETWEEN 0 AND 100
        )

);

-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_discharge_number
ON Discharge_Summary(Discharge_Number);

CREATE INDEX idx_discharge_patient
ON Discharge_Summary(Patient_ID);

CREATE INDEX idx_discharge_admission
ON Discharge_Summary(Admission_ID);

CREATE INDEX idx_discharge_doctor
ON Discharge_Summary(Doctor_ID);

CREATE INDEX idx_discharge_date
ON Discharge_Summary(Discharge_Date);

CREATE INDEX idx_discharge_status
ON Discharge_Summary(Discharge_Status);

CREATE INDEX idx_discharge_readmission_risk
ON Discharge_Summary(Readmission_Risk_Level);

CREATE INDEX idx_discharge_active
ON Discharge_Summary(Is_Active);

-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Discharge_Summary;