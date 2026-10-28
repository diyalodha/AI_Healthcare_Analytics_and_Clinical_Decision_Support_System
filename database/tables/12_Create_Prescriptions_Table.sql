/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 12_Create_Prescriptions_Table.sql
Purpose : Create Prescriptions Transaction Table
Version : 3.0
Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Prescriptions;

-- ===========================================================
-- Create Prescriptions Table
-- ===========================================================

CREATE TABLE Prescriptions (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Prescription_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =======================================================
    -- Foreign Keys
    -- =======================================================

    Diagnosis_ID CHAR(36)
        NOT NULL,

    Patient_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36)
        NOT NULL,

    Appointment_ID CHAR(36),

    Admission_ID CHAR(36),


    -- =======================================================
    -- Prescription Information
    -- =======================================================

    Prescription_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Prescription_Date DATETIME
        NOT NULL,

    Prescription_Type ENUM(
        'OPD',
        'IPD',
        'Emergency',
        'Discharge'
    )
    DEFAULT 'OPD',

    Advice TEXT,

    Lifestyle_Advice TEXT,

    Diet_Advice TEXT,

    Follow_Up_Date DATE,

    Prescription_Notes TEXT,

    Digital_Signature VARCHAR(255),

    Prescription_Status ENUM(
        'Active',
        'Completed',
        'Cancelled'
    )
    DEFAULT 'Active',


    -- =======================================================
    -- AI Support
    -- =======================================================

    AI_Generated BOOLEAN
        DEFAULT FALSE,

    AI_Recommendation_Score DECIMAL(5,2),

    Requires_Followup BOOLEAN
        DEFAULT FALSE,


    -- =======================================================
    -- System Information
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

    CONSTRAINT fk_prescription_diagnosis
        FOREIGN KEY (Diagnosis_ID)
        REFERENCES Diagnoses(Diagnosis_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_prescription_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_prescription_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_prescription_appointment
        FOREIGN KEY (Appointment_ID)
        REFERENCES Appointments(Appointment_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_prescription_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT chk_followup_date_prescription
        CHECK (
            Follow_Up_Date IS NULL
            OR Follow_Up_Date >= DATE(Prescription_Date)
        )

);

-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_prescription_number
ON Prescriptions(Prescription_Number);

CREATE INDEX idx_prescription_patient
ON Prescriptions(Patient_ID);

CREATE INDEX idx_prescription_doctor
ON Prescriptions(Doctor_ID);

CREATE INDEX idx_prescription_diagnosis
ON Prescriptions(Diagnosis_ID);

CREATE INDEX idx_prescription_appointment
ON Prescriptions(Appointment_ID);

CREATE INDEX idx_prescription_admission
ON Prescriptions(Admission_ID);

CREATE INDEX idx_prescription_date
ON Prescriptions(Prescription_Date);

CREATE INDEX idx_prescription_status
ON Prescriptions(Prescription_Status);

CREATE INDEX idx_prescription_type
ON Prescriptions(Prescription_Type);

-- ===========================================================
-- Verification
-- ===========================================================

SHOW TABLES;

DESCRIBE Prescriptions;