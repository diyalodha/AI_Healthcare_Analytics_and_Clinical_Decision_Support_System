/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 57_Create_Patient_Room_Bed_History.sql

Purpose : Create Patient Room and Bed Movement History Table

Description:
Tracks the movement, allocation, transfers, and stay duration 
of admitted patients across general wards, specialized units, 
and ICU beds.

Version : 2.2
===========================================================
*/

USE healthcare_ai_db;


-- ==========================================================
-- Remove Existing Table
-- Warning: This deletes existing data from this table.
-- ==========================================================

DROP TABLE IF EXISTS Patient_Room_Bed_History;


-- ==========================================================
-- Create Patient Room/Bed History Table
-- ==========================================================

CREATE TABLE Patient_Room_Bed_History (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Allocation_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Key References
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Admission_ID CHAR(36)
        NULL,

    Department_ID CHAR(36)
        NULL,


    -- ======================================================
    -- Location and Unit Classification
    -- ======================================================

    Care_Unit_Type ENUM(
        'General Ward',
        'Semi-Private',
        'Private Room',
        'Deluxe Room',
        'ICU',
        'NICU',
        'PICU',
        'CCU',
        'Emergency Bay',
        'Post-Op Recovery',
        'Isolation Ward',
        'Other'
    )
        NOT NULL DEFAULT 'General Ward',

    Ward_Name VARCHAR(100)
        NOT NULL,

    Room_Number VARCHAR(50)
        NOT NULL,

    Bed_Number VARCHAR(50)
        NOT NULL,

    Floor_Number VARCHAR(20)
        NULL,


    -- ======================================================
    -- Movement and Timeline
    -- ======================================================

    Allocated_From DATETIME
        NOT NULL,

    Allocated_To DATETIME
        NULL,

    Length_Of_Stay_Hours DECIMAL(8,2)
        NULL,

    Allocation_Status ENUM(
        'Active',
        'Transferred',
        'Discharged',
        'Cancelled'
    )
        NOT NULL DEFAULT 'Active',

    Transfer_Reason ENUM(
        'Initial Admission',
        'Condition Deterioration (ICU Transfer)',
        'Condition Improvement (Step Down)',
        'Routine Shift',
        'Patient Request',
        'Infection Control / Isolation',
        'Maintenance',
        'Discharge',
        'Other'
    )
        NOT NULL DEFAULT 'Initial Admission',


    -- ======================================================
    -- Financial Tracking
    -- ======================================================

    Daily_Bed_Charge DECIMAL(10,2)
        NOT NULL DEFAULT 0.00,

    Total_Bed_Cost DECIMAL(12,2)
        NULL,


    -- ======================================================
    -- Clinical Observations & Notes
    -- ======================================================

    Attending_Nurse_Notes TEXT
        NULL,

    Clinical_Remarks TEXT
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

    CONSTRAINT chk_prbh_dates
        CHECK (
            Allocated_To IS NULL
            OR Allocated_To >= Allocated_From
        ),

    CONSTRAINT chk_prbh_stay_hours
        CHECK (
            Length_Of_Stay_Hours IS NULL
            OR Length_Of_Stay_Hours >= 0
        ),

    CONSTRAINT chk_prbh_daily_charge
        CHECK (
            Daily_Bed_Charge >= 0
        ),

    CONSTRAINT chk_prbh_total_cost
        CHECK (
            Total_Bed_Cost IS NULL
            OR Total_Bed_Cost >= 0
        ),


    -- ======================================================
    -- Foreign Key Constraints
    -- ======================================================

    CONSTRAINT fk_prbh_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_prbh_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_prbh_department
        FOREIGN KEY (Department_ID)
        REFERENCES Departments(Department_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_prbh_patient
    ON Patient_Room_Bed_History(Patient_ID);

CREATE INDEX idx_prbh_admission
    ON Patient_Room_Bed_History(Admission_ID);

CREATE INDEX idx_prbh_department
    ON Patient_Room_Bed_History(Department_ID);

CREATE INDEX idx_prbh_unit_type
    ON Patient_Room_Bed_History(Care_Unit_Type);

CREATE INDEX idx_prbh_allocated_from
    ON Patient_Room_Bed_History(Allocated_From);

CREATE INDEX idx_prbh_allocated_to
    ON Patient_Room_Bed_History(Allocated_To);

CREATE INDEX idx_prbh_status
    ON Patient_Room_Bed_History(Allocation_Status);

CREATE INDEX idx_prbh_bed_lookup
    ON Patient_Room_Bed_History(Ward_Name, Room_Number, Bed_Number);

CREATE INDEX idx_prbh_data_source
    ON Patient_Room_Bed_History(Data_Source);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Patient_Room_Bed_History;