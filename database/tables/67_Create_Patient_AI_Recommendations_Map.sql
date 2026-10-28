/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 67_Create_Patient_AI_Recommendations_Map.sql

Purpose : Create Patient AI Recommendations Mapping Table

Description :
Maps patients with AI-generated clinical recommendations.

Stores recommendation details, prediction session,
disease/diagnosis information, AI confidence, risk level,
doctor validation, follow-up information and dataset
tracking.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- =========================================================
-- Remove Existing Table
-- =========================================================

DROP TABLE IF EXISTS Patient_AI_Recommendations_Map;


-- =========================================================
-- Create Patient AI Recommendations Mapping Table
-- =========================================================

CREATE TABLE Patient_AI_Recommendations_Map (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Patient_AI_Recommendation_Map_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =====================================================
    -- Foreign Keys
    -- =====================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Recommendation_ID CHAR(36)
        NOT NULL,

    Prediction_Session_ID CHAR(36)
        NOT NULL,

    Disease_ID CHAR(36),

    Diagnosis_ID CHAR(36),

    Doctor_ID CHAR(36),


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
    -- Recommendation Information
    -- =====================================================

    Recommendation_Number VARCHAR(30),

    Recommendation_Date DATETIME,

    Recommendation_Type ENUM(
        'Medication',
        'Lifestyle',
        'Investigation',
        'Treatment',
        'Monitoring',
        'Hospitalization',
        'Referral',
        'Preventive Care'
    )
    DEFAULT 'Monitoring',

    Recommended_Action TEXT,

    Clinical_Reason TEXT,

    Expected_Outcome TEXT,

    Recommendation_Status ENUM(
        'Generated',
        'Sent',
        'Accepted',
        'Rejected',
        'Completed'
    )
    DEFAULT 'Generated',


    -- =====================================================
    -- AI Information
    -- =====================================================

    Model_Name VARCHAR(150),

    Model_Version VARCHAR(50),

    AI_Confidence_Score DECIMAL(6,2),

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',


    -- =====================================================
    -- Priority & Follow-Up
    -- =====================================================

    Priority_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Medium',

    Requires_Immediate_Action BOOLEAN
        DEFAULT FALSE,

    Followup_Recommended BOOLEAN
        DEFAULT FALSE,

    Followup_Days INT,


    -- =====================================================
    -- Doctor Validation
    -- =====================================================

    Doctor_Approval_Status ENUM(
        'Pending',
        'Approved',
        'Rejected',
        'Modified'
    )
    DEFAULT 'Pending',

    Doctor_Feedback TEXT,

    Reviewed_Date DATETIME,


    -- =====================================================
    -- Dataset Tracking
    -- =====================================================

    Data_Source ENUM(
        'Synthetic',
        'Hospital_Records',
        'MIMIC-IV',
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

    CONSTRAINT chk_pair_ai_confidence
        CHECK (
            AI_Confidence_Score IS NULL
            OR AI_Confidence_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_pair_followup_days
        CHECK (
            Followup_Days IS NULL
            OR Followup_Days >= 0
        ),

    CONSTRAINT chk_pair_record_version
        CHECK (
            Record_Version >= 1
        ),


    -- =====================================================
    -- Foreign Key Constraints
    -- Unique names prevent Error 1826
    -- =====================================================

    CONSTRAINT fk_pair_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_pair_recommendation
        FOREIGN KEY (Recommendation_ID)
        REFERENCES Clinical_Decision_Recommendations(Recommendation_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_pair_session
        FOREIGN KEY (Prediction_Session_ID)
        REFERENCES Prediction_Sessions(Prediction_Session_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_pair_disease
        FOREIGN KEY (Disease_ID)
        REFERENCES Diseases(Disease_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_pair_diagnosis
        FOREIGN KEY (Diagnosis_ID)
        REFERENCES Diagnoses(Diagnosis_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_pair_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL

);


-- =========================================================
-- Indexes
-- =========================================================

CREATE INDEX idx_pair_patient
ON Patient_AI_Recommendations_Map(Patient_ID);


CREATE INDEX idx_pair_recommendation
ON Patient_AI_Recommendations_Map(Recommendation_ID);


CREATE INDEX idx_pair_session
ON Patient_AI_Recommendations_Map(Prediction_Session_ID);


CREATE INDEX idx_pair_disease
ON Patient_AI_Recommendations_Map(Disease_ID);


CREATE INDEX idx_pair_diagnosis
ON Patient_AI_Recommendations_Map(Diagnosis_ID);


CREATE INDEX idx_pair_doctor
ON Patient_AI_Recommendations_Map(Doctor_ID);


CREATE INDEX idx_pair_mapping_number
ON Patient_AI_Recommendations_Map(Mapping_Number);


CREATE INDEX idx_pair_recommendation_number
ON Patient_AI_Recommendations_Map(Recommendation_Number);


CREATE INDEX idx_pair_date
ON Patient_AI_Recommendations_Map(Mapping_Date);


CREATE INDEX idx_pair_type
ON Patient_AI_Recommendations_Map(Recommendation_Type);


CREATE INDEX idx_pair_status
ON Patient_AI_Recommendations_Map(Recommendation_Status);


CREATE INDEX idx_pair_priority
ON Patient_AI_Recommendations_Map(Priority_Level);


CREATE INDEX idx_pair_ai_risk
ON Patient_AI_Recommendations_Map(AI_Risk_Level);


CREATE INDEX idx_pair_doctor_status
ON Patient_AI_Recommendations_Map(Doctor_Approval_Status);


CREATE INDEX idx_pair_source
ON Patient_AI_Recommendations_Map(Data_Source);


-- =========================================================
-- Verification
-- =========================================================

SHOW TABLES;

DESCRIBE Patient_AI_Recommendations_Map;