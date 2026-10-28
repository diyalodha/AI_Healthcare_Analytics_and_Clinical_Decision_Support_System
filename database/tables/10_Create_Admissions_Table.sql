/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 10_Create_Admissions_Table.sql
Purpose : Create Admissions Transaction Table
Version : 3.0
Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- ===========================================================
-- Create Admissions Table
-- ===========================================================

CREATE TABLE IF NOT EXISTS Admissions (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Admission_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =======================================================
    -- Foreign Keys
    -- =======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Department_ID CHAR(36)
        NOT NULL,

    Admitting_Doctor_ID CHAR(36)
        NOT NULL,

    Bed_ID CHAR(36),

    Room_ID CHAR(36),


    -- =======================================================
    -- Admission Information
    -- =======================================================

    Admission_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Admission_Date DATETIME
        NOT NULL,

    Expected_Discharge_Date DATE,

    Actual_Discharge_Date DATE,

    Admission_Type ENUM(
        'Emergency',
        'Routine',
        'Referral',
        'Transfer'
    )
    NOT NULL,

    Admission_Reason TEXT,

    Initial_Diagnosis TEXT,

    Ward VARCHAR(100),

    Room_Number VARCHAR(20),

    Bed_Number VARCHAR(20),

    Current_Status ENUM(
        'Admitted',
        'Under Observation',
        'ICU',
        'Discharged',
        'Transferred',
        'Expired'
    )
    DEFAULT 'Admitted',

    Length_of_Stay INT,

    Is_ICU_Admission BOOLEAN
        DEFAULT FALSE,

    Requires_Surgery BOOLEAN
        DEFAULT FALSE,

    Is_Emergency BOOLEAN
        DEFAULT FALSE,

    Notes TEXT,


    -- =======================================================
    -- AI Decision Support
    -- =======================================================

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

    Predicted_Disease_ID CHAR(36),


    -- =======================================================
    -- Status Information
    -- =======================================================

    Is_Active BOOLEAN
        DEFAULT TRUE,

    Is_Deleted BOOLEAN
        DEFAULT FALSE,

    Record_Version INT
        DEFAULT 1,


    -- =======================================================
    -- Audit Information
    -- =======================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,


    -- =======================================================
    -- Foreign Keys
    -- =======================================================

    CONSTRAINT fk_admissions_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_admissions_department
        FOREIGN KEY (Department_ID)
        REFERENCES Departments(Department_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_admissions_doctor
        FOREIGN KEY (Admitting_Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_admissions_predicted_disease
        FOREIGN KEY (Predicted_Disease_ID)
        REFERENCES Diseases(Disease_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT chk_admissions_length_of_stay
        CHECK (
            Length_of_Stay IS NULL
            OR Length_of_Stay >= 0
        )

);


-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_admissions_number
ON Admissions(Admission_Number);

CREATE INDEX idx_admissions_patient
ON Admissions(Patient_ID);

CREATE INDEX idx_admissions_department
ON Admissions(Department_ID);

CREATE INDEX idx_admissions_doctor
ON Admissions(Admitting_Doctor_ID);

CREATE INDEX idx_admissions_date
ON Admissions(Admission_Date);

CREATE INDEX idx_admissions_status
ON Admissions(Current_Status);

CREATE INDEX idx_admissions_type
ON Admissions(Admission_Type);

CREATE INDEX idx_admissions_ai_risk
ON Admissions(AI_Risk_Level);

CREATE INDEX idx_admissions_predicted_disease
ON Admissions(Predicted_Disease_ID);


-- ===========================================================
-- Verification
-- ===========================================================

SHOW TABLES;

DESCRIBE Admissions;