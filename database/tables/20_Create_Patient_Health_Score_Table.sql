/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 20_Create_Patient_Health_Score_Table.sql

Purpose : Create Patient Health Score Table

Description :
Stores AI generated overall health score, component
scores, risk assessment, trend information and doctor
review for each patient.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Patient_Health_Score;

CREATE TABLE Patient_Health_Score (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Health_Score_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =====================================================
    -- Foreign Keys
    -- =====================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Prediction_Session_ID CHAR(36),

    Disease_ID CHAR(36),

    Doctor_ID CHAR(36),


    -- =====================================================
    -- Score Information
    -- =====================================================

    Health_Score_Number VARCHAR(30)
        UNIQUE,

    Score_Date DATETIME
        DEFAULT CURRENT_TIMESTAMP,

    Overall_Health_Score DECIMAL(5,2),

    Health_Category ENUM(
        'Excellent',
        'Good',
        'Moderate',
        'Poor',
        'Critical'
    )
    DEFAULT 'Moderate',

    -- =====================================================
    -- Health Score Components
    -- =====================================================

    Physical_Health_Score DECIMAL(5,2),

    Mental_Health_Score DECIMAL(5,2),

    Chronic_Disease_Score DECIMAL(5,2),

    Lifestyle_Score DECIMAL(5,2),

    Nutrition_Score DECIMAL(5,2),

    Exercise_Score DECIMAL(5,2),

    Sleep_Score DECIMAL(5,2),

    Lab_Result_Score DECIMAL(5,2),

    Risk_Factor_Score DECIMAL(5,2),


    -- =====================================================
    -- AI Assessment
    -- =====================================================

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
    DEFAULT 'Low',

    AI_Confidence_Score DECIMAL(5,2),

    Health_Trend ENUM(
        'Improving',
        'Stable',
        'Declining'
    )
    DEFAULT 'Stable',

    Major_Risk_Factors TEXT,

    Improvement_Suggestions TEXT,

    Predicted_Readmission_Risk DECIMAL(5,2),


    -- =====================================================
    -- Doctor Review
    -- =====================================================

    Reviewed_By_Doctor BOOLEAN
        DEFAULT FALSE,

    Doctor_Comments TEXT,

    Review_Date DATETIME,

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

    CONSTRAINT fk_healthscore_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_healthscore_session
        FOREIGN KEY (Prediction_Session_ID)
        REFERENCES Prediction_Sessions(Prediction_Session_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_healthscore_disease
        FOREIGN KEY (Disease_ID)
        REFERENCES Diseases(Disease_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_healthscore_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    -- =====================================================
    -- Check Constraints
    -- =====================================================

    CONSTRAINT chk_overall_health_score
        CHECK (
            Overall_Health_Score IS NULL
            OR Overall_Health_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_ai_confidence_health
        CHECK (
            AI_Confidence_Score IS NULL
            OR AI_Confidence_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_readmission_risk
        CHECK (
            Predicted_Readmission_Risk IS NULL
            OR Predicted_Readmission_Risk BETWEEN 0 AND 100
        )

);

-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX idx_healthscore_number
ON Patient_Health_Score(Health_Score_Number);

CREATE INDEX idx_healthscore_patient
ON Patient_Health_Score(Patient_ID);

CREATE INDEX idx_healthscore_session
ON Patient_Health_Score(Prediction_Session_ID);

CREATE INDEX idx_healthscore_disease
ON Patient_Health_Score(Disease_ID);

CREATE INDEX idx_healthscore_doctor
ON Patient_Health_Score(Doctor_ID);

CREATE INDEX idx_healthscore_date
ON Patient_Health_Score(Score_Date);

CREATE INDEX idx_healthscore_category
ON Patient_Health_Score(Health_Category);

CREATE INDEX idx_healthscore_ai_risk
ON Patient_Health_Score(AI_Risk_Level);

CREATE INDEX idx_healthscore_trend
ON Patient_Health_Score(Health_Trend);

-- =====================================================
-- Verification
-- =====================================================

SHOW TABLES;

DESCRIBE Patient_Health_Score;