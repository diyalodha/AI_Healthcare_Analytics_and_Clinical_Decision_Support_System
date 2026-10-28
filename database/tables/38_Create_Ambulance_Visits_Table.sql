/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 38_Create_Ambulance_Visits_Table.sql

Purpose : Create Ambulance Emergency Visit Table

Description:
Stores emergency transportation details including
pre-hospital care, severity level, response time,
AI-supported emergency analytics, and patient transfer
information.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

-- ==========================================================
-- Create Ambulance Visits Table
-- ==========================================================

CREATE TABLE IF NOT EXISTS Ambulance_Visits (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Ambulance_Visit_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Keys
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Admission_ID CHAR(36),


    -- ======================================================
    -- Ambulance Information
    -- ======================================================

    Ambulance_Visit_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Ambulance_Number VARCHAR(50),

    Ambulance_Type ENUM(
        'Basic Life Support',
        'Advanced Life Support',
        'Patient Transport',
        'Emergency'
    )
    DEFAULT 'Emergency',

    Driver_Name VARCHAR(150),

    EMT_Name VARCHAR(150),


    -- ======================================================
    -- Emergency Details
    -- ======================================================

    Pickup_Address VARCHAR(255),

    Destination_Hospital VARCHAR(200),

    Pickup_Time DATETIME,

    Arrival_Time DATETIME,

    Response_Time_Minutes INT,

    Distance_KM DECIMAL(6,2),

    Emergency_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    NOT NULL,

    Chief_Complaint TEXT,

    Pre_Hospital_Treatment TEXT,

    Vital_Status_Before_Arrival TEXT,

    Outcome TEXT,


    -- ======================================================
    -- Visit Status
    -- ======================================================

    Status ENUM(
        'Requested',
        'Dispatched',
        'In Transit',
        'Completed',
        'Cancelled'
    )
    DEFAULT 'Requested',


    -- ======================================================
    -- AI Emergency Analytics
    -- ======================================================

    AI_Triage_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

    AI_Response_Priority INT,

    AI_Recommendation TEXT,

    AI_Processed BOOLEAN
        DEFAULT FALSE,


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
    -- Foreign Key Constraints
    -- ======================================================

    CONSTRAINT fk_ambulance_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_ambulance_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Check Constraints
    -- ======================================================

    CONSTRAINT chk_response_time
        CHECK (
            Response_Time_Minutes IS NULL
            OR Response_Time_Minutes >= 0
        ),

    CONSTRAINT chk_distance
        CHECK (
            Distance_KM IS NULL
            OR Distance_KM >= 0
        ),

    CONSTRAINT chk_arrival_time
        CHECK (
            Pickup_Time IS NULL
            OR Arrival_Time IS NULL
            OR Arrival_Time >= Pickup_Time
        )

);

-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_ambulance_visit_number
ON Ambulance_Visits(Ambulance_Visit_Number);

CREATE INDEX idx_ambulance_patient
ON Ambulance_Visits(Patient_ID);

CREATE INDEX idx_ambulance_admission
ON Ambulance_Visits(Admission_ID);

CREATE INDEX idx_ambulance_pickup
ON Ambulance_Visits(Pickup_Time);

CREATE INDEX idx_ambulance_level
ON Ambulance_Visits(Emergency_Level);

CREATE INDEX idx_ambulance_status
ON Ambulance_Visits(Status);

CREATE INDEX idx_ambulance_ai_triage
ON Ambulance_Visits(AI_Triage_Level);

CREATE INDEX idx_ambulance_active
ON Ambulance_Visits(Is_Active);

-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Ambulance_Visits;