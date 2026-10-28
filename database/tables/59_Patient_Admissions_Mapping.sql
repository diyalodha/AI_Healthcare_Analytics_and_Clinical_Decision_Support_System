/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 59_Create_Patient_Admissions_Map.sql

Purpose : Create Patient Admissions Mapping Table

Description:
Stores the relationship between patients and their hospital
admissions. This mapping captures admission details, admission
type, department, admitting doctor, room and bed allocation,
discharge information, clinical indicators, AI risk level,
and admission status.

Version : 2.2
===========================================================
*/

USE healthcare_ai_db;


-- ==========================================================
-- Remove Existing Table
-- Warning: This deletes existing data from this table.
-- ==========================================================

DROP TABLE IF EXISTS Patient_Admissions_Map;


-- ==========================================================
-- Create Patient Admissions Mapping Table
-- ==========================================================

CREATE TABLE Patient_Admissions_Map (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Admission_Map_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Key References
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Admission_ID CHAR(36)
        NOT NULL,

    Department_ID CHAR(36)
        NOT NULL,

    Admitting_Doctor_ID CHAR(36)
        NOT NULL,

    Predicted_Disease_ID CHAR(36)
        NULL,


    -- ======================================================
    -- Room and Bed References
    --
    -- Room_ID and Bed_ID are retained from Admissions.
    -- They are not foreign keys because the current project
    -- schema does not contain Rooms/Beds master tables.
    -- ======================================================

    Room_ID CHAR(36)
        NULL,

    Bed_ID CHAR(36)
        NULL,


    -- ======================================================
    -- Admission Identification
    -- ======================================================

    Admission_Number VARCHAR(30)
        NOT NULL,


    -- ======================================================
    -- Admission Dates
    -- ======================================================

    Admission_Date DATETIME
        NOT NULL,

    Expected_Discharge_Date DATE
        NULL,

    Actual_Discharge_Date DATE
        NULL,


    -- ======================================================
    -- Admission Classification
    -- ======================================================

    Admission_Type ENUM(
        'Emergency',
        'Routine',
        'Referral',
        'Transfer'
    )
        NOT NULL,

    Admission_Reason TEXT
        NULL,

    Initial_Diagnosis TEXT
        NULL,


    -- ======================================================
    -- Hospital Location
    -- ======================================================

    Ward VARCHAR(100)
        NULL,

    Room_Number VARCHAR(20)
        NULL,

    Bed_Number VARCHAR(20)
        NULL,


    -- ======================================================
    -- Admission Status
    -- ======================================================

    Current_Status ENUM(
        'Admitted',
        'Under Observation',
        'ICU',
        'Discharged',
        'Transferred',
        'Expired'
    )
        NOT NULL DEFAULT 'Admitted',

    Length_of_Stay INT
        NULL,


    -- ======================================================
    -- Clinical Indicators
    -- ======================================================

    Is_ICU_Admission BOOLEAN
        NOT NULL DEFAULT FALSE,

    Requires_Surgery BOOLEAN
        NOT NULL DEFAULT FALSE,

    Is_Emergency BOOLEAN
        NOT NULL DEFAULT FALSE,


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


    -- ======================================================
    -- Additional Information
    -- ======================================================

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

    CONSTRAINT chk_pam_length_of_stay
        CHECK (
            Length_of_Stay IS NULL
            OR Length_of_Stay >= 0
        ),


    CONSTRAINT chk_pam_expected_discharge
        CHECK (
            Expected_Discharge_Date IS NULL
            OR Expected_Discharge_Date >= DATE(Admission_Date)
        ),


    CONSTRAINT chk_pam_actual_discharge
        CHECK (
            Actual_Discharge_Date IS NULL
            OR Actual_Discharge_Date >= DATE(Admission_Date)
        ),


    -- ======================================================
    -- Foreign Key Constraints
    -- ======================================================

    CONSTRAINT fk_pam_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,


    CONSTRAINT fk_pam_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,


    CONSTRAINT fk_pam_department
        FOREIGN KEY (Department_ID)
        REFERENCES Departments(Department_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,


    CONSTRAINT fk_pam_doctor
        FOREIGN KEY (Admitting_Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,


    CONSTRAINT fk_pam_predicted_disease
        FOREIGN KEY (Predicted_Disease_ID)
        REFERENCES Diseases(Disease_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Duplicate Record Prevention
    -- Each admission can appear only once.
    -- ======================================================

    CONSTRAINT uk_pam_admission
        UNIQUE (
            Admission_ID
        )

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_pam_patient
    ON Patient_Admissions_Map(Patient_ID);

CREATE INDEX idx_pam_admission
    ON Patient_Admissions_Map(Admission_ID);

CREATE INDEX idx_pam_admission_number
    ON Patient_Admissions_Map(Admission_Number);

CREATE INDEX idx_pam_department
    ON Patient_Admissions_Map(Department_ID);

CREATE INDEX idx_pam_doctor
    ON Patient_Admissions_Map(Admitting_Doctor_ID);

CREATE INDEX idx_pam_room
    ON Patient_Admissions_Map(Room_ID);

CREATE INDEX idx_pam_bed
    ON Patient_Admissions_Map(Bed_ID);

CREATE INDEX idx_pam_admission_date
    ON Patient_Admissions_Map(Admission_Date);

CREATE INDEX idx_pam_expected_discharge
    ON Patient_Admissions_Map(Expected_Discharge_Date);

CREATE INDEX idx_pam_actual_discharge
    ON Patient_Admissions_Map(Actual_Discharge_Date);

CREATE INDEX idx_pam_status
    ON Patient_Admissions_Map(Current_Status);

CREATE INDEX idx_pam_type
    ON Patient_Admissions_Map(Admission_Type);

CREATE INDEX idx_pam_icu
    ON Patient_Admissions_Map(Is_ICU_Admission);

CREATE INDEX idx_pam_emergency
    ON Patient_Admissions_Map(Is_Emergency);

CREATE INDEX idx_pam_ai_risk
    ON Patient_Admissions_Map(AI_Risk_Level);

CREATE INDEX idx_pam_predicted_disease
    ON Patient_Admissions_Map(Predicted_Disease_ID);

CREATE INDEX idx_pam_data_source
    ON Patient_Admissions_Map(Data_Source);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Patient_Admissions_Map;