/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 17_Create_Disease_Risk_Predictions_Table.sql

Purpose : Create Disease Risk Predictions Table

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Disease_Risk_Predictions;

CREATE TABLE Disease_Risk_Predictions (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Risk_Prediction_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =====================================================
    -- Foreign Keys
    -- =====================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Prediction_Session_ID CHAR(36)
        NOT NULL,

    Disease_ID CHAR(36)
        NOT NULL,


    -- =====================================================
    -- Prediction Information
    -- =====================================================

    Prediction_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Prediction_Date DATETIME
        DEFAULT CURRENT_TIMESTAMP,

    Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

    Risk_Probability DECIMAL(6,2),

    Prediction_Score DECIMAL(6,2),

    Confidence_Score DECIMAL(6,2),

    Risk_Rank INT
        DEFAULT 1,

    Predicted_Disease_Status ENUM(
        'At Risk',
        'Not At Risk',
        'Confirmed',
        'Recovered'
    )
    DEFAULT 'At Risk',

    -- =====================================================
    -- AI Model Information
    -- =====================================================

    Model_Name VARCHAR(150),

    Model_Version VARCHAR(50),

    Feature_Count INT,

    Important_Features TEXT,

    Explanation_Method VARCHAR(100),

    AI_Explanation TEXT,


    -- =====================================================
    -- Clinical Recommendation
    -- =====================================================

    Recommendation TEXT,

    Requires_Immediate_Action BOOLEAN
        DEFAULT FALSE,


    -- =====================================================
    -- Doctor Review
    -- =====================================================

    Doctor_Review_Status ENUM(
        'Pending',
        'Reviewed',
        'Approved',
        'Rejected'
    )
    DEFAULT 'Pending',

    Doctor_Comments TEXT,


    -- =====================================================
    -- Dataset Information
    -- =====================================================

    Data_Source ENUM(
        'MIMIC-IV',
        'Synthetic',
        'Hospital_Records',
        'Hybrid Dataset'
    )
    DEFAULT 'Synthetic',


    Dataset_Version VARCHAR(30),


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
    -- Audit
    -- =====================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    -- =====================================================
    -- Foreign Keys
    -- =====================================================

    CONSTRAINT fk_risk_prediction_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_risk_prediction_session
        FOREIGN KEY (Prediction_Session_ID)
        REFERENCES Prediction_Sessions(Prediction_Session_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_risk_prediction_disease
        FOREIGN KEY (Disease_ID)
        REFERENCES Diseases(Disease_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,


    -- =====================================================
    -- Check Constraints
    -- =====================================================

    CONSTRAINT chk_risk_probability
        CHECK (
            Risk_Probability IS NULL
            OR Risk_Probability BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_prediction_score
        CHECK (
            Prediction_Score IS NULL
            OR Prediction_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_confidence_score
        CHECK (
            Confidence_Score IS NULL
            OR Confidence_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_feature_count
        CHECK (
            Feature_Count IS NULL
            OR Feature_Count >= 0
        ),

    CONSTRAINT chk_risk_rank
        CHECK (
            Risk_Rank >= 1
        )

);


-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX idx_prediction_number
ON Disease_Risk_Predictions(Prediction_Number);

CREATE INDEX idx_risk_patient
ON Disease_Risk_Predictions(Patient_ID);

CREATE INDEX idx_risk_session
ON Disease_Risk_Predictions(Prediction_Session_ID);

CREATE INDEX idx_risk_disease
ON Disease_Risk_Predictions(Disease_ID);

CREATE INDEX idx_risk_level
ON Disease_Risk_Predictions(Risk_Level);

CREATE INDEX idx_risk_probability
ON Disease_Risk_Predictions(Risk_Probability);

CREATE INDEX idx_prediction_date
ON Disease_Risk_Predictions(Prediction_Date);

CREATE INDEX idx_doctor_review
ON Disease_Risk_Predictions(Doctor_Review_Status);

CREATE INDEX idx_immediate_action
ON Disease_Risk_Predictions(Requires_Immediate_Action);


-- =====================================================
-- Verification
-- =====================================================

SHOW TABLES;

DESCRIBE Disease_Risk_Predictions;