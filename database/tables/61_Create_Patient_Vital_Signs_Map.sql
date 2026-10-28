/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 61_Create_Patient_Vital_Signs_Map.sql

Purpose : Create Patient Vital Signs Mapping Table

Description:
Stores the relationship between patients and their vital-sign
records. This mapping captures physiological measurements,
recording information, measurement source, clinical assessment,
AI risk level, early warning score, and status information.

Version : 2.3
===========================================================
*/

USE healthcare_ai_db;


-- ==========================================================
-- Remove Existing Table
-- Warning: This deletes any existing data from this table.
-- ==========================================================

DROP TABLE IF EXISTS Patient_Vital_Signs_Map;


-- ==========================================================
-- Create Patient Vital Signs Mapping Table
-- ==========================================================

CREATE TABLE Patient_Vital_Signs_Map (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Vital_Signs_Map_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Key References
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Vital_Record_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36)
        NULL,

    ICU_Stay_ID CHAR(36)
        NULL,


    -- ======================================================
    -- Recording Information
    -- ======================================================

    Recorded_DateTime DATETIME
        NOT NULL,

    Recorded_By VARCHAR(100)
        NULL,

    Device_ID VARCHAR(100)
        NULL,

    Device_Type VARCHAR(100)
        NULL,

    Measurement_Source ENUM(
        'Manual',
        'Monitor',
        'Wearable Device',
        'ICU Monitor'
    )
        NOT NULL DEFAULT 'Manual',


    -- ======================================================
    -- Vital Parameters
    -- ======================================================

    Temperature_C DECIMAL(4,1)
        NULL,

    Heart_Rate_BPM INT
        NULL,

    Respiratory_Rate INT
        NULL,

    Oxygen_Saturation DECIMAL(5,2)
        NULL,

    Blood_Pressure_Systolic INT
        NULL,

    Blood_Pressure_Diastolic INT
        NULL,

    Mean_Arterial_Pressure DECIMAL(5,2)
        NULL,

    Pulse_Rate INT
        NULL,

    Height_cm DECIMAL(6,2)
        NULL,

    Weight_kg DECIMAL(6,2)
        NULL,

    BMI DECIMAL(5,2)
        NULL,

    Blood_Glucose DECIMAL(6,2)
        NULL,

    Pain_Score INT
        NULL,

    Glasgow_Coma_Scale INT
        NULL,

    Body_Surface_Area DECIMAL(5,2)
        NULL,


    -- ======================================================
    -- Clinical Assessment
    -- ======================================================

    Abnormal_Flag BOOLEAN
        NOT NULL DEFAULT FALSE,

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
        NOT NULL DEFAULT 'Low',

    Early_Warning_Score INT
        NULL,

    Clinical_Remarks TEXT
        NULL,

    Notes TEXT
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

    CONSTRAINT chk_pvsm_temperature
        CHECK (
            Temperature_C IS NULL
            OR Temperature_C BETWEEN 25 AND 45
        ),


    CONSTRAINT chk_pvsm_heart_rate
        CHECK (
            Heart_Rate_BPM IS NULL
            OR Heart_Rate_BPM BETWEEN 20 AND 250
        ),


    CONSTRAINT chk_pvsm_respiratory_rate
        CHECK (
            Respiratory_Rate IS NULL
            OR Respiratory_Rate BETWEEN 5 AND 100
        ),


    CONSTRAINT chk_pvsm_oxygen_saturation
        CHECK (
            Oxygen_Saturation IS NULL
            OR Oxygen_Saturation BETWEEN 0 AND 100
        ),


    CONSTRAINT chk_pvsm_systolic_bp
        CHECK (
            Blood_Pressure_Systolic IS NULL
            OR Blood_Pressure_Systolic BETWEEN 40 AND 300
        ),


    CONSTRAINT chk_pvsm_diastolic_bp
        CHECK (
            Blood_Pressure_Diastolic IS NULL
            OR Blood_Pressure_Diastolic BETWEEN 20 AND 200
        ),


    CONSTRAINT chk_pvsm_map
        CHECK (
            Pulse_Rate IS NULL
            OR Pulse_Rate BETWEEN 20 AND 250
        ),


    CONSTRAINT chk_pvsm_height
        CHECK (
            Height_cm IS NULL
            OR Height_cm > 0
        ),


    CONSTRAINT chk_pvsm_weight
        CHECK (
            Weight_kg IS NULL
            OR Weight_kg > 0
        ),


    CONSTRAINT chk_pvsm_bmi
        CHECK (
            BMI IS NULL
            OR BMI > 0
        ),


    CONSTRAINT chk_pvsm_glucose
        CHECK (
            Blood_Glucose IS NULL
            OR Blood_Glucose >= 0
        ),


    CONSTRAINT chk_pvsm_pain_score
        CHECK (
            Pain_Score IS NULL
            OR Pain_Score BETWEEN 0 AND 10
        ),


    CONSTRAINT chk_pvsm_gcs
        CHECK (
            Glasgow_Coma_Scale IS NULL
            OR Glasgow_Coma_Scale BETWEEN 3 AND 15
        ),


    CONSTRAINT chk_pvsm_bsa
        CHECK (
            Body_Surface_Area IS NULL
            OR Body_Surface_Area > 0
        ),


    CONSTRAINT chk_pvsm_early_warning
        CHECK (
            Early_Warning_Score IS NULL
            OR Early_Warning_Score >= 0
        ),


    CONSTRAINT chk_pvsm_record_version
        CHECK (
            Record_Version >= 1
        ),


    -- ======================================================
    -- Foreign Key Constraints
    -- Unique constraint names are used to prevent
    -- conflicts with existing database constraints.
    -- ======================================================

    CONSTRAINT fk_pvsm_map_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,


    CONSTRAINT fk_pvsm_map_vital_record
        FOREIGN KEY (Vital_Record_ID)
        REFERENCES Vital_Signs(Vital_Record_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,


    CONSTRAINT fk_pvsm_map_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Duplicate Record Prevention
    -- Each vital-sign record can appear only once.
    -- ======================================================

    CONSTRAINT uk_pvsm_map_vital_record
        UNIQUE (
            Vital_Record_ID
        )

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_pvsm_map_patient
    ON Patient_Vital_Signs_Map(Patient_ID);

CREATE INDEX idx_pvsm_map_doctor
    ON Patient_Vital_Signs_Map(Doctor_ID);

CREATE INDEX idx_pvsm_map_icu_stay
    ON Patient_Vital_Signs_Map(ICU_Stay_ID);

CREATE INDEX idx_pvsm_map_datetime
    ON Patient_Vital_Signs_Map(Recorded_DateTime);

CREATE INDEX idx_pvsm_map_source
    ON Patient_Vital_Signs_Map(Measurement_Source);

CREATE INDEX idx_pvsm_map_heart_rate
    ON Patient_Vital_Signs_Map(Heart_Rate_BPM);

CREATE INDEX idx_pvsm_map_temperature
    ON Patient_Vital_Signs_Map(Temperature_C);

CREATE INDEX idx_pvsm_map_oxygen
    ON Patient_Vital_Signs_Map(Oxygen_Saturation);

CREATE INDEX idx_pvsm_map_blood_pressure
    ON Patient_Vital_Signs_Map(
        Blood_Pressure_Systolic,
        Blood_Pressure_Diastolic
    );

CREATE INDEX idx_pvsm_map_abnormal
    ON Patient_Vital_Signs_Map(Abnormal_Flag);

CREATE INDEX idx_pvsm_map_ai_risk
    ON Patient_Vital_Signs_Map(AI_Risk_Level);

CREATE INDEX idx_pvsm_map_active
    ON Patient_Vital_Signs_Map(Is_Active);

CREATE INDEX idx_pvsm_map_data_source
    ON Patient_Vital_Signs_Map(Data_Source);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Patient_Vital_Signs_Map;