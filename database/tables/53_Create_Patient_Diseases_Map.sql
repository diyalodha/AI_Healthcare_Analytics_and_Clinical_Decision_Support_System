/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 53_Create_Patient_Diseases_Map.sql

Purpose : Create Patient-Disease Mapping Table

Description:
Stores the relationship between patients and diseases,
including disease history, severity, status, diagnosis
source, treating doctor and AI risk analytics.

Version : 2.2

Author  : Diya Lodha & Team
===========================================================
*/


USE healthcare_ai_db;


-- ==========================================================
-- Remove Existing Table
-- ==========================================================

DROP TABLE IF EXISTS Patient_Diseases_Map;


-- ==========================================================
-- Create Patient Diseases Mapping Table
-- ==========================================================

CREATE TABLE Patient_Diseases_Map (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Patient_Disease_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Patient & Disease References
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Disease_ID CHAR(36)
        NOT NULL,

    Diagnosed_By_Doctor_ID CHAR(36),


    -- ======================================================
    -- Disease Information
    -- ======================================================

    Diagnosis_Date DATE
        NOT NULL,

    Disease_Status ENUM(
        'Active',
        'Resolved',
        'Chronic',
        'Remission',
        'Suspected'
    )
        DEFAULT 'Active',

    Disease_Severity ENUM(
        'Mild',
        'Moderate',
        'Severe',
        'Critical'
    ),

    Is_Primary_Disease BOOLEAN
        DEFAULT FALSE,

    Is_Chronic BOOLEAN
        DEFAULT FALSE,

    Is_Hereditary BOOLEAN
        DEFAULT FALSE,


    -- ======================================================
    -- Diagnosis Information
    -- ======================================================

    Diagnosis_Source ENUM(
        'Clinical Diagnosis',
        'Laboratory Test',
        'Imaging',
        'AI Prediction',
        'Patient History',
        'Other'
    )
        DEFAULT 'Clinical Diagnosis',

    Symptoms_At_Diagnosis TEXT,

    Treatment_Summary TEXT,

    Clinical_Notes TEXT,


    -- ======================================================
    -- Disease Timeline
    -- ======================================================

    Resolution_Date DATE,

    Last_Reviewed_Date DATE,


    -- ======================================================
    -- AI Analytics
    -- ======================================================

    AI_Risk_Score DECIMAL(5,2),

    AI_Progression_Risk DECIMAL(5,2),

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
    -- Validation Constraints
    -- ======================================================

    CONSTRAINT CHK_PatientDisease_Risk
        CHECK (
            AI_Risk_Score IS NULL
            OR (
                AI_Risk_Score >= 0
                AND AI_Risk_Score <= 100
            )
        ),


    CONSTRAINT CHK_PatientDisease_Progression
        CHECK (
            AI_Progression_Risk IS NULL
            OR (
                AI_Progression_Risk >= 0
                AND AI_Progression_Risk <= 100
            )
        ),


    CONSTRAINT CHK_PatientDisease_Resolution
        CHECK (
            Resolution_Date IS NULL
            OR Resolution_Date >= Diagnosis_Date
        ),


    -- ======================================================
    -- Foreign Key Constraints
    -- ======================================================

    CONSTRAINT FK_PatientDisease_Patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,


    CONSTRAINT FK_PatientDisease_Disease
        FOREIGN KEY (Disease_ID)
        REFERENCES Diseases(Disease_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,


    CONSTRAINT FK_PatientDisease_Doctor
        FOREIGN KEY (Diagnosed_By_Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Prevent Duplicate Records
    -- ======================================================

    CONSTRAINT UK_Patient_Disease_Date
        UNIQUE (
            Patient_ID,
            Disease_ID,
            Diagnosis_Date
        )

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX IDX_PatientDisease_Patient
ON Patient_Diseases_Map(Patient_ID);


CREATE INDEX IDX_PatientDisease_Disease
ON Patient_Diseases_Map(Disease_ID);


CREATE INDEX IDX_PatientDisease_Doctor
ON Patient_Diseases_Map(Diagnosed_By_Doctor_ID);


CREATE INDEX IDX_PatientDisease_Status
ON Patient_Diseases_Map(Disease_Status);


CREATE INDEX IDX_PatientDisease_DiagnosisDate
ON Patient_Diseases_Map(Diagnosis_Date);


CREATE INDEX IDX_PatientDisease_Chronic
ON Patient_Diseases_Map(Is_Chronic);


CREATE INDEX IDX_PatientDisease_Risk
ON Patient_Diseases_Map(AI_Risk_Score);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Patient_Diseases_Map;