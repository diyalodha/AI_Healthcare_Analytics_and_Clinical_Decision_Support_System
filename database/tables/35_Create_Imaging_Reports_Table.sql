/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 35_Create_Imaging_Reports_Table.sql

Purpose : Create Medical Imaging Reports Table

Description:
Stores diagnostic imaging reports including findings,
radiologist interpretation, AI analysis results, image
metadata, and clinical recommendations for healthcare
analytics.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

-- ==========================================================
-- Create Imaging Reports Table
-- ==========================================================

CREATE TABLE IF NOT EXISTS Imaging_Reports (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Imaging_Report_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Keys
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36),

    Admission_ID CHAR(36),


    -- ======================================================
    -- Imaging Information
    -- ======================================================

    Imaging_Report_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Imaging_Type ENUM(
        'X-Ray',
        'CT Scan',
        'MRI',
        'Ultrasound',
        'PET Scan',
        'Mammography',
        'ECG',
        'Echocardiography',
        'Other'
    )
    NOT NULL,

    Body_Part VARCHAR(150),

    Imaging_Date DATETIME
        NOT NULL,

    Clinical_Indication TEXT,

    Contrast_Used BOOLEAN
        DEFAULT FALSE,

    Contrast_Type VARCHAR(100),

    Radiologist_Name VARCHAR(150),


    -- ======================================================
    -- Report Details
    -- ======================================================

    Findings LONGTEXT,

    Impression LONGTEXT,

    Recommendation TEXT,

    Report_Status ENUM(
        'Pending',
        'Completed',
        'Verified',
        'Rejected'
    )
    DEFAULT 'Pending',


    -- ======================================================
    -- AI Imaging Analysis
    -- ======================================================

    AI_Analysis_Performed BOOLEAN
        DEFAULT FALSE,

    AI_Model_Name VARCHAR(150),

    AI_Model_Version VARCHAR(50),

    AI_Detected_Findings TEXT,

    AI_Confidence_Score DECIMAL(5,2),

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

    Abnormality_Detected BOOLEAN
        DEFAULT FALSE,

    Abnormality_Type VARCHAR(200),

    AI_Recommendation TEXT,


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

    CONSTRAINT fk_imaging_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_imaging_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_imaging_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Check Constraints
    -- ======================================================

    CONSTRAINT chk_ai_confidence_imaging
        CHECK (
            AI_Confidence_Score IS NULL
            OR AI_Confidence_Score BETWEEN 0 AND 100
        )

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_imaging_number
ON Imaging_Reports(Imaging_Report_Number);

CREATE INDEX idx_imaging_patient
ON Imaging_Reports(Patient_ID);

CREATE INDEX idx_imaging_doctor
ON Imaging_Reports(Doctor_ID);

CREATE INDEX idx_imaging_admission
ON Imaging_Reports(Admission_ID);

CREATE INDEX idx_imaging_type
ON Imaging_Reports(Imaging_Type);

CREATE INDEX idx_imaging_date
ON Imaging_Reports(Imaging_Date);

CREATE INDEX idx_imaging_status
ON Imaging_Reports(Report_Status);

CREATE INDEX idx_imaging_ai
ON Imaging_Reports(AI_Analysis_Performed);

CREATE INDEX idx_imaging_risk
ON Imaging_Reports(AI_Risk_Level);

CREATE INDEX idx_imaging_active
ON Imaging_Reports(Is_Active);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Imaging_Reports;