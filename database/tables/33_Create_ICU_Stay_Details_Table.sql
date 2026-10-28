/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 33_Create_ICU_Stay_Details_Table.sql

Purpose : Create ICU Stay Details Table

Description:
Stores ICU admission details including severity scores,
critical care support requirements, monitoring data,
clinical outcomes, and AI-ready ICU analytics.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

-- ==========================================================
-- Create ICU Stay Details Table
-- ==========================================================

CREATE TABLE IF NOT EXISTS ICU_Stay_Details (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    ICU_Stay_ID CHAR(36)
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

    Room_ID CHAR(36),

    Bed_ID CHAR(36),


    -- ======================================================
    -- ICU Stay Information
    -- ======================================================

    ICU_Stay_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    ICU_Type ENUM(
        'Medical',
        'Surgical',
        'Cardiac',
        'Neonatal',
        'Pediatric',
        'Trauma'
    )
    NOT NULL,

    Admission_DateTime DATETIME
        NOT NULL,

    Discharge_DateTime DATETIME,

    Length_Of_Stay_Days DECIMAL(6,2),

    Admission_Reason TEXT,


    -- ======================================================
    -- Critical Care Monitoring
    -- ======================================================

    Ventilator_Required BOOLEAN
        DEFAULT FALSE,

    Oxygen_Support BOOLEAN
        DEFAULT FALSE,

    Dialysis_Required BOOLEAN
        DEFAULT FALSE,

    Vasopressor_Required BOOLEAN
        DEFAULT FALSE,

    APACHE_II_Score INT,

    SOFA_Score INT,

    GCS_Score INT,

    Infection_Status ENUM(
        'None',
        'Suspected',
        'Confirmed'
    )
    DEFAULT 'None',

    ICU_Outcome ENUM(
        'Recovered',
        'Transferred',
        'Expired'
    ),

    Clinical_Notes TEXT,


    -- ======================================================
    -- AI & Analytics
    -- ======================================================

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

    Mortality_Risk_Percentage DECIMAL(5,2),

    Readmission_Risk ENUM(
        'Low',
        'Medium',
        'High'
    )
    DEFAULT 'Low',

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

    CONSTRAINT fk_icu_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_icu_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_icu_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_icu_room
        FOREIGN KEY (Room_ID)
        REFERENCES Hospital_Rooms(Room_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_icu_bed
        FOREIGN KEY (Bed_ID)
        REFERENCES Beds(Bed_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Check Constraints
    -- ======================================================

    CONSTRAINT chk_icu_dates
        CHECK (
            Discharge_DateTime IS NULL
            OR Discharge_DateTime >= Admission_DateTime
        ),

    CONSTRAINT chk_apache_score
        CHECK (
            APACHE_II_Score IS NULL
            OR APACHE_II_Score BETWEEN 0 AND 71
        ),

    CONSTRAINT chk_sofa_score
        CHECK (
            SOFA_Score IS NULL
            OR SOFA_Score BETWEEN 0 AND 24
        ),

    CONSTRAINT chk_gcs_score
        CHECK (
            GCS_Score IS NULL
            OR GCS_Score BETWEEN 3 AND 15
        ),

    CONSTRAINT chk_mortality_risk
        CHECK (
            Mortality_Risk_Percentage IS NULL
            OR Mortality_Risk_Percentage BETWEEN 0 AND 100
        )

);

-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_icu_number
ON ICU_Stay_Details(ICU_Stay_Number);

CREATE INDEX idx_icu_patient
ON ICU_Stay_Details(Patient_ID);

CREATE INDEX idx_icu_admission
ON ICU_Stay_Details(Admission_ID);

CREATE INDEX idx_icu_doctor
ON ICU_Stay_Details(Doctor_ID);

CREATE INDEX idx_icu_room
ON ICU_Stay_Details(Room_ID);

CREATE INDEX idx_icu_bed
ON ICU_Stay_Details(Bed_ID);

CREATE INDEX idx_icu_type
ON ICU_Stay_Details(ICU_Type);

CREATE INDEX idx_icu_outcome
ON ICU_Stay_Details(ICU_Outcome);

CREATE INDEX idx_icu_risk
ON ICU_Stay_Details(AI_Risk_Level);

CREATE INDEX idx_icu_active
ON ICU_Stay_Details(Is_Active);

-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE ICU_Stay_Details;