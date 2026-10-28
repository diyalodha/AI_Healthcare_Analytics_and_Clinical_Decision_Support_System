/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 49_Create_Blood_Bank_Table.sql

Purpose : Create Blood Bank Management Table

Description:
Stores blood inventory, donation details, donor
information, screening results, blood requests,
transfusion details and AI analytics information.

Version : 2.2

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

-- ==========================================================
-- Remove Existing Table
-- ==========================================================

DROP TABLE IF EXISTS Blood_Bank;

-- ==========================================================
-- Create Table
-- ==========================================================

CREATE TABLE Blood_Bank (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Blood_Record_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),

    -- ======================================================
    -- Blood Unit Information
    -- ======================================================

    Blood_Unit_Number VARCHAR(100)
        NOT NULL UNIQUE,

    Blood_Group ENUM(
        'A+',
        'A-',
        'B+',
        'B-',
        'AB+',
        'AB-',
        'O+',
        'O-'
    ) NOT NULL,

    Component_Type ENUM(
        'Whole Blood',
        'Red Blood Cells',
        'Platelets',
        'Plasma',
        'Cryoprecipitate'
    ) NOT NULL,

    Donation_Date DATE NOT NULL,

    Expiry_Date DATE NOT NULL,

    Quantity_ml INT NOT NULL,

    Available_Quantity_ml INT DEFAULT 0,

    Storage_Location VARCHAR(150),

    Storage_Temperature VARCHAR(50),

    -- ======================================================
    -- Donor Information
    -- ======================================================

    Donor_Name VARCHAR(150),

    Donor_Age INT,

    Donor_Gender ENUM(
        'Male',
        'Female',
        'Other'
    ),

    Donor_Contact VARCHAR(20),

    Donor_Type ENUM(
        'Voluntary',
        'Replacement',
        'Emergency'
    ) DEFAULT 'Voluntary',

    -- ======================================================
    -- Screening Information
    -- ======================================================

    HIV_Test_Status ENUM(
        'Negative',
        'Positive',
        'Pending'
    ) DEFAULT 'Pending',

    Hepatitis_Test_Status ENUM(
        'Negative',
        'Positive',
        'Pending'
    ) DEFAULT 'Pending',

    Other_Screening_Status TEXT,

    Cross_Match_Status ENUM(
        'Pending',
        'Compatible',
        'Incompatible'
    ) DEFAULT 'Pending',

    Compatibility_Status ENUM(
        'Compatible',
        'Not Compatible',
        'Unknown'
    ) DEFAULT 'Unknown',

    -- ======================================================
    -- Blood Request Information
    -- ======================================================

    Patient_ID CHAR(36),

    Requested_By_Doctor_ID CHAR(36),

    Department_ID CHAR(36),

    Request_Date DATETIME,

    Usage_Status ENUM(
        'Available',
        'Reserved',
        'Issued',
        'Expired',
        'Discarded'
    ) DEFAULT 'Available',

    Transfusion_Date DATETIME,

    -- ======================================================
    -- AI Analytics
    -- ======================================================

    Demand_Prediction_Score DECIMAL(5,2),

    Critical_Level_Flag BOOLEAN DEFAULT FALSE,

    AI_Recommendation TEXT,

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
    -- Foreign Keys
    -- ======================================================

    CONSTRAINT FK_BloodBank_Patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT FK_BloodBank_Doctor
        FOREIGN KEY (Requested_By_Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT FK_BloodBank_Department
        FOREIGN KEY (Department_ID)
        REFERENCES Departments(Department_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL

);

-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX IDX_BloodBank_Group
ON Blood_Bank(Blood_Group);

CREATE INDEX IDX_BloodBank_Component
ON Blood_Bank(Component_Type);

CREATE INDEX IDX_BloodBank_Status
ON Blood_Bank(Usage_Status);

CREATE INDEX IDX_BloodBank_Expiry
ON Blood_Bank(Expiry_Date);

CREATE INDEX IDX_BloodBank_Patient
ON Blood_Bank(Patient_ID);

CREATE INDEX IDX_BloodBank_Department
ON Blood_Bank(Department_ID);

CREATE INDEX IDX_BloodBank_Donation
ON Blood_Bank(Donation_Date);

CREATE INDEX IDX_BloodBank_Critical
ON Blood_Bank(Critical_Level_Flag);

-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Blood_Bank;