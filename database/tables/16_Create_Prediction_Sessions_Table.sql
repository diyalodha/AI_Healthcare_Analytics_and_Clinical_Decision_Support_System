/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 16_Create_Prediction_Sessions_Table.sql

Purpose : Create AI Prediction Sessions Table

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Prediction_Sessions;

CREATE TABLE Prediction_Sessions (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Prediction_Session_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =====================================================
    -- Patient Reference
    -- =====================================================

    Patient_ID CHAR(36)
        NOT NULL,


    -- =====================================================
    -- Session Information
    -- =====================================================

    Prediction_Number VARCHAR(30)
        NOT NULL
        UNIQUE,


    Prediction_Date DATETIME
        DEFAULT CURRENT_TIMESTAMP,


    Prediction_Type ENUM(
        'Disease Risk',
        'Health Score',
        'Treatment Recommendation',
        'Clinical Decision',
        'Readmission Risk'
    )
    NOT NULL,


    Prediction_Status ENUM(
        'Processing',
        'Completed',
        'Failed'
    )
    DEFAULT 'Processing',


    Execution_Time_MS INT
        DEFAULT 0,


    Prediction_Count INT
        DEFAULT 1,


    Error_Message TEXT,


    -- =====================================================
    -- AI Model Information
    -- =====================================================

    AI_Model_ID CHAR(36),

    Model_Name VARCHAR(150)
        NOT NULL,

    Model_Version VARCHAR(50),

    Model_Type ENUM(
        'Machine Learning',
        'Deep Learning',
        'Rule Based',
        'Hybrid'
    )
    DEFAULT 'Machine Learning',

    -- =====================================================
    -- Prediction Results
    -- =====================================================

    Prediction_Score DECIMAL(6,2),

    Confidence_Score DECIMAL(6,2),

    Accuracy_Score DECIMAL(6,2),

    Precision_Score DECIMAL(6,2),

    Recall_Score DECIMAL(6,2),

    F1_Score DECIMAL(6,2),


    Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',


    Explainability_Status ENUM(
        'Pending',
        'Generated',
        'Verified'
    )
    DEFAULT 'Pending',


    -- =====================================================
    -- Dataset Information
    -- =====================================================

    Input_Feature_Count INT,

    Input_Data_Source ENUM(
        'MIMIC-IV',
        'Synthetic',
        'Hospital_Records',
        'Hybrid Dataset'
    )
    DEFAULT 'Synthetic',


    Dataset_Version VARCHAR(30),


    Model_Monitoring_Status ENUM(
        'Active',
        'Inactive',
        'Under Review'
    )
    DEFAULT 'Active',


    -- =====================================================
    -- Status
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

    CONSTRAINT fk_prediction_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,


    -- =====================================================
    -- Check Constraints
    -- =====================================================

    CONSTRAINT chk_prediction_execution_time
        CHECK (
            Execution_Time_MS >= 0
        ),

    CONSTRAINT chk_prediction_feature_count
        CHECK (
            Input_Feature_Count IS NULL
            OR Input_Feature_Count >= 0
        ),

    CONSTRAINT chk_prediction_count
        CHECK (
            Prediction_Count >= 1
        )

);


-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX idx_prediction_number
ON Prediction_Sessions(Prediction_Number);

CREATE INDEX idx_prediction_patient
ON Prediction_Sessions(Patient_ID);

CREATE INDEX idx_prediction_date
ON Prediction_Sessions(Prediction_Date);

CREATE INDEX idx_prediction_type
ON Prediction_Sessions(Prediction_Type);

CREATE INDEX idx_prediction_model
ON Prediction_Sessions(Model_Name);

CREATE INDEX idx_prediction_status
ON Prediction_Sessions(Prediction_Status);

CREATE INDEX idx_prediction_risk
ON Prediction_Sessions(Risk_Level);

CREATE INDEX idx_prediction_confidence
ON Prediction_Sessions(Confidence_Score);


-- =====================================================
-- Verification
-- =====================================================

SHOW TABLES;

DESCRIBE Prediction_Sessions;