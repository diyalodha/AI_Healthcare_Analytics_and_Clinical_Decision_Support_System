/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 09_Create_Appointments_Table.sql
Purpose : Create Appointments Transaction Table
Version : 3.1
Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- ===========================================================
-- Create Appointments Table
-- ===========================================================

CREATE TABLE IF NOT EXISTS Appointments (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Appointment_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =======================================================
    -- Foreign Keys
    -- =======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36)
        NOT NULL,

    Department_ID CHAR(36)
        NOT NULL,

    Predicted_Disease_ID CHAR(36),


    -- =======================================================
    -- Appointment Information
    -- =======================================================

    Appointment_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Appointment_Date DATE
        NOT NULL,

    Appointment_Time TIME
        NOT NULL,

    Estimated_Duration_Minutes INT
        DEFAULT 30,

    Token_Number INT,

    Appointment_Type ENUM(
        'Consultation',
        'Follow-up',
        'Emergency',
        'Telemedicine'
    )
    DEFAULT 'Consultation',

    Consultation_Mode ENUM(
        'Offline',
        'Online'
    )
    DEFAULT 'Offline',

    Reason TEXT,

    Symptoms TEXT,

    Priority ENUM(
        'Low',
        'Medium',
        'High',
        'Emergency'
    )
    DEFAULT 'Medium',

    Status ENUM(
        'Scheduled',
        'Checked-In',
        'In Progress',
        'Completed',
        'Cancelled',
        'No Show'
    )
    DEFAULT 'Scheduled',

    Queue_Position INT,

    Appointment_Notes TEXT,


    -- =======================================================
    -- Financial Information
    -- =======================================================

    Consultation_Fee DECIMAL(10,2),

    Payment_Status ENUM(
        'Pending',
        'Paid',
        'Refunded'
    )
    DEFAULT 'Pending',


    -- =======================================================
    -- AI & Clinical Decision Support
    -- =======================================================

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

    Requires_Followup BOOLEAN
        DEFAULT FALSE,


    -- =======================================================
    -- Record Status
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
    -- Foreign Key Constraints
    -- =======================================================

    CONSTRAINT fk_appointments_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_appointments_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_appointments_department
        FOREIGN KEY (Department_ID)
        REFERENCES Departments(Department_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_appointments_predicted_disease
        FOREIGN KEY (Predicted_Disease_ID)
        REFERENCES Diseases(Disease_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- =======================================================
    -- Check Constraints
    -- =======================================================

    CONSTRAINT chk_appointment_duration
        CHECK (
            Estimated_Duration_Minutes > 0
        ),

    CONSTRAINT chk_appointment_fee
        CHECK (
            Consultation_Fee IS NULL
            OR Consultation_Fee >= 0
        )

);


-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_appointments_number
ON Appointments(Appointment_Number);

CREATE INDEX idx_appointments_date
ON Appointments(Appointment_Date);

CREATE INDEX idx_appointments_time
ON Appointments(Appointment_Time);

CREATE INDEX idx_appointments_patient
ON Appointments(Patient_ID);

CREATE INDEX idx_appointments_doctor
ON Appointments(Doctor_ID);

CREATE INDEX idx_appointments_department
ON Appointments(Department_ID);

CREATE INDEX idx_appointments_status
ON Appointments(Status);

CREATE INDEX idx_appointments_priority
ON Appointments(Priority);

CREATE INDEX idx_appointments_payment_status
ON Appointments(Payment_Status);

CREATE INDEX idx_appointments_ai_risk
ON Appointments(AI_Risk_Level);

CREATE INDEX idx_appointments_predicted_disease
ON Appointments(Predicted_Disease_ID);


-- ===========================================================
-- Verification
-- ===========================================================

SHOW TABLES;

DESCRIBE Appointments;