/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 58_Create_Patient_Vaccination_Map.sql

Purpose : Create Patient Vaccination Mapping Table

Description:
Stores comprehensive vaccination records for patients, including
vaccine types, dose sequences, administration dates, lot numbers,
adverse events, and upcoming scheduled booster doses.

Version : 2.3

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- ==========================================================
-- Remove Existing Table
-- Warning: This deletes existing data from this table.
-- ==========================================================

DROP TABLE IF EXISTS Patient_Vaccination_Map;


-- ==========================================================
-- Create Patient Vaccination Mapping Table
-- ==========================================================

CREATE TABLE Patient_Vaccination_Map (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Vaccination_Map_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Key References
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Administered_By_Doctor_ID CHAR(36)
        NULL,


    -- ======================================================
    -- Vaccine Details
    -- ======================================================

    Vaccine_Name VARCHAR(150)
        NOT NULL,

    Vaccine_Code VARCHAR(50)
        NULL,

    Target_Disease VARCHAR(150)
        NOT NULL,

    Manufacturer VARCHAR(150)
        NULL,

    Batch_Number VARCHAR(50)
        NULL,

    Lot_Number VARCHAR(50)
        NULL,

    Expiration_Date DATE
        NULL,


    -- ======================================================
    -- Administration Protocol
    -- ======================================================

    Dose_Number INT
        NOT NULL DEFAULT 1,

    Total_Doses_Required INT
        NOT NULL DEFAULT 1,

    Administration_Date DATE
        NOT NULL,

    Route_Of_Administration ENUM(
        'Intramuscular',
        'Subcutaneous',
        'Oral',
        'Intradermal',
        'Nasal Spray',
        'Other'
    )
        NOT NULL DEFAULT 'Intramuscular',

    Administration_Site ENUM(
        'Left Deltoid',
        'Right Deltoid',
        'Left Anterolateral Thigh',
        'Right Anterolateral Thigh',
        'Oral',
        'Other'
    )
        NOT NULL DEFAULT 'Left Deltoid',

    Dosage_Administered VARCHAR(50)
        NULL,


    -- ======================================================
    -- Schedule and Status
    -- ======================================================

    Vaccination_Status ENUM(
        'Completed',
        'Partially Vaccinated',
        'Overdue',
        'Exempted',
        'Refused'
    )
        NOT NULL DEFAULT 'Completed',

    Next_Due_Date DATE
        NULL,

    Exemption_Reason TEXT
        NULL,


    -- ======================================================
    -- Safety and Adverse Reactions
    -- ======================================================

    Adverse_Reaction_Observed BOOLEAN
        NOT NULL DEFAULT FALSE,

    Adverse_Reaction_Severity ENUM(
        'None',
        'Mild',
        'Moderate',
        'Severe',
        'Anaphylaxis'
    )
        NOT NULL DEFAULT 'None',

    Adverse_Reaction_Description TEXT
        NULL,


    -- ======================================================
    -- Record Status
    -- ======================================================

    Is_Active BOOLEAN
        NOT NULL DEFAULT TRUE,

    Is_Deleted BOOLEAN
        NOT NULL DEFAULT FALSE,

    Record_Version INT
        NOT NULL DEFAULT 1,


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

    CONSTRAINT chk_pvm_dose_number
        CHECK (
            Dose_Number >= 1
        ),


    CONSTRAINT chk_pvm_doses_required
        CHECK (
            Total_Doses_Required >= 1
            AND Total_Doses_Required >= Dose_Number
        ),


    CONSTRAINT chk_pvm_next_date
        CHECK (
            Next_Due_Date IS NULL
            OR Next_Due_Date >= Administration_Date
        ),


    CONSTRAINT chk_pvm_expiration_date
        CHECK (
            Expiration_Date IS NULL
            OR Expiration_Date >= Administration_Date
        ),


    CONSTRAINT chk_pvm_record_version
        CHECK (
            Record_Version >= 1
        ),


    CONSTRAINT chk_pvm_adverse_reaction
        CHECK (
            (
                Adverse_Reaction_Observed = FALSE
                AND Adverse_Reaction_Severity = 'None'
            )
            OR
            (
                Adverse_Reaction_Observed = TRUE
                AND Adverse_Reaction_Severity <> 'None'
            )
        ),


    -- ======================================================
    -- Foreign Key Constraints
    -- ======================================================

    CONSTRAINT fk_pvm_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,


    CONSTRAINT fk_pvm_doctor
        FOREIGN KEY (Administered_By_Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Duplicate Record Prevention
    -- ======================================================

    CONSTRAINT uk_pvm_patient_vaccine_dose
        UNIQUE (
            Patient_ID,
            Vaccine_Name,
            Dose_Number,
            Administration_Date
        )

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_pvm_patient
    ON Patient_Vaccination_Map(Patient_ID);


CREATE INDEX idx_pvm_doctor
    ON Patient_Vaccination_Map(Administered_By_Doctor_ID);


CREATE INDEX idx_pvm_vaccine_name
    ON Patient_Vaccination_Map(Vaccine_Name);


CREATE INDEX idx_pvm_vaccine_code
    ON Patient_Vaccination_Map(Vaccine_Code);


CREATE INDEX idx_pvm_target_disease
    ON Patient_Vaccination_Map(Target_Disease);


CREATE INDEX idx_pvm_admin_date
    ON Patient_Vaccination_Map(Administration_Date);


CREATE INDEX idx_pvm_status
    ON Patient_Vaccination_Map(Vaccination_Status);


CREATE INDEX idx_pvm_next_due
    ON Patient_Vaccination_Map(Next_Due_Date);


CREATE INDEX idx_pvm_adverse_reaction
    ON Patient_Vaccination_Map(Adverse_Reaction_Observed);


CREATE INDEX idx_pvm_is_active
    ON Patient_Vaccination_Map(Is_Active);


CREATE INDEX idx_pvm_is_deleted
    ON Patient_Vaccination_Map(Is_Deleted);


CREATE INDEX idx_pvm_data_source
    ON Patient_Vaccination_Map(Data_Source);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Patient_Vaccination_Map;