/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 22_Create_Users_Table.sql

Purpose : Create System Users Table

Description :
Stores login credentials, user roles, authentication,
security information and audit details for all
system users.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Users;

CREATE TABLE Users (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    User_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =====================================================
    -- User Information
    -- =====================================================

    Username VARCHAR(100)
        NOT NULL
        UNIQUE,

    Password_Hash VARCHAR(255)
        NOT NULL,

    Email VARCHAR(150)
        UNIQUE,

    Full_Name VARCHAR(150)
        NOT NULL,

    Phone VARCHAR(20),

    Doctor_ID CHAR(36),

    Employee_ID VARCHAR(30)
        UNIQUE,

    -- =====================================================
    -- User Type
    -- =====================================================

    User_Type ENUM(
        'Doctor',
        'Admin',
        'Nurse',
        'Receptionist',
        'Lab Technician',
        'Pharmacist',
        'Researcher',
        'Data Analyst',
        'AI_System'
    )
    DEFAULT 'Doctor',

    Role_Name VARCHAR(100),

    Department VARCHAR(100),

    Designation VARCHAR(100),


    -- =====================================================
    -- Account Status
    -- =====================================================

    Account_Status ENUM(
        'Active',
        'Inactive',
        'Locked',
        'Blocked'
    )
    DEFAULT 'Active',

    Email_Verified BOOLEAN
        DEFAULT FALSE,

    Last_Login DATETIME,

    Last_Logout DATETIME,

    Last_Login_IP VARCHAR(50),

    -- =====================================================
    -- Security Information
    -- =====================================================

    Failed_Login_Attempts INT
        DEFAULT 0,

    Password_Last_Changed DATETIME,

    Password_Expiry_Date DATETIME,

    Two_Factor_Enabled BOOLEAN
        DEFAULT FALSE,

    Account_Locked_Until DATETIME,

    Login_Count INT
        DEFAULT 0,


    -- =====================================================
    -- Status Information
    -- =====================================================

    Is_Active BOOLEAN
        DEFAULT TRUE,

    Is_Deleted BOOLEAN
        DEFAULT FALSE,

    Record_Version INT
        DEFAULT 1,

    -- =====================================================
    -- Audit Information
    -- =====================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,


    -- =====================================================
    -- Foreign Key
    -- =====================================================

    CONSTRAINT fk_user_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- =====================================================
    -- Check Constraints
    -- =====================================================

    CONSTRAINT chk_failed_attempts
        CHECK (
            Failed_Login_Attempts >= 0
        ),

    CONSTRAINT chk_login_count
        CHECK (
            Login_Count >= 0
        )

);

-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX idx_user_username
ON Users(Username);

CREATE INDEX idx_user_email
ON Users(Email);

CREATE INDEX idx_user_status
ON Users(Account_Status);

CREATE INDEX idx_user_type
ON Users(User_Type);

CREATE INDEX idx_user_doctor
ON Users(Doctor_ID);

CREATE INDEX idx_user_employee
ON Users(Employee_ID);

CREATE INDEX idx_user_active
ON Users(Is_Active);

-- =====================================================
-- Verification
-- =====================================================

SHOW TABLES;

DESCRIBE Users;