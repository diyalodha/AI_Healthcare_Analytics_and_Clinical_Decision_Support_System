/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 06_Create_Medications_Table.sql
Purpose : Create Medications Master Table
Version : 3.0
Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- ===========================================================
-- Create Medications Master Table
-- ===========================================================

CREATE TABLE IF NOT EXISTS Medications (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Medication_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =======================================================
    -- Medication Information
    -- =======================================================

    Medication_Code VARCHAR(20)
        NOT NULL
        UNIQUE,

    Medication_Name VARCHAR(150)
        NOT NULL,

    Generic_Name VARCHAR(150),

    Brand_Name VARCHAR(150),

    Manufacturer VARCHAR(150),

    Drug_Class VARCHAR(100),

    Used_For VARCHAR(255),

    Dosage_Form ENUM(
        'Tablet',
        'Capsule',
        'Injection',
        'Syrup',
        'Cream',
        'Drops',
        'Inhaler',
        'Ointment',
        'Powder',
        'Solution',
        'Other'
    ),

    Strength VARCHAR(50),

    Route ENUM(
        'Oral',
        'IV',
        'IM',
        'Subcutaneous',
        'Topical',
        'Inhalation',
        'Rectal',
        'Ophthalmic',
        'Nasal',
        'Other'
    ),

    Description TEXT,

    Side_Effects TEXT,

    Contraindications TEXT,

    Storage_Conditions VARCHAR(255),

    Pregnancy_Category ENUM(
        'A',
        'B',
        'C',
        'D',
        'X',
        'Not Applicable'
    )
    DEFAULT 'Not Applicable',

    Prescription_Required BOOLEAN
        DEFAULT TRUE,

    Maximum_Daily_Dose VARCHAR(100),

    Risk_Level ENUM(
        'Low',
        'Medium',
        'High'
    )
    DEFAULT 'Low',


    -- =======================================================
    -- Status Information
    -- =======================================================

    Status ENUM(
        'Available',
        'Out of Stock',
        'Discontinued'
    )
    DEFAULT 'Available',

    Is_Active BOOLEAN
        DEFAULT TRUE,

    Is_Deleted BOOLEAN
        DEFAULT FALSE,


    -- =======================================================
    -- System Information
    -- =======================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Record_Version INT
        DEFAULT 1,


    -- =======================================================
    -- Audit Information
    -- =======================================================

    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,


    -- =======================================================
    -- Validation
    -- =======================================================

    CONSTRAINT chk_medication_name
        CHECK (
            LENGTH(Medication_Name) > 1
        )

);


-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_medication_code
ON Medications(Medication_Code);

CREATE INDEX idx_medication_name
ON Medications(Medication_Name);

CREATE INDEX idx_generic_name
ON Medications(Generic_Name);

CREATE INDEX idx_brand_name
ON Medications(Brand_Name);

CREATE INDEX idx_drug_class
ON Medications(Drug_Class);

CREATE INDEX idx_used_for
ON Medications(Used_For);

CREATE INDEX idx_route
ON Medications(Route);

CREATE INDEX idx_risk_level
ON Medications(Risk_Level);

CREATE INDEX idx_medication_status
ON Medications(Status);


-- ===========================================================
-- Verification
-- ===========================================================

SHOW TABLES;

DESCRIBE Medications;