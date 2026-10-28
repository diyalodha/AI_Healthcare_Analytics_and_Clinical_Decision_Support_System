/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 51_Create_Referrals_Table.sql

Purpose : Create Patient Referral Management Table

Description:
Stores patient referral information between doctors,
departments and external healthcare facilities for
clinical coordination, tracking and AI analytics.

Version : 2.2

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

-- ==========================================================
-- Remove Existing Table
-- ==========================================================

DROP TABLE IF EXISTS Referrals;

-- ==========================================================
-- Create Table
-- ==========================================================

CREATE TABLE Referrals (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Referral_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),

    Referral_Number VARCHAR(50)
        NOT NULL UNIQUE,

    -- ======================================================
    -- Patient Information
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Appointment_ID CHAR(36),

    -- ======================================================
    -- Doctor Information
    -- ======================================================

    Referring_Doctor_ID CHAR(36),

    Receiving_Doctor_ID CHAR(36),

    -- ======================================================
    -- Department Information
    -- ======================================================

    From_Department_ID CHAR(36),

    To_Department_ID CHAR(36),

    -- ======================================================
    -- External Referral Information
    -- ======================================================

    External_Hospital_Name VARCHAR(200),

    External_Doctor_Name VARCHAR(150),

    External_Contact_Number VARCHAR(20),

    -- ======================================================
    -- Referral Details
    -- ======================================================

    Referral_Date DATE
        NOT NULL,

    Expected_Visit_Date DATE,

    Referral_Type ENUM(
        'Internal',
        'External',
        'Emergency'
    ) DEFAULT 'Internal',

    Referral_Mode ENUM(
        'Walk-In',
        'Email',
        'Phone',
        'Portal',
        'Other'
    ) DEFAULT 'Portal',

    Referral_Reason TEXT,

    Diagnosis_At_Referral TEXT,

    Priority_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    ) DEFAULT 'Medium',

    Urgency_Justification TEXT,

    -- ======================================================
    -- Referral Status
    -- ======================================================

    Referral_Status ENUM(
        'Pending',
        'Accepted',
        'Rejected',
        'Completed',
        'Cancelled'
    ) DEFAULT 'Pending',

    Referral_Outcome TEXT,

    Referral_Completed_Date DATE,

    Follow_Up_Date DATE,

    Doctor_Notes TEXT,

    -- ======================================================
    -- AI Analytics
    -- ======================================================

    AI_Referral_Risk_Score DECIMAL(5,2),

    AI_Recommendation TEXT,

    Processing_Time_Hours DECIMAL(6,2),

    -- ======================================================
    -- Dataset Tracking
    -- ======================================================

    Data_Source ENUM(
        'Hospital_Records',
        'Synthetic',
        'Hybrid Dataset'
    ) DEFAULT 'Hospital_Records',

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
    -- Constraints
    -- ======================================================

    CONSTRAINT CHK_Referral_Risk
        CHECK (
            AI_Referral_Risk_Score IS NULL
            OR (
                AI_Referral_Risk_Score >= 0
                AND AI_Referral_Risk_Score <= 100
            )
        ),

    CONSTRAINT CHK_Referral_Time
        CHECK (
            Processing_Time_Hours IS NULL
            OR Processing_Time_Hours >= 0
        ),

    -- ======================================================
    -- Foreign Keys
    -- ======================================================

    CONSTRAINT FK_Referral_Patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT FK_Referral_Appointment
        FOREIGN KEY (Appointment_ID)
        REFERENCES Appointments(Appointment_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT FK_Referral_ReferringDoctor
        FOREIGN KEY (Referring_Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT FK_Referral_ReceivingDoctor
        FOREIGN KEY (Receiving_Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT FK_Referral_FromDepartment
        FOREIGN KEY (From_Department_ID)
        REFERENCES Departments(Department_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT FK_Referral_ToDepartment
        FOREIGN KEY (To_Department_ID)
        REFERENCES Departments(Department_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL

);

-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX IDX_Referral_Patient
ON Referrals(Patient_ID);

CREATE INDEX IDX_Referral_Appointment
ON Referrals(Appointment_ID);

CREATE INDEX IDX_Referral_Status
ON Referrals(Referral_Status);

CREATE INDEX IDX_Referral_Date
ON Referrals(Referral_Date);

CREATE INDEX IDX_Referral_Priority
ON Referrals(Priority_Level);

CREATE INDEX IDX_Referral_ReferringDoctor
ON Referrals(Referring_Doctor_ID);

CREATE INDEX IDX_Referral_ReceivingDoctor
ON Referrals(Receiving_Doctor_ID);

CREATE INDEX IDX_Referral_ToDepartment
ON Referrals(To_Department_ID);

-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Referrals;