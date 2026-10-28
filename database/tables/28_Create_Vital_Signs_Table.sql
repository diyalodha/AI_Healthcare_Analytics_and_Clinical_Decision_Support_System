/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 28_Create_Vital_Signs_Table.sql

Purpose : Create Vital Signs Table

Description :
Stores patient vital signs collected from hospital
monitoring systems, ICU devices and wearable devices.
Supports AI analytics, early warning scores and
clinical decision support.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Vital_Signs;

CREATE TABLE Vital_Signs (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Vital_Record_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),

    -- =====================================================
    -- Foreign Keys
    -- =====================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36),

    ICU_Stay_ID CHAR(36),

    -- =====================================================
    -- Recording Information
    -- =====================================================

    Recorded_DateTime DATETIME
        NOT NULL,

    Recorded_By VARCHAR(100),

    Device_ID VARCHAR(100),

    Device_Type VARCHAR(100),

    Measurement_Source ENUM(
        'Manual',
        'Monitor',
        'Wearable Device',
        'ICU Monitor'
    )
    DEFAULT 'Manual',

    -- =====================================================
    -- Vital Parameters
    -- =====================================================

    Temperature_C DECIMAL(4,1),

    Heart_Rate_BPM INT,

    Respiratory_Rate INT,

    Oxygen_Saturation DECIMAL(5,2),

    Blood_Pressure_Systolic INT,

    Blood_Pressure_Diastolic INT,

    Mean_Arterial_Pressure DECIMAL(5,2),

    Pulse_Rate INT,

    Height_cm DECIMAL(6,2),

    Weight_kg DECIMAL(6,2),

    BMI DECIMAL(5,2),

    Blood_Glucose DECIMAL(6,2),

    Pain_Score INT,

    Glasgow_Coma_Scale INT,

    Body_Surface_Area DECIMAL(5,2),

    -- =====================================================
    -- Clinical Assessment
    -- =====================================================

    Abnormal_Flag BOOLEAN
        DEFAULT FALSE,

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

    Early_Warning_Score INT,

    Clinical_Remarks TEXT,

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

    CONSTRAINT fk_vitals_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_vitals_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    -- =====================================================
    -- Check Constraints
    -- =====================================================

    CONSTRAINT chk_temperature
        CHECK (
            Temperature_C IS NULL
            OR Temperature_C BETWEEN 25 AND 45
        ),

    CONSTRAINT chk_heart_rate
        CHECK (
            Heart_Rate_BPM IS NULL
            OR Heart_Rate_BPM BETWEEN 20 AND 250
        ),

    CONSTRAINT chk_pain_score
        CHECK (
            Pain_Score IS NULL
            OR Pain_Score BETWEEN 0 AND 10
        ),

    CONSTRAINT chk_gcs
        CHECK (
            Glasgow_Coma_Scale IS NULL
            OR Glasgow_Coma_Scale BETWEEN 3 AND 15
        )

);

-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX idx_vitals_patient
ON Vital_Signs(Patient_ID);

CREATE INDEX idx_vitals_datetime
ON Vital_Signs(Recorded_DateTime);

CREATE INDEX idx_vitals_doctor
ON Vital_Signs(Doctor_ID);

CREATE INDEX idx_vitals_bp
ON Vital_Signs(
    Blood_Pressure_Systolic,
    Blood_Pressure_Diastolic
);

CREATE INDEX idx_vitals_heart_rate
ON Vital_Signs(Heart_Rate_BPM);

CREATE INDEX idx_vitals_temperature
ON Vital_Signs(Temperature_C);

CREATE INDEX idx_vitals_ai_risk
ON Vital_Signs(AI_Risk_Level);

CREATE INDEX idx_vitals_abnormal
ON Vital_Signs(Abnormal_Flag);

CREATE INDEX idx_vitals_source
ON Vital_Signs(Data_Source);

-- =====================================================
-- Verification
-- =====================================================

SHOW TABLES;

DESCRIBE Vital_Signs;