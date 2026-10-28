/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 37_Create_Emergency_Contacts_Table.sql

Purpose : Create Patient Emergency Contacts Table

Description:
Stores emergency contact information of patients for
critical care communication, hospital operations,
and AI-enabled emergency response management.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

-- ==========================================================
-- Create Emergency Contacts Table
-- ==========================================================

CREATE TABLE IF NOT EXISTS Emergency_Contacts (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Emergency_Contact_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Key
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,


    -- ======================================================
    -- Contact Information
    -- ======================================================

    Contact_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Contact_Name VARCHAR(150)
        NOT NULL,

    Relationship VARCHAR(100)
        NOT NULL,

    Primary_Phone VARCHAR(20)
        NOT NULL,

    Alternate_Phone VARCHAR(20),

    Email VARCHAR(150),

    Address VARCHAR(255),

    City VARCHAR(100),

    State VARCHAR(100),

    Country VARCHAR(100)
        DEFAULT 'India',

    Postal_Code VARCHAR(20),


    -- ======================================================
    -- Emergency Contact Information
    -- ======================================================

    Is_Primary_Contact BOOLEAN
        DEFAULT TRUE,

    Contact_Priority ENUM(
        'Primary',
        'Secondary',
        'Emergency Only'
    )
    DEFAULT 'Primary',

    Available_24x7 BOOLEAN
        DEFAULT FALSE,

    Preferred_Communication ENUM(
        'Phone',
        'SMS',
        'Email',
        'WhatsApp'
    )
    DEFAULT 'Phone',

    Emergency_Contact_Status ENUM(
        'Active',
        'Inactive'
    )
    DEFAULT 'Active',

    Verification_Status ENUM(
        'Pending',
        'Verified',
        'Rejected'
    )
    DEFAULT 'Pending',


    -- ======================================================
    -- AI & Healthcare Support
    -- ======================================================

    AI_Notification_Enabled BOOLEAN
        DEFAULT TRUE,

    Notes TEXT,


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
    -- Foreign Key Constraint
    -- ======================================================

    CONSTRAINT fk_emergency_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    -- ======================================================
    -- Check Constraints
    -- ======================================================

    CONSTRAINT chk_primary_phone
        CHECK (
            CHAR_LENGTH(Primary_Phone) >= 10
        )

);

-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_emergency_contact_number
ON Emergency_Contacts(Contact_Number);

CREATE INDEX idx_emergency_patient
ON Emergency_Contacts(Patient_ID);

CREATE INDEX idx_emergency_primary
ON Emergency_Contacts(Is_Primary_Contact);

CREATE INDEX idx_emergency_priority
ON Emergency_Contacts(Contact_Priority);

CREATE INDEX idx_emergency_phone
ON Emergency_Contacts(Primary_Phone);

CREATE INDEX idx_emergency_status
ON Emergency_Contacts(Emergency_Contact_Status);

CREATE INDEX idx_emergency_verification
ON Emergency_Contacts(Verification_Status);

CREATE INDEX idx_emergency_active
ON Emergency_Contacts(Is_Active);

-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Emergency_Contacts;