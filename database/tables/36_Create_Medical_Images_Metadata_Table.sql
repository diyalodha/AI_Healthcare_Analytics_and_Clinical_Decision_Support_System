/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 36_Create_Medical_Images_Metadata_Table.sql

Purpose : Create Medical Images Metadata Table

Description:
Stores DICOM and medical image metadata required for
AI-based image processing, computer vision models,
dataset management, and imaging analytics.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

-- ==========================================================
-- Create Medical Images Metadata Table
-- ==========================================================

CREATE TABLE IF NOT EXISTS Medical_Images_Metadata (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Image_Metadata_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Keys
    -- ======================================================

    Imaging_Report_ID CHAR(36)
        NOT NULL,

    Patient_ID CHAR(36)
        NOT NULL,


    -- ======================================================
    -- Image Information
    -- ======================================================

    Image_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Image_File_Name VARCHAR(255)
        NOT NULL,

    Original_File_Name VARCHAR(255),

    Image_Format VARCHAR(20),

    Image_Size_MB DECIMAL(10,2),

    Storage_Path VARCHAR(500),

    Checksum_Hash VARCHAR(128),

    Image_Status ENUM(
        'Available',
        'Archived',
        'Deleted'
    )
    DEFAULT 'Available',


    -- ======================================================
    -- DICOM Information
    -- ======================================================

    DICOM_UID VARCHAR(255),

    Study_Instance_UID VARCHAR(255),

    Series_Instance_UID VARCHAR(255),

    SOP_Instance_UID VARCHAR(255),

    Modality VARCHAR(100),

    Body_Part VARCHAR(150),

    Image_Resolution VARCHAR(50),

    Pixel_Size VARCHAR(50),

    Slice_Count INT,

    Acquisition_Date DATETIME,


    -- ======================================================
    -- AI Processing Information
    -- ======================================================

    Is_Annotated BOOLEAN
        DEFAULT FALSE,

    Annotation_Status ENUM(
        'Pending',
        'Completed',
        'Verified'
    )
    DEFAULT 'Pending',

    Annotation_Details TEXT,

    AI_Processed BOOLEAN
        DEFAULT FALSE,

    AI_Processing_Status ENUM(
        'Pending',
        'Processing',
        'Completed',
        'Failed'
    )
    DEFAULT 'Pending',

    AI_Model_Name VARCHAR(150),

    AI_Model_Version VARCHAR(50),

    AI_Confidence_Score DECIMAL(5,2),

    Processing_Time_Seconds DECIMAL(8,2),


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


    -- ======================================================
    -- Status Information
    -- ======================================================

    Is_Active BOOLEAN
        DEFAULT TRUE,

    Record_Version INT
        DEFAULT 1,


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
    -- Foreign Key Constraints
    -- ======================================================

    CONSTRAINT fk_metadata_report
        FOREIGN KEY (Imaging_Report_ID)
        REFERENCES Imaging_Reports(Imaging_Report_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_metadata_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,


    -- ======================================================
    -- Check Constraints
    -- ======================================================

    CONSTRAINT chk_image_size
        CHECK (
            Image_Size_MB IS NULL
            OR Image_Size_MB >= 0
        ),

    CONSTRAINT chk_slice_count
        CHECK (
            Slice_Count IS NULL
            OR Slice_Count >= 0
        ),

    CONSTRAINT chk_ai_confidence_metadata
        CHECK (
            AI_Confidence_Score IS NULL
            OR AI_Confidence_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_processing_time
        CHECK (
            Processing_Time_Seconds IS NULL
            OR Processing_Time_Seconds >= 0
        )

);

-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_metadata_image_number
ON Medical_Images_Metadata(Image_Number);

CREATE INDEX idx_metadata_report
ON Medical_Images_Metadata(Imaging_Report_ID);

CREATE INDEX idx_metadata_patient
ON Medical_Images_Metadata(Patient_ID);

CREATE INDEX idx_metadata_modality
ON Medical_Images_Metadata(Modality);

CREATE INDEX idx_metadata_body_part
ON Medical_Images_Metadata(Body_Part);

CREATE INDEX idx_metadata_annotation
ON Medical_Images_Metadata(Annotation_Status);

CREATE INDEX idx_metadata_ai_status
ON Medical_Images_Metadata(AI_Processing_Status);

CREATE INDEX idx_metadata_ai_processed
ON Medical_Images_Metadata(AI_Processed);

CREATE INDEX idx_metadata_active
ON Medical_Images_Metadata(Is_Active);

-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Medical_Images_Metadata;