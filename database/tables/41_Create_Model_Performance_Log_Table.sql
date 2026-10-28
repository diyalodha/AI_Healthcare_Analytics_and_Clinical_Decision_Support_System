/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 41_Create_Model_Performance_Log_Table.sql

Purpose : Create AI Model Performance Tracking Table

Description:
Stores AI model training, validation, evaluation,
deployment monitoring, resource utilization, and
performance metrics for continuous model monitoring.

Version : 2.2

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;



-- ==========================================================
-- Remove Existing Table
-- ==========================================================

DROP TABLE IF EXISTS Model_Performance_Log;



-- ==========================================================
-- Table : Model_Performance_Log
-- ==========================================================

CREATE TABLE Model_Performance_Log (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Performance_Log_ID CHAR(36)
        NOT NULL PRIMARY KEY DEFAULT (UUID()),



    -- ======================================================
    -- Dataset Reference
    -- ======================================================

    Dataset_ID CHAR(36),



    -- ======================================================
    -- Model Information
    -- ======================================================

    Model_Name VARCHAR(150)
        NOT NULL,

    Model_Version VARCHAR(50)
        NOT NULL,

    Model_Type ENUM(

        'Machine Learning',
        'Deep Learning',
        'NLP',
        'Hybrid'

    )
    DEFAULT 'Machine Learning',

    Algorithm VARCHAR(150),

    Evaluation_Dataset VARCHAR(150),



    -- ======================================================
    -- Training Information
    -- ======================================================

    Training_Date DATETIME,

    Training_Record_Count INT,

    Feature_Count INT,

    Training_Time_Seconds DECIMAL(10,2),

    Inference_Time_MS DECIMAL(10,2),

    Training_Status ENUM(

        'Started',
        'Completed',
        'Failed',
        'Cancelled'

    )
    DEFAULT 'Completed',



    -- ======================================================
    -- Performance Metrics
    -- ======================================================

    Accuracy DECIMAL(6,3),

    Precision_Score DECIMAL(6,3),

    Recall_Score DECIMAL(6,3),

    F1_Score DECIMAL(6,3),

    ROC_AUC DECIMAL(6,3),

    Log_Loss DECIMAL(8,5),

    Validation_Method VARCHAR(100),



    -- ======================================================
    -- Resource Utilization
    -- ======================================================

    CPU_Usage_Percentage DECIMAL(5,2),

    GPU_Usage_Percentage DECIMAL(5,2),

    Memory_Usage_MB DECIMAL(10,2),



    -- ======================================================
    -- Deployment Monitoring
    -- ======================================================

    Model_Status ENUM(

        'Training',
        'Testing',
        'Production',
        'Archived'

    )
    DEFAULT 'Training',

    Deployment_Date DATETIME,

    Last_Monitoring_Date DATETIME,



    -- ======================================================
    -- Dataset Tracking
    -- ======================================================

    Data_Source ENUM(

        'MIMIC-IV',
        'Synthetic',
        'Hospital_Records',
        'Hybrid Dataset'

    )
    DEFAULT 'Synthetic',



    Notes TEXT,



    -- ======================================================
    -- Audit Information
    -- ======================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,



    -- ======================================================
    -- Foreign Key
    -- ======================================================

    CONSTRAINT FK_Performance_Dataset

        FOREIGN KEY (Dataset_ID)

        REFERENCES Model_Training_Datasets(Dataset_ID)

        ON UPDATE CASCADE

        ON DELETE SET NULL

);



-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX IDX_Performance_Dataset
ON Model_Performance_Log(Dataset_ID);



CREATE INDEX IDX_Performance_Model_Name
ON Model_Performance_Log(Model_Name);



CREATE INDEX IDX_Performance_Model_Version
ON Model_Performance_Log(Model_Version);



CREATE INDEX IDX_Performance_Model_Type
ON Model_Performance_Log(Model_Type);



CREATE INDEX IDX_Performance_Algorithm
ON Model_Performance_Log(Algorithm);



CREATE INDEX IDX_Performance_Status
ON Model_Performance_Log(Model_Status);



CREATE INDEX IDX_Performance_Training_Status
ON Model_Performance_Log(Training_Status);



CREATE INDEX IDX_Performance_Date
ON Model_Performance_Log(Training_Date);



SHOW TABLES;

DESCRIBE Model_Performance_Log;