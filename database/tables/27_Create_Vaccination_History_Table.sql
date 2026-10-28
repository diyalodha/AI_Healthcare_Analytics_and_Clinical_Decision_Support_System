/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 27_Create_Vaccination_History_Table.sql

Purpose : Create Vaccination History Table

Description :
Stores complete vaccination history including vaccine
details, dosage schedule, immunity status, adverse
events, verification and AI analytics support.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Vaccination_History;

CREATE TABLE Vaccination_History (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Vaccination_Record_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),

    -- =====================================================
    -- Foreign Keys
    -- =====================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Vaccine_ID CHAR(36),

    Administered_By_Doctor_ID CHAR(36),

    -- =====================================================
    -- Vaccine Information
    -- =====================================================

    Vaccine_Name VARCHAR(150)
        NOT NULL,

    Vaccine_Code VARCHAR(30),

    Vaccine_Category ENUM(
        'Childhood',
        'Adult',
        'Travel',
        'COVID-19',
        'Influenza',
        'Other'
    )
    NOT NULL,

    Manufacturer VARCHAR(150),

    Batch_Number VARCHAR(100),

    Dose_Number INT
        NOT NULL,

    Total_Doses_Required INT,

    Vaccination_Date DATE
        NOT NULL,

    Next_Due_Date DATE,

    Injection_Site VARCHAR(50),

    Route ENUM(
        'Intramuscular',
        'Subcutaneous',
        'Oral',
        'Intradermal',
        'Other'
    ),

    Hospital_Name VARCHAR(150),

    Vaccination_Status ENUM(
        'Completed',
        'Pending',
        'Booster Due'
    )
    DEFAULT 'Completed',

    Immunity_Status ENUM(
        'Active',
        'Expired',
        'Unknown'
    )
    DEFAULT 'Active',

    Adverse_Reaction TEXT,

    Observation_Period_Minutes INT
        DEFAULT 30,

    Notes TEXT,

    -- =====================================================
    -- Verification
    -- =====================================================

    Verification_Status ENUM(
        'Pending',
        'Verified',
        'Rejected'
    )
    DEFAULT 'Verified',

    Verified_By VARCHAR(100),

    Verification_Date DATE,

    -- =====================================================
    -- AI Analytics
    -- =====================================================

    AI_Immunity_Prediction BOOLEAN
        DEFAULT FALSE,

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

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
    -- Foreign Keys
    -- =====================================================

    CONSTRAINT fk_vaccine_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_vaccine_doctor
        FOREIGN KEY (Administered_By_Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    -- =====================================================
    -- Check Constraints
    -- =====================================================

    CONSTRAINT chk_dose_number
        CHECK (Dose_Number > 0),

    CONSTRAINT chk_total_doses
        CHECK (
            Total_Doses_Required IS NULL
            OR Total_Doses_Required > 0
        ),

    CONSTRAINT chk_observation_period
        CHECK (Observation_Period_Minutes >= 0)

);

-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX idx_vaccine_patient
ON Vaccination_History(Patient_ID);

CREATE INDEX idx_vaccine_name
ON Vaccination_History(Vaccine_Name);

CREATE INDEX idx_vaccine_code
ON Vaccination_History(Vaccine_Code);

CREATE INDEX idx_vaccine_date
ON Vaccination_History(Vaccination_Date);

CREATE INDEX idx_vaccine_status
ON Vaccination_History(Vaccination_Status);

CREATE INDEX idx_immunity_status
ON Vaccination_History(Immunity_Status);

CREATE INDEX idx_ai_risk
ON Vaccination_History(AI_Risk_Level);

CREATE INDEX idx_verification_status
ON Vaccination_History(Verification_Status);

-- =====================================================
-- Verification
-- =====================================================

SHOW TABLES;

DESCRIBE Vaccination_History;