/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 05_Create_Diseases_Table.sql
Purpose : Create Diseases Master Table
Version : 3.0
Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- ===========================================================
-- Create Diseases Master Table
-- ===========================================================

CREATE TABLE IF NOT EXISTS Diseases (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Disease_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =======================================================
    -- Disease Information
    -- =======================================================

    Disease_Name VARCHAR(150)
        NOT NULL
        UNIQUE,

    ICD10_Code VARCHAR(20)
        UNIQUE,

    SNOMED_Code VARCHAR(30)
        UNIQUE,

    Disease_Category VARCHAR(100),

    Department_Name VARCHAR(100),

    Disease_Type ENUM(
        'Acute',
        'Chronic',
        'Genetic',
        'Infectious',
        'Lifestyle',
        'Autoimmune',
        'Cancer',
        'Mental Health',
        'Other'
    ),

    Description TEXT,

    Symptoms TEXT,

    Causes TEXT,

    Risk_Factors TEXT,

    Prevention TEXT,

    Treatment_Protocol TEXT,

    Recovery_Period_Days INT,

    Severity ENUM(
        'Low',
        'Moderate',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

    Mortality_Risk ENUM(
        'Very Low',
        'Low',
        'Moderate',
        'High',
        'Very High'
    )
    DEFAULT 'Low',

    Requires_Hospitalization BOOLEAN
        DEFAULT FALSE,

    Is_Contagious BOOLEAN
        DEFAULT FALSE,


    -- =======================================================
    -- Status Information
    -- =======================================================

    Status ENUM(
        'Active',
        'Inactive'
    )
    DEFAULT 'Active',

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

    CONSTRAINT chk_recovery_days
        CHECK (
            Recovery_Period_Days IS NULL
            OR Recovery_Period_Days >= 0
        )

);


-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_disease_name
ON Diseases(Disease_Name);

CREATE INDEX idx_disease_icd10
ON Diseases(ICD10_Code);

CREATE INDEX idx_disease_snomed
ON Diseases(SNOMED_Code);

CREATE INDEX idx_disease_category
ON Diseases(Disease_Category);

CREATE INDEX idx_disease_department
ON Diseases(Department_Name);

CREATE INDEX idx_disease_type
ON Diseases(Disease_Type);

CREATE INDEX idx_disease_severity
ON Diseases(Severity);

CREATE INDEX idx_disease_status
ON Diseases(Status);


-- ===========================================================
-- Verification
-- ===========================================================

SHOW TABLES;

DESCRIBE Diseases;