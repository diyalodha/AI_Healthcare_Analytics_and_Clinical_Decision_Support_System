/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 66_Create_Patient_Explainable_AI_Results_Map.sql

Purpose : Create Patient Explainable AI Results Mapping Table

Description :
Maps patients to Explainable AI (XAI) results generated
from AI prediction sessions.

Stores patient-level explainability information including
prediction references, explanation method, important
features, confidence, doctor review and dataset tracking.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/


USE healthcare_ai_db;


-- =========================================================
-- Remove Existing Table
-- =========================================================

DROP TABLE IF EXISTS Patient_Explainable_AI_Results_Map;


-- =========================================================
-- Create Patient Explainable AI Results Mapping Table
-- =========================================================

CREATE TABLE Patient_Explainable_AI_Results_Map (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Patient_XAI_Map_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =====================================================
    -- Foreign Keys
    -- =====================================================

    Patient_ID CHAR(36)
        NOT NULL,

    XAI_Result_ID CHAR(36)
        NOT NULL,

    Prediction_Session_ID CHAR(36)
        NOT NULL,

    Disease_ID CHAR(36),


    -- =====================================================
    -- Patient XAI Mapping Information
    -- =====================================================

    Mapping_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Mapping_Date DATETIME
        NOT NULL
        DEFAULT CURRENT_TIMESTAMP,


    -- =====================================================
    -- Prediction Information
    -- =====================================================

    Prediction_Number VARCHAR(30),

    Prediction_Date DATETIME,

    Model_Name VARCHAR(150),

    Model_Version VARCHAR(50),


    -- =====================================================
    -- Explainability Information
    -- =====================================================

    Explanation_Method ENUM(
        'SHAP',
        'LIME',
        'Feature Importance',
        'Rule Based',
        'Integrated Gradients',
        'Attention Map',
        'Other'
    )
    DEFAULT 'SHAP',

    Important_Features TEXT,

    Feature_Contribution TEXT,

    Positive_Factors TEXT,

    Negative_Factors TEXT,

    Explanation_Text TEXT,

    Model_Decision TEXT,

    Confidence_Explanation TEXT,


    -- =====================================================
    -- AI Scores
    -- =====================================================

    Confidence_Score DECIMAL(6,2),

    Explanation_Score DECIMAL(6,2),

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',


    -- =====================================================
    -- Doctor Review
    -- =====================================================

    Reviewed_By_Doctor BOOLEAN
        DEFAULT FALSE,

    Doctor_Name VARCHAR(100),

    Doctor_Feedback TEXT,

    Doctor_Approval_Status ENUM(
        'Pending',
        'Approved',
        'Rejected',
        'Needs Review'
    )
    DEFAULT 'Pending',

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
    -- Status Information
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
    -- Validation Constraints
    -- =====================================================

    CONSTRAINT chk_pxai_confidence
        CHECK (
            Confidence_Score IS NULL
            OR Confidence_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_pxai_explanation_score
        CHECK (
            Explanation_Score IS NULL
            OR Explanation_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_pxai_record_version
        CHECK (
            Record_Version >= 1
        ),


    -- =====================================================
    -- Foreign Key Constraints
    -- IMPORTANT:
    -- Constraint names are unique to prevent Error 1826
    -- =====================================================

    CONSTRAINT fk_pxai_map_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_pxai_map_xai_result
        FOREIGN KEY (XAI_Result_ID)
        REFERENCES Explainable_AI_Results(XAI_Result_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_pxai_map_session
        FOREIGN KEY (Prediction_Session_ID)
        REFERENCES Prediction_Sessions(Prediction_Session_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_pxai_map_disease
        FOREIGN KEY (Disease_ID)
        REFERENCES Diseases(Disease_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL

);


-- =========================================================
-- Indexes
-- =========================================================

CREATE INDEX idx_pxai_map_patient
ON Patient_Explainable_AI_Results_Map(Patient_ID);


CREATE INDEX idx_pxai_map_xai
ON Patient_Explainable_AI_Results_Map(XAI_Result_ID);


CREATE INDEX idx_pxai_map_session
ON Patient_Explainable_AI_Results_Map(Prediction_Session_ID);


CREATE INDEX idx_pxai_map_disease
ON Patient_Explainable_AI_Results_Map(Disease_ID);


CREATE INDEX idx_pxai_map_prediction
ON Patient_Explainable_AI_Results_Map(Prediction_Number);


CREATE INDEX idx_pxai_map_date
ON Patient_Explainable_AI_Results_Map(Mapping_Date);


CREATE INDEX idx_pxai_map_method
ON Patient_Explainable_AI_Results_Map(Explanation_Method);


CREATE INDEX idx_pxai_map_model
ON Patient_Explainable_AI_Results_Map(Model_Name);


CREATE INDEX idx_pxai_map_risk
ON Patient_Explainable_AI_Results_Map(AI_Risk_Level);


CREATE INDEX idx_pxai_map_review
ON Patient_Explainable_AI_Results_Map(Doctor_Approval_Status);


CREATE INDEX idx_pxai_map_source
ON Patient_Explainable_AI_Results_Map(Data_Source);


-- =========================================================
-- Verification
-- =========================================================

SHOW TABLES;

DESCRIBE Patient_Explainable_AI_Results_Map;