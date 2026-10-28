/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 29_Create_Medical_Procedures_Table.sql

Purpose : Create Medical Procedures Transaction Table

Description:
Stores all medical and surgical procedures performed
for patients including procedure details, AI support,
doctor information, outcomes and dataset tracking.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Medical_Procedures;

CREATE TABLE Medical_Procedures (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Procedure_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),


    -- =====================================================
    -- Foreign Keys
    -- =====================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36)
        NOT NULL,

    Admission_ID CHAR(36),

    Diagnosis_ID CHAR(36),

    Department_ID CHAR(36),


    -- =====================================================
    -- Procedure Information
    -- =====================================================

    Procedure_Number VARCHAR(30)
        NOT NULL UNIQUE,

    Procedure_Code VARCHAR(30)
        UNIQUE,

    Procedure_Name VARCHAR(200)
        NOT NULL,

    Procedure_Category ENUM(
        'Surgical',
        'Diagnostic',
        'Therapeutic',
        'Emergency',
        'Minimally Invasive',
        'Other'
    )
    NOT NULL,

    Procedure_Date DATETIME
        NOT NULL,

    Duration_Minutes INT
        DEFAULT 30,

    Procedure_Status ENUM(
        'Scheduled',
        'In Progress',
        'Completed',
        'Cancelled'
    )
    DEFAULT 'Scheduled',

    Priority ENUM(
        'Low',
        'Medium',
        'High',
        'Emergency'
    )
    DEFAULT 'Medium',

    Operation_Theater VARCHAR(100),

    Anaesthetist VARCHAR(150),

    Assistant_Surgeon VARCHAR(150),

    Anaesthesia_Type ENUM(
        'General',
        'Local',
        'Regional',
        'Sedation',
        'None'
    ),

    Procedure_Cost DECIMAL(12,2),

    Complications TEXT,

    Procedure_Outcome TEXT,

    Follow_Up_Required BOOLEAN
        DEFAULT FALSE,

    Notes TEXT,


    -- =====================================================
    -- AI Support
    -- =====================================================

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

    AI_Recommendation TEXT,

    AI_Confidence DECIMAL(5,2),


    -- =====================================================
    -- Dataset Tracking
    -- =====================================================

    Data_Source ENUM(
        'MIMIC-IV',
        'Synthetic',
        'Hospital_Records',
        'Hybrid Dataset'
    )
    DEFAULT 'Synthetic',


    -- =====================================================
    -- Status Information
    -- =====================================================

    Is_Active BOOLEAN
        DEFAULT TRUE,

    Is_Deleted BOOLEAN
        DEFAULT FALSE,

    Record_Version INT
        DEFAULT 1,


    -- =====================================================
    -- Audit Information
    -- =====================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,


    -- =====================================================
    -- Constraints
    -- =====================================================

    CONSTRAINT fk_medproc_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_medproc_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_medproc_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_medproc_diagnosis
        FOREIGN KEY (Diagnosis_ID)
        REFERENCES Diagnoses(Diagnosis_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_medproc_department
        FOREIGN KEY (Department_ID)
        REFERENCES Departments(Department_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT chk_medproc_duration
        CHECK (Duration_Minutes > 0),

    CONSTRAINT chk_medproc_cost
        CHECK (
            Procedure_Cost IS NULL
            OR Procedure_Cost >= 0
        )

);


-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX idx_medproc_number
ON Medical_Procedures(Procedure_Number);

CREATE INDEX idx_medproc_patient
ON Medical_Procedures(Patient_ID);

CREATE INDEX idx_medproc_doctor
ON Medical_Procedures(Doctor_ID);

CREATE INDEX idx_medproc_department
ON Medical_Procedures(Department_ID);

CREATE INDEX idx_medproc_admission
ON Medical_Procedures(Admission_ID);

CREATE INDEX idx_medproc_diagnosis
ON Medical_Procedures(Diagnosis_ID);

CREATE INDEX idx_medproc_date
ON Medical_Procedures(Procedure_Date);

CREATE INDEX idx_medproc_category
ON Medical_Procedures(Procedure_Category);

CREATE INDEX idx_medproc_status
ON Medical_Procedures(Procedure_Status);

CREATE INDEX idx_medproc_priority
ON Medical_Procedures(Priority);

CREATE INDEX idx_medproc_ai
ON Medical_Procedures(AI_Risk_Level);


-- =====================================================
-- Verification
-- =====================================================

SHOW TABLES;

DESCRIBE Medical_Procedures;