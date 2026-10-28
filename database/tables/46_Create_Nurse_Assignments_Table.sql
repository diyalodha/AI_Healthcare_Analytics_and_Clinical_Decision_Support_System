/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 46_Create_Nurse_Assignments_Table.sql

Purpose : Create Nurse Assignment Tracking Table

Description:
Stores nurse allocation details for patients including
shift assignment, responsibility level, workload,
patient acuity, and room/bed allocation.
Nurse master table will be integrated later.

Version : 2.2

Author  : Diya Lodha & Team
===========================================================
*/


USE healthcare_ai_db;



-- ==========================================================
-- Remove Existing Table
-- ==========================================================

DROP TABLE IF EXISTS Nurse_Assignments;



-- ==========================================================
-- Table : Nurse_Assignments
-- ==========================================================

CREATE TABLE Nurse_Assignments (


    -- ======================================================
    -- Primary Key
    -- ======================================================

    Assignment_ID CHAR(36)
        NOT NULL PRIMARY KEY DEFAULT (UUID()),



    -- ======================================================
    -- References
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,


    Nurse_ID CHAR(36)
        NOT NULL,


    Department_ID CHAR(36),


    Room_ID CHAR(36),


    Bed_ID CHAR(36),



    -- ======================================================
    -- Assignment Details
    -- ======================================================

    Assignment_Date DATE
        NOT NULL,


    Shift_Type ENUM(

        'Morning',

        'Evening',

        'Night'

    )
    NOT NULL,


    Duty_Start_Time TIME,


    Duty_End_Time TIME,


    Responsibility_Level ENUM(

        'Primary Nurse',

        'Assistant Nurse',

        'Critical Care',

        'ICU Nurse',

        'Emergency Nurse'

    )
    DEFAULT 'Primary Nurse',


    Assignment_Priority ENUM(

        'Low',

        'Medium',

        'High',

        'Critical'

    )
    DEFAULT 'Medium',


    Patient_Acuity_Level ENUM(

        'Low',

        'Moderate',

        'High',

        'Critical'

    )
    DEFAULT 'Moderate',


    Overtime_Hours DECIMAL(4,2)
        DEFAULT 0.00,


    Assignment_Status ENUM(

        'Active',

        'Completed',

        'Transferred',

        'Cancelled'

    )
    DEFAULT 'Active',


    Notes TEXT,



    -- ======================================================
    -- Dataset Tracking
    -- ======================================================

    Data_Source ENUM(

        'Hospital_Records',

        'Synthetic',

        'AI Scheduler'

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
    -- Constraints
    -- ======================================================

    CONSTRAINT CHK_Overtime
        CHECK (Overtime_Hours >= 0),


    CONSTRAINT UK_Nurse_Assignment

        UNIQUE (
            Nurse_ID,
            Assignment_Date,
            Shift_Type
        ),



    -- ======================================================
    -- Foreign Keys
    -- ======================================================

    CONSTRAINT FK_Assignment_Patient

        FOREIGN KEY (Patient_ID)

        REFERENCES Patients(Patient_ID)

        ON UPDATE CASCADE

        ON DELETE CASCADE,


    CONSTRAINT FK_Assignment_Department

        FOREIGN KEY (Department_ID)

        REFERENCES Departments(Department_ID)

        ON UPDATE CASCADE

        ON DELETE SET NULL,


    CONSTRAINT FK_Assignment_Room

        FOREIGN KEY (Room_ID)

        REFERENCES Hospital_Rooms(Room_ID)

        ON UPDATE CASCADE

        ON DELETE SET NULL,


    CONSTRAINT FK_Assignment_Bed

        FOREIGN KEY (Bed_ID)

        REFERENCES Beds(Bed_ID)

        ON UPDATE CASCADE

        ON DELETE SET NULL

);



-- ==========================================================
-- Nurse_ID intentionally kept without FK
-- Nurse Master table will be added in a future version.
-- ==========================================================



-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX IDX_Assignment_Patient
ON Nurse_Assignments(Patient_ID);


CREATE INDEX IDX_Assignment_Nurse
ON Nurse_Assignments(Nurse_ID);


CREATE INDEX IDX_Assignment_Department
ON Nurse_Assignments(Department_ID);


CREATE INDEX IDX_Assignment_Room
ON Nurse_Assignments(Room_ID);


CREATE INDEX IDX_Assignment_Bed
ON Nurse_Assignments(Bed_ID);


CREATE INDEX IDX_Assignment_Date
ON Nurse_Assignments(Assignment_Date);


CREATE INDEX IDX_Assignment_Status
ON Nurse_Assignments(Assignment_Status);


CREATE INDEX IDX_Assignment_Shift
ON Nurse_Assignments(Shift_Type);



SHOW TABLES;

DESCRIBE Nurse_Assignments;