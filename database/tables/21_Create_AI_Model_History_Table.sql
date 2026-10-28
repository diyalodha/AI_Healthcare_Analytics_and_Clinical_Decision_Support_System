/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 21_Create_AI_Model_History_Table.sql

Purpose : Create AI Model History Table

Description :
Stores complete lifecycle information of AI models
including training, validation, deployment,
performance monitoring and version history.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS AI_Model_History;

CREATE TABLE AI_Model_History (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Model_History_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),

    -- =====================================================
    -- Model Information
    -- =====================================================

    Model_Name VARCHAR(150)
        NOT NULL,

    Model_Version VARCHAR(50)
        NOT NULL,

    Model_Display_Name VARCHAR(200),

    Model_Type ENUM(
        'Machine Learning',
        'Deep Learning',
        'NLP',
        'Hybrid'
    )
    DEFAULT 'Machine Learning',

    Algorithm_Name VARCHAR(150),

    Framework VARCHAR(100),

    Programming_Language VARCHAR(50)
        DEFAULT 'Python',

    Model_File_Name VARCHAR(255),

    -- =====================================================
    -- Training Information
    -- =====================================================

    Training_Date DATETIME,

    Training_Duration_Minutes INT,

    Dataset_Name VARCHAR(150),

    Dataset_Version VARCHAR(50),

    Dataset_Size INT,

    Training_Record_Count INT,

    Validation_Record_Count INT,

    Test_Record_Count INT,

    Feature_Count INT,

    Target_Variable VARCHAR(100),

    Hyperparameters TEXT,

    Random_Seed INT
        DEFAULT 42,


    -- =====================================================
    -- Model Performance
    -- =====================================================

    Accuracy DECIMAL(5,2),

    Precision_Score DECIMAL(5,2),

    Recall_Score DECIMAL(5,2),

    F1_Score DECIMAL(5,2),

    ROC_AUC DECIMAL(5,2),

    Log_Loss DECIMAL(8,4),

    Cross_Validation_Score DECIMAL(5,2),

    -- =====================================================
    -- Deployment Information
    -- =====================================================

    Deployment_Status ENUM(
        'Development',
        'Testing',
        'Production',
        'Deprecated'
    )
    DEFAULT 'Development',

    Deployment_Date DATETIME,

    Last_Updated_Date DATETIME,

    Model_Status ENUM(
        'Active',
        'Inactive',
        'Archived'
    )
    DEFAULT 'Active',

    Prediction_Count INT
        DEFAULT 0,

    Average_Response_Time_MS DECIMAL(8,2),

    Average_Confidence DECIMAL(5,2),


    -- =====================================================
    -- Explainability
    -- =====================================================

    Explainability_Method VARCHAR(100),

    Supports_SHAP BOOLEAN
        DEFAULT FALSE,

    Supports_LIME BOOLEAN
        DEFAULT FALSE,

    Model_Description TEXT,

    Remarks TEXT,

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
    -- Check Constraints
    -- =====================================================

    CONSTRAINT chk_model_accuracy
        CHECK (
            Accuracy IS NULL
            OR Accuracy BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_model_precision
        CHECK (
            Precision_Score IS NULL
            OR Precision_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_model_recall
        CHECK (
            Recall_Score IS NULL
            OR Recall_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_model_f1
        CHECK (
            F1_Score IS NULL
            OR F1_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_model_auc
        CHECK (
            ROC_AUC IS NULL
            OR ROC_AUC BETWEEN 0 AND 100
        )

);

-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX idx_model_name
ON AI_Model_History(Model_Name);

CREATE INDEX idx_model_version
ON AI_Model_History(Model_Version);

CREATE INDEX idx_model_status
ON AI_Model_History(Deployment_Status);

CREATE INDEX idx_model_type
ON AI_Model_History(Model_Type);

CREATE INDEX idx_algorithm
ON AI_Model_History(Algorithm_Name);

CREATE INDEX idx_training_date
ON AI_Model_History(Training_Date);

CREATE INDEX idx_dataset
ON AI_Model_History(Dataset_Name);

CREATE INDEX idx_active_model
ON AI_Model_History(Model_Status);

-- =====================================================
-- Verification
-- =====================================================

SHOW TABLES;

DESCRIBE AI_Model_History;