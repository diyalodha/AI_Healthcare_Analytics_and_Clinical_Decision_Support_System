/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 56_Create_Patient_Doctors_Map.sql

Purpose : Create Patient-Doctor Mapping Table

Description:
Stores the assignment and relationship between patients and 
doctors, including primary attending physicians, consulting 
specialists, relationship status, and timeline history.

Version : 2.2
===========================================================
*/

USE healthcare_ai_db;


-- ==========================================================
-- Remove Existing Table
-- Warning: This deletes existing data from this table.
-- ==========================================================

DROP TABLE IF EXISTS Patient_Doctors_Map;


-- ==========================================================
-- Create Patient Doctors Mapping Table
-- ==========================================================

CREATE TABLE Patient_Doctors_Map (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Patient_Doctor_Map_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Key References
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36)
        NOT NULL,

    Department_ID CHAR(36)
        NULL,


    -- ======================================================
    -- Relationship Details
    -- ======================================================

    Doctor_Role ENUM(
        'Primary Care Physician',
        'Attending Physician',
        'Consulting Specialist',
        'Surgeon',
        'Referring Doctor',
        'Emergency Doctor',
        'Other'
    )
        NOT NULL DEFAULT 'Primary Care Physician',

    Is_Primary_Doctor BOOLEAN
        NOT NULL DEFAULT FALSE,

    Assignment_Reason VARCHAR(255)
        NULL,


    -- ======================================================
    -- Timeline Information
    -- ======================================================

    Start_Date DATE
        NOT NULL,

    End_Date DATE
        NULL,

    Relationship_Status ENUM(
        'Active',
        'Completed',
        'Transferred',
        'Discontinued'
    )
        NOT NULL DEFAULT 'Active',


    -- ======================================================
    -- Visit and Clinical Tracking
    -- ======================================================

    Total_Visits_Completed INT
        NOT NULL DEFAULT 0,

    Last_Consultation_Date DATE
        NULL,

    Next_Scheduled_Visit DATE
        NULL,

    Clinical_Notes TEXT
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

    CONSTRAINT chk_pdm_dates
        CHECK (
            End_Date IS NULL
            OR End_Date >= Start_Date
        ),

    CONSTRAINT chk_pdm_visits
        CHECK (
            Total_Visits_Completed >= 0
        ),


    -- ======================================================
    -- Foreign Key Constraints
    -- ======================================================

    CONSTRAINT fk_pdm_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_pdm_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_pdm_department
        FOREIGN KEY (Department_ID)
        REFERENCES Departments(Department_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Duplicate Assignment Protection
    -- ======================================================

    CONSTRAINT uk_pdm_patient_doctor_start
        UNIQUE (
            Patient_ID,
            Doctor_ID,
            Start_Date
        )

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_pdm_patient
    ON Patient_Doctors_Map(Patient_ID);

CREATE INDEX idx_pdm_doctor
    ON Patient_Doctors_Map(Doctor_ID);

CREATE INDEX idx_pdm_department
    ON Patient_Doctors_Map(Department_ID);

CREATE INDEX idx_pdm_status
    ON Patient_Doctors_Map(Relationship_Status);

CREATE INDEX idx_pdm_start_date
    ON Patient_Doctors_Map(Start_Date);

CREATE INDEX idx_pdm_primary
    ON Patient_Doctors_Map(Is_Primary_Doctor);

CREATE INDEX idx_pdm_data_source
    ON Patient_Doctors_Map(Data_Source);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Patient_Doctors_Map;