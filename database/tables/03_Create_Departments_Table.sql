/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 03_Create_Departments_Table.sql
Purpose : Create Departments Master Table
Version : 3.0
Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- ===========================================================
-- Create Departments Table
-- ===========================================================

CREATE TABLE IF NOT EXISTS Departments (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Department_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =======================================================
    -- Department Information
    -- =======================================================

    Department_Name VARCHAR(100)
        NOT NULL
        UNIQUE,

    Department_Code VARCHAR(15)
        NOT NULL
        UNIQUE,

    Description TEXT,

    Department_Type ENUM(
        'Clinical',
        'Diagnostic',
        'Administrative',
        'Support'
    ) NOT NULL,


    -- =======================================================
    -- Contact Information
    -- =======================================================

    Contact_Number VARCHAR(20),

    Email VARCHAR(100)
        UNIQUE,

    Location VARCHAR(100),

    Floor_Number INT,

    Extension_Number VARCHAR(10),


    -- =======================================================
    -- Department Head
    -- =======================================================

    Head_Doctor_ID CHAR(36),


    -- =======================================================
    -- Capacity Information
    -- =======================================================

    Total_Doctors INT
        DEFAULT 0,

    Total_Staff INT
        DEFAULT 0,

    Capacity INT
        DEFAULT 0,


    -- =======================================================
    -- Working Hours
    -- =======================================================

    Opening_Time TIME,

    Closing_Time TIME,

    Is_24x7 BOOLEAN
        DEFAULT FALSE,


    -- =======================================================
    -- Status Information
    -- =======================================================

    Status ENUM(
        'Active',
        'Inactive',
        'Under Maintenance'
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

    CONSTRAINT chk_total_doctors
        CHECK (Total_Doctors >= 0),

    CONSTRAINT chk_total_staff
        CHECK (Total_Staff >= 0),

    CONSTRAINT chk_capacity
        CHECK (Capacity >= 0),

    CONSTRAINT chk_floor
        CHECK (
            Floor_Number IS NULL
            OR Floor_Number >= 0
        )

);


-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_department_name
ON Departments(Department_Name);

CREATE INDEX idx_department_code
ON Departments(Department_Code);

CREATE INDEX idx_department_type
ON Departments(Department_Type);

CREATE INDEX idx_department_status
ON Departments(Status);

CREATE INDEX idx_department_location
ON Departments(Location);

CREATE INDEX idx_department_head
ON Departments(Head_Doctor_ID);


-- ===========================================================
-- Verification
-- ===========================================================

SHOW TABLES;

DESCRIBE Departments;