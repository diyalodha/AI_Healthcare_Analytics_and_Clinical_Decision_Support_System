/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 62_Create_Patient_Procedures_Map.sql

Purpose : Create Patient Medical Procedures Mapping Table

Description:
Stores the relationship between patients and medical procedure
records. Captures procedure details, doctors, admissions,
diagnoses, departments, procedure status, priority, cost,
outcomes, complications, AI risk assessment and dataset source.

Version : 2.4
===========================================================
*/

USE healthcare_ai_db;


-- ==========================================================
-- Remove Existing Table
-- Warning: This deletes existing data from this table.
-- ==========================================================

DROP TABLE IF EXISTS Patient_Procedures_Map;


-- ==========================================================
-- Create Patient Procedures Mapping Table
-- ==========================================================

CREATE TABLE Patient_Procedures_Map (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Procedure_Map_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Key References
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Procedure_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36)
        NOT NULL,

    Admission_ID CHAR(36)
        NULL,

    Diagnosis_ID CHAR(36)
        NULL,

    Department_ID CHAR(36)
        NULL,


    -- ======================================================
    -- Procedure Identification
    -- ======================================================

    Procedure_Number VARCHAR(30)
        NOT NULL,

    Procedure_Code VARCHAR(30)
        NULL,


    -- ======================================================
    -- Procedure Information
    -- ======================================================

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
        NOT NULL DEFAULT 30,

    Procedure_Status ENUM(
        'Scheduled',
        'In Progress',
        'Completed',
        'Cancelled'
    )
        NOT NULL DEFAULT 'Scheduled',

    Priority ENUM(
        'Low',
        'Medium',
        'High',
        'Emergency'
    )
        NOT NULL DEFAULT 'Medium',


    -- ======================================================
    -- Procedure Execution Details
    -- ======================================================

    Operation_Theater VARCHAR(100)
        NULL,

    Anaesthetist VARCHAR(150)
        NULL,

    Assistant_Surgeon VARCHAR(150)
        NULL,

    Anaesthesia_Type ENUM(
        'General',
        'Local',
        'Regional',
        'Sedation',
        'None'
    )
        NULL,


    -- ======================================================
    -- Financial and Outcome Information
    -- ======================================================

    Procedure_Cost DECIMAL(12,2)
        NULL,

    Complications TEXT
        NULL,

    Procedure_Outcome TEXT
        NULL,

    Follow_Up_Required BOOLEAN
        NOT NULL DEFAULT FALSE,

    Notes TEXT
        NULL,


    -- ======================================================
    -- AI Decision Support
    -- ======================================================

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
        NOT NULL DEFAULT 'Low',

    AI_Recommendation TEXT
        NULL,

    AI_Confidence DECIMAL(5,2)
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

    CONSTRAINT chk_ppm_duration
        CHECK (
            Duration_Minutes > 0
        ),

    CONSTRAINT chk_ppm_cost
        CHECK (
            Procedure_Cost IS NULL
            OR Procedure_Cost >= 0
        ),

    CONSTRAINT chk_ppm_ai_confidence
        CHECK (
            AI_Confidence IS NULL
            OR AI_Confidence BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_ppm_record_version
        CHECK (
            Record_Version >= 1
        ),


    -- ======================================================
    -- Foreign Key Constraints
    --
    -- IMPORTANT:
    -- Constraint names are globally unique within the
    -- database to avoid MySQL Error 1826.
    -- ======================================================

    CONSTRAINT fk_ppm62_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_ppm62_procedure
        FOREIGN KEY (Procedure_ID)
        REFERENCES Medical_Procedures(Procedure_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_ppm62_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_ppm62_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_ppm62_diagnosis
        FOREIGN KEY (Diagnosis_ID)
        REFERENCES Diagnoses(Diagnosis_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_ppm62_department
        FOREIGN KEY (Department_ID)
        REFERENCES Departments(Department_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Duplicate Record Prevention
    -- Each medical procedure can appear only once.
    -- ======================================================

    CONSTRAINT uk_ppm62_procedure
        UNIQUE (
            Procedure_ID
        )

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_ppm62_patient
    ON Patient_Procedures_Map(Patient_ID);

CREATE INDEX idx_ppm62_procedure
    ON Patient_Procedures_Map(Procedure_ID);

CREATE INDEX idx_ppm62_procedure_number
    ON Patient_Procedures_Map(Procedure_Number);

CREATE INDEX idx_ppm62_procedure_code
    ON Patient_Procedures_Map(Procedure_Code);

CREATE INDEX idx_ppm62_doctor
    ON Patient_Procedures_Map(Doctor_ID);

CREATE INDEX idx_ppm62_admission
    ON Patient_Procedures_Map(Admission_ID);

CREATE INDEX idx_ppm62_diagnosis
    ON Patient_Procedures_Map(Diagnosis_ID);

CREATE INDEX idx_ppm62_department
    ON Patient_Procedures_Map(Department_ID);

CREATE INDEX idx_ppm62_date
    ON Patient_Procedures_Map(Procedure_Date);

CREATE INDEX idx_ppm62_category
    ON Patient_Procedures_Map(Procedure_Category);

CREATE INDEX idx_ppm62_status
    ON Patient_Procedures_Map(Procedure_Status);

CREATE INDEX idx_ppm62_priority
    ON Patient_Procedures_Map(Priority);

CREATE INDEX idx_ppm62_ai_risk
    ON Patient_Procedures_Map(AI_Risk_Level);

CREATE INDEX idx_ppm62_followup
    ON Patient_Procedures_Map(Follow_Up_Required);

CREATE INDEX idx_ppm62_active
    ON Patient_Procedures_Map(Is_Active);

CREATE INDEX idx_ppm62_data_source
    ON Patient_Procedures_Map(Data_Source);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Patient_Procedures_Map;