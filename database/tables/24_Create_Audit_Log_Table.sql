/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 24_Create_Audit_Log_Table.sql

Purpose : Create Audit Log Tracking Table

Description :
Stores complete activity history of users, AI models,
API calls and database operations for security,
monitoring and compliance.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Audit_Log;

CREATE TABLE Audit_Log (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Audit_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),

    -- =====================================================
    -- User Information
    -- =====================================================

    User_ID CHAR(36),

    Session_ID CHAR(36),

    Username VARCHAR(100),

    User_Role VARCHAR(100),

    -- =====================================================
    -- Activity Information
    -- =====================================================

    Action_Type ENUM(
        'LOGIN',
        'LOGOUT',
        'INSERT',
        'UPDATE',
        'DELETE',
        'VIEW',
        'DOWNLOAD',
        'UPLOAD',
        'EXPORT',
        'IMPORT',
        'AI_PREDICTION',
        'MODEL_TRAINING',
        'REPORT_GENERATION',
        'API_CALL'
    )
    NOT NULL,

    Module_Name VARCHAR(100),

    Table_Name VARCHAR(100),

    Record_ID CHAR(36),

    Action_Description TEXT,

    Request_Method ENUM(
        'GET',
        'POST',
        'PUT',
        'DELETE',
        'PATCH'
    ),

    API_Endpoint VARCHAR(255),

    -- =====================================================
    -- Security Information
    -- =====================================================

    IP_Address VARCHAR(50),

    MAC_Address VARCHAR(50),

    Device_Information VARCHAR(255),

    Browser VARCHAR(100),

    Operating_System VARCHAR(100),

    Location VARCHAR(150),

    Action_Status ENUM(
        'Success',
        'Failed'
    )
    DEFAULT 'Success',

    Error_Message TEXT,

    Response_Time_MS INT,

    Severity_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

    -- =====================================================
    -- AI Tracking
    -- =====================================================

    AI_Model_Name VARCHAR(150),

    Prediction_Session_ID CHAR(36),

    -- =====================================================
    -- Status Information
    -- =====================================================

    Is_Active BOOLEAN
        DEFAULT TRUE,

    Record_Version INT
        DEFAULT 1,

    -- =====================================================
    -- Audit Information
    -- =====================================================

    Action_Timestamp DATETIME
        DEFAULT CURRENT_TIMESTAMP,

    Created_By VARCHAR(50),

    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    -- =====================================================
    -- Foreign Key
    -- =====================================================

    CONSTRAINT fk_audit_user
        FOREIGN KEY (User_ID)
        REFERENCES Users(User_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX idx_audit_user
ON Audit_Log(User_ID);

CREATE INDEX idx_audit_session
ON Audit_Log(Session_ID);

CREATE INDEX idx_audit_username
ON Audit_Log(Username);

CREATE INDEX idx_audit_action
ON Audit_Log(Action_Type);

CREATE INDEX idx_audit_module
ON Audit_Log(Module_Name);

CREATE INDEX idx_audit_table
ON Audit_Log(Table_Name);

CREATE INDEX idx_audit_record
ON Audit_Log(Record_ID);

CREATE INDEX idx_audit_status
ON Audit_Log(Action_Status);

CREATE INDEX idx_audit_timestamp
ON Audit_Log(Action_Timestamp);

CREATE INDEX idx_audit_prediction
ON Audit_Log(Prediction_Session_ID);

-- =====================================================
-- Verification
-- =====================================================

SHOW TABLES;

DESCRIBE Audit_Log;