/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 44_Create_Medical_Devices_Table.sql

Purpose : Create Medical Devices Table

Description:
Stores hospital medical equipment information including
device lifecycle, maintenance history, AI compatibility,
department allocation, and operational status.

Version : 2.2

Author  : Diya Lodha & Team
===========================================================
*/


USE healthcare_ai_db;



-- ==========================================================
-- Remove Existing Table
-- ==========================================================

DROP TABLE IF EXISTS Medical_Devices;



-- ==========================================================
-- Table : Medical_Devices
-- ==========================================================

CREATE TABLE Medical_Devices (


    -- ======================================================
    -- Primary Key
    -- ======================================================

    Device_ID CHAR(36)
        NOT NULL PRIMARY KEY DEFAULT (UUID()),



    -- ======================================================
    -- Device Information
    -- ======================================================

    Device_Name VARCHAR(150)
        NOT NULL,


    Device_Category ENUM(

        'Monitoring',
        'Diagnostic',
        'Therapeutic',
        'Surgical',
        'Imaging',
        'Laboratory',
        'ICU'

    )
    NOT NULL,


    Device_Type VARCHAR(100),


    Manufacturer VARCHAR(150),


    Model_Number VARCHAR(100),


    Serial_Number VARCHAR(100)
        UNIQUE,


    Vendor_Name VARCHAR(150),


    Vendor_Contact VARCHAR(100),



    -- ======================================================
    -- Purchase & Maintenance
    -- ======================================================

    Purchase_Date DATE,


    Installation_Date DATE,


    Warranty_Expiry DATE,


    Last_Maintenance_Date DATE,


    Calibration_Date DATE,


    Next_Calibration_Date DATE,


    Maintenance_Frequency ENUM(

        'Monthly',
        'Quarterly',
        'Half-Yearly',
        'Yearly'

    )
    DEFAULT 'Yearly',



    -- ======================================================
    -- Department Allocation
    -- ======================================================

    Department_ID CHAR(36),


    Location VARCHAR(150),



    -- ======================================================
    -- Device Status
    -- ======================================================

    Device_Status ENUM(

        'Active',
        'Inactive',
        'Under Maintenance',
        'Retired'

    )
    DEFAULT 'Active',


    AI_Compatible BOOLEAN
        DEFAULT FALSE,


    Notes TEXT,



    -- ======================================================
    -- Dataset Tracking
    -- ======================================================

    Data_Source ENUM(

        'Hospital_Records',
        'Vendor',
        'Synthetic'

    )
    DEFAULT 'Hospital_Records',



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
    -- Foreign Key
    -- ======================================================

    CONSTRAINT FK_Device_Department

    FOREIGN KEY (Department_ID)

    REFERENCES Departments(Department_ID)

    ON UPDATE CASCADE

    ON DELETE SET NULL

);



-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX IDX_Device_Name
ON Medical_Devices(Device_Name);



CREATE INDEX IDX_Device_Category
ON Medical_Devices(Device_Category);



CREATE INDEX IDX_Device_Status
ON Medical_Devices(Device_Status);



CREATE INDEX IDX_Device_Department
ON Medical_Devices(Department_ID);



CREATE INDEX IDX_Device_Location
ON Medical_Devices(Location);



CREATE INDEX IDX_Device_AI
ON Medical_Devices(AI_Compatible);



SHOW TABLES;

DESCRIBE Medical_Devices;