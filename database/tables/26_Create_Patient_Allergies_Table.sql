/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 26_Create_Patient_Allergies_Table.sql

Purpose : Create Patient Allergies Table

Description:
Stores complete patient allergy information including
severity, reactions, verification, emergency risk,
AI analytics support and audit tracking.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Patient_Allergies;

CREATE TABLE Patient_Allergies (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Allergy_Record_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),

    -- =====================================================
    -- Foreign Keys
    -- =====================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Diagnosed_By_Doctor_ID CHAR(36),

    Verified_By_Doctor_ID CHAR(36),

    -- =====================================================
    -- Allergy Information
    -- =====================================================

    Allergy_Name VARCHAR(150)
        NOT NULL,

    Allergen_Code VARCHAR(30),

    Allergy_Category ENUM(
        'Drug',
        'Food',
        'Environmental',
        'Insect',
        'Latex',
        'Chemical',
        'Other'
    )
    NOT NULL,

    Allergy_Severity ENUM(
        'Mild',
        'Moderate',
        'Severe',
        'Life-Threatening'
    )
    NOT NULL,

    Reaction_Severity_Score INT
        DEFAULT 1,

    Reaction TEXT,

    Symptoms TEXT,

    Treatment_Advice TEXT,

    Trigger_Factors TEXT,

    First_Observed_Date DATE,

    Last_Reaction_Date DATE,

    Requires_Emergency_Care BOOLEAN
        DEFAULT FALSE,

    Is_Chronic BOOLEAN
        DEFAULT FALSE,

    Is_Active BOOLEAN
        DEFAULT TRUE,

    Is_Deleted BOOLEAN
        DEFAULT FALSE,

    -- =====================================================
    -- Doctor Verification
    -- =====================================================

    Verification_Status ENUM(
        'Pending',
        'Verified',
        'Rejected'
    )
    DEFAULT 'Pending',

    Last_Verified_Date DATE,

    Notes TEXT,

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
    -- Foreign Keys
    -- =====================================================

    CONSTRAINT fk_allergy_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_allergy_doctor
        FOREIGN KEY (Diagnosed_By_Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_allergy_verified_doctor
        FOREIGN KEY (Verified_By_Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    -- =====================================================
    -- Check Constraints
    -- =====================================================

    CONSTRAINT chk_allergy_severity_score
        CHECK (
            Reaction_Severity_Score BETWEEN 1 AND 10
        )

);

-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX idx_allergy_patient
ON Patient_Allergies(Patient_ID);

CREATE INDEX idx_allergy_name
ON Patient_Allergies(Allergy_Name);

CREATE INDEX idx_allergy_category
ON Patient_Allergies(Allergy_Category);

CREATE INDEX idx_allergy_status
ON Patient_Allergies(Is_Active);

CREATE INDEX idx_allergy_verification
ON Patient_Allergies(Verification_Status);

CREATE INDEX idx_allergy_doctor
ON Patient_Allergies(Diagnosed_By_Doctor_ID);

CREATE INDEX idx_allergy_verified_doctor
ON Patient_Allergies(Verified_By_Doctor_ID);

-- =====================================================
-- Verification
-- =====================================================

SHOW TABLES;

DESCRIBE Patient_Allergies;