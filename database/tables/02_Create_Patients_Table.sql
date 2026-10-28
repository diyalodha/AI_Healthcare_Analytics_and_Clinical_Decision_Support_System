/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 02_Create_Patients_Table.sql
Purpose : Create Patients Master Table
Version : 3.1
Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

-- ===========================================================
-- Drop Existing Table (Optional)
-- ===========================================================

DROP TABLE IF EXISTS Patients;

-- ===========================================================
-- Create Patients Master Table
-- ===========================================================

CREATE TABLE Patients (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Patient_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),

    -- =======================================================
    -- Personal Information
    -- =======================================================

    First_Name VARCHAR(100) NOT NULL,

    Middle_Name VARCHAR(100),

    Last_Name VARCHAR(100) NOT NULL,

    Date_of_Birth DATE NOT NULL,

    Gender ENUM(
        'Male',
        'Female',
        'Other'
    ) NOT NULL,

    Blood_Group ENUM(
        'A+',
        'A-',
        'B+',
        'B-',
        'AB+',
        'AB-',
        'O+',
        'O-'
    ),

    Nationality VARCHAR(50)
        DEFAULT 'Indian',

    Preferred_Language VARCHAR(50)
        DEFAULT 'English',

    -- =======================================================
    -- Physical Information
    -- =======================================================

    Height_cm DECIMAL(5,2),

    Weight_kg DECIMAL(5,2),

    BMI DECIMAL(5,2),

    -- =======================================================
    -- Contact Information
    -- =======================================================

    Phone VARCHAR(20) UNIQUE,

    Alternate_Phone VARCHAR(20),

    Email VARCHAR(100) UNIQUE,

    Government_ID_Type ENUM(
        'Aadhaar',
        'PAN',
        'Passport',
        'Driving License',
        'Voter ID',
        'Other'
    ),

    Government_ID VARCHAR(30) UNIQUE,

    -- =======================================================
    -- Address Information
    -- =======================================================

    Address_Line VARCHAR(255),

    City VARCHAR(100),

    State VARCHAR(100),

    Postal_Code VARCHAR(10),

    Country VARCHAR(100)
        DEFAULT 'India',

    -- =======================================================
    -- Personal Details
    -- =======================================================

    Occupation VARCHAR(100),

    Marital_Status ENUM(
        'Single',
        'Married',
        'Divorced',
        'Widowed'
    ),

    -- =======================================================
    -- Lifestyle Information
    -- =======================================================

    Smoking_Status ENUM(
        'Never',
        'Former',
        'Current'
    )
    DEFAULT 'Never',

    Alcohol_Consumption ENUM(
        'Never',
        'Occasional',
        'Regular'
    )
    DEFAULT 'Never',

    Physical_Activity ENUM(
        'Low',
        'Moderate',
        'High'
    )
    DEFAULT 'Moderate',

    Family_History BOOLEAN
        DEFAULT FALSE,

    Known_Allergies TEXT,

    Organ_Donor BOOLEAN
        DEFAULT FALSE,

    Disability_Status BOOLEAN
        DEFAULT FALSE,

    -- =======================================================
    -- Emergency Contact
    -- =======================================================

    Emergency_Contact_Name VARCHAR(100),

    Emergency_Contact_Number VARCHAR(20),

    Emergency_Contact_Relationship VARCHAR(50),

    -- =======================================================
    -- Registration Information
    -- =======================================================

    Registration_Date DATE NOT NULL,

    Registration_Source ENUM(
        'Walk-In',
        'Online',
        'Referral',
        'Emergency'
    )
    DEFAULT 'Walk-In',

    Last_Visit_Date DATE,

    -- =======================================================
    -- AI Helper Information
    -- =======================================================

    Risk_Category ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

    Primary_Disease_ID CHAR(36),

    Latest_Health_Score DECIMAL(5,2),

    -- =======================================================
    -- Patient Status
    -- =======================================================

    Status ENUM(
        'Active',
        'Inactive',
        'Deceased'
    )
    DEFAULT 'Active',

    Date_of_Death DATE,

    Profile_Photo_URL VARCHAR(255),

    -- =======================================================
    -- System Information
    -- =======================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Is_Deleted BOOLEAN
        DEFAULT FALSE,

    Is_Active BOOLEAN
        DEFAULT TRUE,

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
    -- CHECK Constraints
    -- =======================================================

    CONSTRAINT chk_height
        CHECK (
            Height_cm IS NULL
            OR Height_cm BETWEEN 30 AND 250
        ),

    CONSTRAINT chk_weight
        CHECK (
            Weight_kg IS NULL
            OR Weight_kg BETWEEN 1 AND 350
        ),

    CONSTRAINT chk_bmi
        CHECK (
            BMI IS NULL
            OR BMI BETWEEN 5 AND 100
        ),

    CONSTRAINT chk_death_date
        CHECK (
            Date_of_Death IS NULL
            OR Date_of_Death >= Date_of_Birth
        )

);

-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_patient_name
ON Patients(Last_Name, First_Name);

CREATE INDEX idx_patient_phone
ON Patients(Phone);

CREATE INDEX idx_patient_email
ON Patients(Email);

CREATE INDEX idx_patient_city
ON Patients(City);

CREATE INDEX idx_patient_state
ON Patients(State);

CREATE INDEX idx_patient_registration
ON Patients(Registration_Date);

CREATE INDEX idx_patient_status
ON Patients(Status);

CREATE INDEX idx_patient_dob
ON Patients(Date_of_Birth);

CREATE INDEX idx_patient_blood_group
ON Patients(Blood_Group);

CREATE INDEX idx_patient_created
ON Patients(Created_At);

CREATE INDEX idx_patient_risk
ON Patients(Risk_Category);

-- ===========================================================
-- Verify Table
-- ===========================================================

SHOW TABLES;

DESCRIBE Patients;