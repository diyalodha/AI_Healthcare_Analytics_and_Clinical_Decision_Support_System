/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 69_Create_Patient_Prediction_Sessions_Map.sql

Purpose : Create Patient Prediction Sessions Mapping Table

Description :
Maps patients with AI prediction sessions and their related
clinical information.

Supports:
- Patient-wise AI prediction history
- Disease prediction tracking
- Diagnosis association
- Doctor association
- Admission association
- Health score association
- AI model traceability
- Dataset tracking

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- =========================================================
-- Remove Existing Table
-- =========================================================

DROP TABLE IF EXISTS Patient_Prediction_Sessions_Map;


-- =========================================================
-- Create Patient Prediction Sessions Mapping Table
-- =========================================================

CREATE TABLE Patient_Prediction_Sessions_Map (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Patient_Prediction_Map_ID CHAR(36)
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

    Doctor_ID CHAR(36),

    Disease_ID CHAR(36),

    Diagnosis_ID CHAR(36),

    Admission_ID CHAR(36),

    Health_Score_ID CHAR(36),


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
    -- Prediction Snapshot
    -- =====================================================

    Prediction_Type ENUM(
        'Disease Risk',
        'Health Score',
        'Readmission Risk',
        'Treatment Recommendation',
        'Clinical Decision',
        'Other'
    )
    DEFAULT 'Disease Risk',

    Predicted_Disease VARCHAR(200),

    Prediction_Result TEXT,

    Prediction_Confidence DECIMAL(5,2),

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',


    -- =====================================================
    -- AI Model Information
    -- =====================================================

    Model_Name VARCHAR(150),

    Model_Version VARCHAR(50),

    Prediction_Status ENUM(
        'Generated',
        'Reviewed',
        'Approved',
        'Rejected',
        'Completed'
    )
    DEFAULT 'Generated',


    -- =====================================================
    -- Clinical Context
    -- =====================================================

    Clinical_Context TEXT,

    Risk_Factors TEXT,

    Recommended_Action TEXT,

    Doctor_Reviewed BOOLEAN
        DEFAULT FALSE,

    Doctor_Feedback TEXT,

    Review_Date DATETIME,


    -- =====================================================
    -- Dataset Tracking
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

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Created_At TIMESTAMP
        NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,


    -- =====================================================
    -- Foreign Key Constraints
    -- =====================================================

    CONSTRAINT fk_ppsm_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,


    CONSTRAINT fk_ppsm_prediction_session
        FOREIGN KEY (Prediction_Session_ID)
        REFERENCES Prediction_Sessions(Prediction_Session_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,


    CONSTRAINT fk_ppsm_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_ppsm_disease
        FOREIGN KEY (Disease_ID)
        REFERENCES Diseases(Disease_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_ppsm_diagnosis
        FOREIGN KEY (Diagnosis_ID)
        REFERENCES Diagnoses(Diagnosis_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_ppsm_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_ppsm_health_score
        FOREIGN KEY (Health_Score_ID)
        REFERENCES Patient_Health_Score(Health_Score_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- =====================================================
    -- Validation Constraints
    -- =====================================================

    CONSTRAINT chk_ppsm_confidence
        CHECK (
            Prediction_Confidence IS NULL
            OR Prediction_Confidence BETWEEN 0 AND 100
        ),


    CONSTRAINT chk_ppsm_record_version
        CHECK (
            Record_Version >= 1
        ),


    CONSTRAINT chk_ppsm_review_date
        CHECK (
            Doctor_Reviewed = FALSE
            OR Review_Date IS NOT NULL
        )

);


-- =========================================================
-- Indexes
-- =========================================================

CREATE INDEX idx_ppsm_mapping_number
ON Patient_Prediction_Sessions_Map(Mapping_Number);


CREATE INDEX idx_ppsm_patient
ON Patient_Prediction_Sessions_Map(Patient_ID);


CREATE INDEX idx_ppsm_prediction_session
ON Patient_Prediction_Sessions_Map(Prediction_Session_ID);


CREATE INDEX idx_ppsm_doctor
ON Patient_Prediction_Sessions_Map(Doctor_ID);


CREATE INDEX idx_ppsm_disease
ON Patient_Prediction_Sessions_Map(Disease_ID);


CREATE INDEX idx_ppsm_diagnosis
ON Patient_Prediction_Sessions_Map(Diagnosis_ID);


CREATE INDEX idx_ppsm_admission
ON Patient_Prediction_Sessions_Map(Admission_ID);


CREATE INDEX idx_ppsm_health_score
ON Patient_Prediction_Sessions_Map(Health_Score_ID);


CREATE INDEX idx_ppsm_mapping_date
ON Patient_Prediction_Sessions_Map(Mapping_Date);


CREATE INDEX idx_ppsm_prediction_type
ON Patient_Prediction_Sessions_Map(Prediction_Type);


CREATE INDEX idx_ppsm_prediction_status
ON Patient_Prediction_Sessions_Map(Prediction_Status);


CREATE INDEX idx_ppsm_model
ON Patient_Prediction_Sessions_Map(Model_Name);


CREATE INDEX idx_ppsm_ai_risk
ON Patient_Prediction_Sessions_Map(AI_Risk_Level);


CREATE INDEX idx_ppsm_source
ON Patient_Prediction_Sessions_Map(Data_Source);


-- =========================================================
-- Verification
-- =========================================================

SHOW TABLES;

DESCRIBE Patient_Prediction_Sessions_Map;


-- =========================================================
-- Foreign Key Verification
-- =========================================================

SELECT
    TABLE_NAME,
    CONSTRAINT_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'healthcare_ai_db'
  AND TABLE_NAME = 'Patient_Prediction_Sessions_Map'
  AND REFERENCED_TABLE_NAME IS NOT NULL;