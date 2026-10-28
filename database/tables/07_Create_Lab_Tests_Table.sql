/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 07_Create_Lab_Tests_Table.sql
Purpose : Create Lab Tests Master Table
Version : 3.0
Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- ===========================================================
-- Create Lab Tests Master Table
-- ===========================================================

CREATE TABLE IF NOT EXISTS Lab_Tests (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Lab_Test_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =======================================================
    -- Test Information
    -- =======================================================

    Test_Code VARCHAR(20)
        NOT NULL
        UNIQUE,

    Test_Name VARCHAR(150)
        NOT NULL
        UNIQUE,

    Test_Category VARCHAR(100),

    Department_Name VARCHAR(100),

    Description TEXT,

    Sample_Type ENUM(
        'Blood',
        'Urine',
        'Saliva',
        'Stool',
        'Tissue',
        'Sputum',
        'CSF',
        'Serum',
        'Plasma',
        'Other'
    ),

    Preparation_Required VARCHAR(255),

    Fasting_Required BOOLEAN
        DEFAULT FALSE,

    Minimum_Age INT,

    Maximum_Age INT,

    Reference_Range VARCHAR(100),

    Normal_Range VARCHAR(100),

    Critical_Low_Value VARCHAR(50),

    Critical_High_Value VARCHAR(50),

    Unit VARCHAR(50),

    Methodology VARCHAR(100),

    Instrument_Name VARCHAR(150),

    Cost DECIMAL(10,2),

    Turnaround_Time_Hours INT,


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

    CONSTRAINT chk_lab_cost
        CHECK (
            Cost IS NULL
            OR Cost >= 0
        ),

    CONSTRAINT chk_turnaround
        CHECK (
            Turnaround_Time_Hours IS NULL
            OR Turnaround_Time_Hours >= 0
        ),

    CONSTRAINT chk_age_range
        CHECK (
            Minimum_Age IS NULL
            OR Maximum_Age IS NULL
            OR Minimum_Age <= Maximum_Age
        )

);


-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_lab_test_code
ON Lab_Tests(Test_Code);

CREATE INDEX idx_lab_test_name
ON Lab_Tests(Test_Name);

CREATE INDEX idx_lab_test_category
ON Lab_Tests(Test_Category);

CREATE INDEX idx_lab_department
ON Lab_Tests(Department_Name);

CREATE INDEX idx_lab_sample_type
ON Lab_Tests(Sample_Type);

CREATE INDEX idx_lab_status
ON Lab_Tests(Status);


-- ===========================================================
-- Verification
-- ===========================================================

SHOW TABLES;

DESCRIBE Lab_Tests;