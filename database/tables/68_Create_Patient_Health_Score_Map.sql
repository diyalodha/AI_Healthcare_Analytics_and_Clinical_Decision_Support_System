/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 68_Create_Patient_Health_Score_Map.sql

Purpose : Create Patient Health Score Mapping Table

Description :
Maps patients with their generated health scores and
related AI prediction sessions, diseases and doctors.

Supports:
- Patient health score history
- AI-generated health assessment
- Prediction session tracking
- Disease association
- Doctor review
- Health trend analysis
- Readmission risk analysis
- Dataset traceability

Version : 3.1

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- =========================================================
-- Remove Existing Table
-- Warning: This deletes existing data from this table.
-- =========================================================

DROP TABLE IF EXISTS Patient_Health_Score_Map;


-- =========================================================
-- Create Patient Health Score Mapping Table
-- =========================================================

CREATE TABLE Patient_Health_Score_Map (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Health_Score_Map_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =====================================================
    -- Foreign Key References
    -- =====================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Health_Score_ID CHAR(36)
        NOT NULL,

    Prediction_Session_ID CHAR(36)
        NULL,

    Disease_ID CHAR(36)
        NULL,

    Doctor_ID CHAR(36)
        NULL,


    -- =====================================================
    -- Mapping Information
    -- =====================================================

    Mapping_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Mapping_Date DATETIME
        NOT NULL
        DEFAULT CURRENT_TIMESTAMP,


    -- =====================================================
    -- Health Score Snapshot
    -- =====================================================

    Overall_Health_Score DECIMAL(5,2)
        NULL,

    Health_Category ENUM(
        'Excellent',
        'Good',
        'Moderate',
        'Poor',
        'Critical'
    )
        NULL,

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
        NULL
        DEFAULT 'Low',

    Health_Trend ENUM(
        'Improving',
        'Stable',
        'Declining'
    )
        NULL,


    -- =====================================================
    -- AI Information
    -- =====================================================

    AI_Confidence_Score DECIMAL(5,2)
        NULL,

    Predicted_Readmission_Risk DECIMAL(5,2)
        NULL,

    Major_Risk_Factors TEXT
        NULL,

    Improvement_Suggestions TEXT
        NULL,

    AI_Analysis_Used BOOLEAN
        NOT NULL
        DEFAULT TRUE,


    -- =====================================================
    -- Doctor Review
    -- =====================================================

    Reviewed_By_Doctor BOOLEAN
        NOT NULL
        DEFAULT FALSE,

    Doctor_Comments TEXT
        NULL,

    Review_Date DATETIME
        NULL,


    -- =====================================================
    -- Mapping Status
    -- =====================================================

    Mapping_Status ENUM(
        'Active',
        'Inactive',
        'Archived'
    )
        NOT NULL
        DEFAULT 'Active',


    -- =====================================================
    -- Dataset Tracking
    -- =====================================================

    Data_Source ENUM(
        'MIMIC-IV',
        'Synthetic',
        'Hospital_Records',
        'Hybrid Dataset'
    )
        NOT NULL
        DEFAULT 'Synthetic',

    Dataset_Version VARCHAR(30)
        NULL,


    -- =====================================================
    -- System Status
    -- =====================================================

    Is_Active BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    Is_Deleted BOOLEAN
        NOT NULL
        DEFAULT FALSE,

    Record_Version INT
        NOT NULL
        DEFAULT 1,


    -- =====================================================
    -- Audit Information
    -- =====================================================

    Created_By VARCHAR(50)
        NULL,

    Updated_By VARCHAR(50)
        NULL,

    Created_At TIMESTAMP
        NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,


    -- =====================================================
    -- Validation Constraints
    -- =====================================================

    CONSTRAINT chk_phsm_health_score
        CHECK (
            Overall_Health_Score IS NULL
            OR Overall_Health_Score BETWEEN 0 AND 100
        ),


    CONSTRAINT chk_phsm_ai_confidence
        CHECK (
            AI_Confidence_Score IS NULL
            OR AI_Confidence_Score BETWEEN 0 AND 100
        ),


    CONSTRAINT chk_phsm_readmission_risk
        CHECK (
            Predicted_Readmission_Risk IS NULL
            OR Predicted_Readmission_Risk BETWEEN 0 AND 100
        ),


    CONSTRAINT chk_phsm_record_version
        CHECK (
            Record_Version >= 1
        ),


    CONSTRAINT chk_phsm_review_date
        CHECK (
            Reviewed_By_Doctor = FALSE
            OR Review_Date IS NOT NULL
        ),


    -- =====================================================
    -- Foreign Key Constraints
    -- =====================================================

    CONSTRAINT fk_phsm_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,


    CONSTRAINT fk_phsm_health_score
        FOREIGN KEY (Health_Score_ID)
        REFERENCES Patient_Health_Score(Health_Score_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,


    CONSTRAINT fk_phsm_prediction_session
        FOREIGN KEY (Prediction_Session_ID)
        REFERENCES Prediction_Sessions(Prediction_Session_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_phsm_disease
        FOREIGN KEY (Disease_ID)
        REFERENCES Diseases(Disease_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_phsm_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL

);


-- =========================================================
-- Indexes
-- =========================================================

CREATE INDEX idx_phsm_patient
    ON Patient_Health_Score_Map(Patient_ID);


CREATE INDEX idx_phsm_health_score
    ON Patient_Health_Score_Map(Health_Score_ID);


CREATE INDEX idx_phsm_prediction_session
    ON Patient_Health_Score_Map(Prediction_Session_ID);


CREATE INDEX idx_phsm_disease
    ON Patient_Health_Score_Map(Disease_ID);


CREATE INDEX idx_phsm_doctor
    ON Patient_Health_Score_Map(Doctor_ID);


CREATE INDEX idx_phsm_mapping_date
    ON Patient_Health_Score_Map(Mapping_Date);


CREATE INDEX idx_phsm_health_category
    ON Patient_Health_Score_Map(Health_Category);


CREATE INDEX idx_phsm_ai_risk
    ON Patient_Health_Score_Map(AI_Risk_Level);


CREATE INDEX idx_phsm_health_trend
    ON Patient_Health_Score_Map(Health_Trend);


CREATE INDEX idx_phsm_mapping_status
    ON Patient_Health_Score_Map(Mapping_Status);


CREATE INDEX idx_phsm_reviewed
    ON Patient_Health_Score_Map(Reviewed_By_Doctor);


CREATE INDEX idx_phsm_source
    ON Patient_Health_Score_Map(Data_Source);


CREATE INDEX idx_phsm_active
    ON Patient_Health_Score_Map(Is_Active);


-- =========================================================
-- Verification
-- =========================================================

SHOW TABLES;

DESCRIBE Patient_Health_Score_Map;


-- =========================================================
-- Relationship Verification
-- =========================================================

SELECT
    TABLE_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'healthcare_ai_db'
  AND TABLE_NAME = 'Patient_Health_Score_Map'
  AND REFERENCED_TABLE_NAME IS NOT NULL;