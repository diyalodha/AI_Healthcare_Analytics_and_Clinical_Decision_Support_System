/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 40_Create_Model_Training_Datasets_Table.sql

Purpose : Create AI Model Training Dataset Management Table

Description:
Stores metadata of datasets used for AI model training,
validation, testing, preprocessing, versioning, and
dataset quality management.

Version : 2.2

Author  : Diya Lodha & Team
===========================================================
*/


USE healthcare_ai_db;



-- ==========================================================
-- Remove Existing Table
-- ==========================================================

DROP TABLE IF EXISTS Model_Training_Datasets;



-- ==========================================================
-- Table : Model_Training_Datasets
-- ==========================================================

CREATE TABLE Model_Training_Datasets (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Dataset_ID CHAR(36)
        NOT NULL PRIMARY KEY DEFAULT (UUID()),



    -- ======================================================
    -- Dataset Information
    -- ======================================================

    Dataset_Name VARCHAR(200)
        NOT NULL,

    Dataset_Version VARCHAR(50)
        NOT NULL,

    Dataset_Description TEXT,

    Dataset_Type ENUM(

        'Training',
        'Validation',
        'Testing',
        'Hybrid',
        'Synthetic',
        'Real'

    )
    DEFAULT 'Hybrid',


    Source_Name VARCHAR(200),

    Source_Type ENUM(

        'MIMIC-IV',
        'Hospital Records',
        'Synthetic Generator',
        'Hybrid'

    )
    DEFAULT 'Synthetic Generator',


    Data_Source ENUM(

        'MIMIC-IV',
        'Synthetic',
        'Hospital_Records',
        'Hybrid Dataset'

    )
    DEFAULT 'Synthetic',



    -- ======================================================
    -- Dataset Statistics
    -- ======================================================

    Number_Of_Records INT
        DEFAULT 0,

    Number_Of_Features INT
        DEFAULT 0,

    Target_Column VARCHAR(100),

    Feature_List TEXT,

    Missing_Value_Percentage DECIMAL(5,2)
        DEFAULT 0.00,

    Duplicate_Record_Count INT
        DEFAULT 0,

    Data_Quality_Score DECIMAL(5,2),



    -- ======================================================
    -- Data Processing Information
    -- ======================================================

    Preprocessing_Method TEXT,

    Feature_Engineering_Method TEXT,

    Normalization_Method VARCHAR(100),

    Encoding_Method VARCHAR(100),

    Train_Test_Split_Ratio VARCHAR(50),



    -- ======================================================
    -- Storage Information
    -- ======================================================

    Storage_Path VARCHAR(500),

    File_Format ENUM(

        'CSV',
        'JSON',
        'Parquet',
        'Database',
        'Other'

    )
    DEFAULT 'CSV',

    File_Size_MB DECIMAL(10,2),

    Checksum_Hash VARCHAR(128),



    -- ======================================================
    -- Model Usage Tracking
    -- ======================================================

    Used_For_Model VARCHAR(150),

    Model_Version VARCHAR(50),

    Dataset_Purpose TEXT,

    AI_Ready BOOLEAN
        DEFAULT TRUE,



    -- ======================================================
    -- Dataset Status
    -- ======================================================

    Dataset_Status ENUM(

        'Active',
        'Archived',
        'Deprecated'

    )
    DEFAULT 'Active',

    Is_Active BOOLEAN
        DEFAULT TRUE,



    -- ======================================================
    -- Ownership Information
    -- ======================================================

    Prepared_By VARCHAR(150),

    Approved_By VARCHAR(150),

    Approval_Status ENUM(

        'Pending',
        'Approved',
        'Rejected'

    )
    DEFAULT 'Pending',



    -- ======================================================
    -- Date Tracking
    -- ======================================================

    Created_Date DATE
        DEFAULT (CURRENT_DATE()),

    Last_Updated DATE,



    -- ======================================================
    -- Audit Information
    -- ======================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);



-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX IDX_Dataset_Name
ON Model_Training_Datasets(Dataset_Name);



CREATE INDEX IDX_Dataset_Type
ON Model_Training_Datasets(Dataset_Type);



CREATE INDEX IDX_Dataset_Status
ON Model_Training_Datasets(Dataset_Status);



CREATE INDEX IDX_Dataset_Source
ON Model_Training_Datasets(Source_Type);



CREATE INDEX IDX_Dataset_DataSource
ON Model_Training_Datasets(Data_Source);



CREATE INDEX IDX_Dataset_Model
ON Model_Training_Datasets(Used_For_Model);



CREATE INDEX IDX_Dataset_Approval
ON Model_Training_Datasets(Approval_Status);



CREATE INDEX IDX_Dataset_AIReady
ON Model_Training_Datasets(AI_Ready);



SHOW TABLES;

DESCRIBE Model_Training_Datasets;