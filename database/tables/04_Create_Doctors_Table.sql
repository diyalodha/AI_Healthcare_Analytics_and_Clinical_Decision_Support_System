/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 04_Create_Doctors_Table.sql
Purpose : Create Doctors Master Table
Version : 3.0
Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- ===========================================================
-- Create Doctors Table
-- ===========================================================

CREATE TABLE IF NOT EXISTS Doctors (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Doctor_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =======================================================
    -- Personal Information
    -- =======================================================

    First_Name VARCHAR(100)
        NOT NULL,

    Middle_Name VARCHAR(100),

    Last_Name VARCHAR(100)
        NOT NULL,

    Gender ENUM(
        'Male',
        'Female',
        'Other'
    ) NOT NULL,

    Date_of_Birth DATE,


    -- =======================================================
    -- Professional Information
    -- =======================================================

    Medical_License_No VARCHAR(50)
        NOT NULL
        UNIQUE,

    Qualification VARCHAR(150)
        NOT NULL,

    Specialization VARCHAR(100)
        NOT NULL,

    Years_of_Experience INT
        DEFAULT 0,

    Consultation_Fee DECIMAL(10,2)
        DEFAULT 0,

    Consultation_Duration_Minutes INT
        DEFAULT 20,


    -- =======================================================
    -- Department Information
    -- =======================================================

    Department_ID CHAR(36)
        NOT NULL,


    -- =======================================================
    -- Contact Information
    -- =======================================================

    Phone VARCHAR(20)
        UNIQUE,

    Email VARCHAR(100)
        UNIQUE,

    Profile_Photo_URL VARCHAR(255),


    -- =======================================================
    -- Employment Information
    -- =======================================================

    Joining_Date DATE
        NOT NULL,

    Shift ENUM(
        'Morning',
        'Evening',
        'Night',
        'Rotational'
    )
    DEFAULT 'Morning',

    Employment_Type ENUM(
        'Full-Time',
        'Part-Time',
        'Visiting'
    )
    DEFAULT 'Full-Time',

    Availability_Status ENUM(
        'Available',
        'Busy',
        'On Leave',
        'Emergency Duty'
    )
    DEFAULT 'Available',


    -- =======================================================
    -- Status Information
    -- =======================================================

    Status ENUM(
        'Active',
        'Inactive',
        'On Leave'
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

    CONSTRAINT chk_experience
        CHECK (
            Years_of_Experience >= 0
        ),

    CONSTRAINT chk_fee
        CHECK (
            Consultation_Fee >= 0
        ),

    CONSTRAINT chk_duration
        CHECK (
            Consultation_Duration_Minutes > 0
        ),


    -- =======================================================
    -- Foreign Key
    -- =======================================================

    CONSTRAINT fk_doctor_department

        FOREIGN KEY (Department_ID)

        REFERENCES Departments(Department_ID)

        ON UPDATE CASCADE

        ON DELETE RESTRICT

);


-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_doctor_department
ON Doctors(Department_ID);

CREATE INDEX idx_doctor_specialization
ON Doctors(Specialization);

CREATE INDEX idx_doctor_license
ON Doctors(Medical_License_No);

CREATE INDEX idx_doctor_status
ON Doctors(Status);

CREATE INDEX idx_doctor_name
ON Doctors(Last_Name, First_Name);

CREATE INDEX idx_doctor_gender
ON Doctors(Gender);

CREATE INDEX idx_doctor_email
ON Doctors(Email);

CREATE INDEX idx_doctor_phone
ON Doctors(Phone);

CREATE INDEX idx_doctor_shift
ON Doctors(Shift);

CREATE INDEX idx_doctor_availability
ON Doctors(Availability_Status);


-- ===========================================================
-- Verification
-- ===========================================================

SHOW TABLES;

DESCRIBE Doctors;