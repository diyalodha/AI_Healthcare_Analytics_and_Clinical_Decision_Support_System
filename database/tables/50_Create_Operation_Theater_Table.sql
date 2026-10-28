/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 50_Create_Operation_Theatre_Table.sql

Purpose : Create Operation Theatre Master Table

Description:
Stores operation theatre details including availability,
equipment status, maintenance schedules, utilization,
and AI-based resource optimization.

Version : 2.2

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

-- ==========================================================
-- Remove Existing Table
-- ==========================================================

DROP TABLE IF EXISTS Operation_Theatre;

-- ==========================================================
-- Create Table
-- ==========================================================

CREATE TABLE Operation_Theatre (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    OT_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),

    -- ======================================================
    -- Theatre Information
    -- ======================================================

    OT_Code VARCHAR(30)
        NOT NULL UNIQUE,

    OT_Name VARCHAR(100)
        NOT NULL,

    OT_Number VARCHAR(20)
        NOT NULL UNIQUE,

    Department_ID CHAR(36),

    OT_Type ENUM(
        'General',
        'Emergency',
        'Cardiac',
        'Neuro',
        'Orthopedic',
        'Robotic',
        'Gynecology',
        'ENT',
        'Ophthalmology',
        'Other'
    ) DEFAULT 'General',

    Floor_Number INT,

    Location VARCHAR(150),

    Capacity INT DEFAULT 1,

    Air_Conditioned BOOLEAN DEFAULT TRUE,

    Emergency_Ready BOOLEAN DEFAULT TRUE,

    Sterilization_Status ENUM(
        'Sterilized',
        'Pending',
        'In Progress'
    ) DEFAULT 'Sterilized',

    Is_Active BOOLEAN DEFAULT TRUE,

    -- ======================================================
    -- Availability Information
    -- ======================================================

    Availability_Status ENUM(
        'Available',
        'Occupied',
        'Reserved',
        'Maintenance'
    ) DEFAULT 'Available',

    Current_Status_Reason TEXT,

    -- ======================================================
    -- Equipment Information
    -- ======================================================

    Equipment_Status ENUM(
        'Operational',
        'Under Maintenance',
        'Unavailable'
    ) DEFAULT 'Operational',

    Major_Equipment TEXT,

    Last_Maintenance_Date DATE,

    Next_Maintenance_Date DATE,

    -- ======================================================
    -- Scheduling Information
    -- ======================================================

    Working_Start_Time TIME,

    Working_End_Time TIME,

    Average_Surgery_Duration_Minutes INT,

    Total_Surgeries_Performed INT DEFAULT 0,

    -- ======================================================
    -- AI Analytics
    -- ======================================================

    Utilization_Percentage DECIMAL(5,2),

    Predicted_Demand_Score DECIMAL(5,2),

    AI_Optimization_Recommendation TEXT,

    -- ======================================================
    -- Dataset Tracking
    -- ======================================================

    Data_Source ENUM(
        'Hospital_Records',
        'Synthetic'
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

    CONSTRAINT CHK_OT_Capacity
        CHECK (Capacity > 0),

    CONSTRAINT CHK_OT_Total_Surgeries
        CHECK (Total_Surgeries_Performed >= 0),

    CONSTRAINT CHK_OT_Utilization
        CHECK (
            Utilization_Percentage IS NULL
            OR (
                Utilization_Percentage >= 0
                AND Utilization_Percentage <= 100
            )
        ),

    CONSTRAINT CHK_OT_Demand
        CHECK (
            Predicted_Demand_Score IS NULL
            OR (
                Predicted_Demand_Score >= 0
                AND Predicted_Demand_Score <= 100
            )
        ),

    -- ======================================================
    -- Foreign Key
    -- ======================================================

    CONSTRAINT FK_OperationTheatre_Department
        FOREIGN KEY (Department_ID)
        REFERENCES Departments(Department_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL

);

-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX IDX_OT_Department
ON Operation_Theatre(Department_ID);

CREATE INDEX IDX_OT_Status
ON Operation_Theatre(Availability_Status);

CREATE INDEX IDX_OT_Type
ON Operation_Theatre(OT_Type);

CREATE INDEX IDX_OT_Equipment
ON Operation_Theatre(Equipment_Status);

CREATE INDEX IDX_OT_Active
ON Operation_Theatre(Is_Active);

-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Operation_Theatre;