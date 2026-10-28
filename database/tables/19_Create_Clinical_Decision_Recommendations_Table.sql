/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 19_Create_Clinical_Decision_Recommendations_Table.sql

Purpose : Create Clinical Decision Recommendations Table

Description :
Stores AI generated clinical recommendations,
treatment suggestions, lifestyle advice,
investigations and doctor validation.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Clinical_Decision_Recommendations;

CREATE TABLE Clinical_Decision_Recommendations (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Recommendation_ID CHAR(36)
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

    Disease_ID CHAR(36),

    Diagnosis_ID CHAR(36),

    Doctor_ID CHAR(36),


    -- =====================================================
    -- Recommendation Information
    -- =====================================================

    Recommendation_Number VARCHAR(30)
        UNIQUE,

    Recommendation_Date DATETIME
        DEFAULT CURRENT_TIMESTAMP,

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
    -- Priority
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
    -- Foreign Keys
    -- =====================================================

    CONSTRAINT fk_recommendation_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_recommendation_session
        FOREIGN KEY (Prediction_Session_ID)
        REFERENCES Prediction_Sessions(Prediction_Session_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_recommendation_disease
        FOREIGN KEY (Disease_ID)
        REFERENCES Diseases(Disease_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_recommendation_diagnosis
        FOREIGN KEY (Diagnosis_ID)
        REFERENCES Diagnoses(Diagnosis_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_recommendation_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- =====================================================
    -- Check Constraints
    -- =====================================================

    CONSTRAINT chk_ai_confidence_recommendation
        CHECK (
            AI_Confidence_Score IS NULL
            OR AI_Confidence_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_followup_days
        CHECK (
            Followup_Days IS NULL
            OR Followup_Days >= 0
        )

);

-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX idx_recommendation_number
ON Clinical_Decision_Recommendations(Recommendation_Number);

CREATE INDEX idx_recommendation_patient
ON Clinical_Decision_Recommendations(Patient_ID);

CREATE INDEX idx_recommendation_session
ON Clinical_Decision_Recommendations(Prediction_Session_ID);

CREATE INDEX idx_recommendation_disease
ON Clinical_Decision_Recommendations(Disease_ID);

CREATE INDEX idx_recommendation_doctor
ON Clinical_Decision_Recommendations(Doctor_ID);

CREATE INDEX idx_recommendation_diagnosis
ON Clinical_Decision_Recommendations(Diagnosis_ID);

CREATE INDEX idx_recommendation_priority
ON Clinical_Decision_Recommendations(Priority_Level);

CREATE INDEX idx_recommendation_status
ON Clinical_Decision_Recommendations(Doctor_Approval_Status);

CREATE INDEX idx_recommendation_model
ON Clinical_Decision_Recommendations(Model_Name);

CREATE INDEX idx_recommendation_ai_risk
ON Clinical_Decision_Recommendations(AI_Risk_Level);

-- =====================================================
-- Verification
-- =====================================================

SHOW TABLES;

DESCRIBE Clinical_Decision_Recommendations;