/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 63_Create_Patient_Lab_Results_Map.sql

Purpose : Create Patient Laboratory Results Mapping Table

Description:
Stores the relationship between patients and laboratory result
records. Captures laboratory test identification, result values,
clinical interpretation, verification status, AI analysis,
risk category, model-training usage and dataset source.

The Lab_Results table is the transaction table and Lab_Tests
is the laboratory test master table.

Version : 2.4
===========================================================
*/

USE healthcare_ai_db;


-- ==========================================================
-- Remove Existing Table
-- Warning: This deletes existing data from this table.
-- ==========================================================

DROP TABLE IF EXISTS Patient_Lab_Results_Map;


-- ==========================================================
-- Create Patient Laboratory Results Mapping Table
-- ==========================================================

CREATE TABLE Patient_Lab_Results_Map (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Lab_Result_Map_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Key References
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Lab_Result_ID CHAR(36)
        NOT NULL,

    Lab_Test_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36)
        NULL,

    Appointment_ID CHAR(36)
        NULL,

    Admission_ID CHAR(36)
        NULL,

    Diagnosis_ID CHAR(36)
        NULL,


    -- ======================================================
    -- Laboratory Order Information
    -- ======================================================

    Lab_Order_Number VARCHAR(30)
        NULL,

    Lab_Order_ID CHAR(36)
        NULL,


    -- ======================================================
    -- Test Timeline
    -- ======================================================

    Test_Date DATETIME
        NOT NULL,

    Sample_Type VARCHAR(100)
        NULL,

    Sample_Collected_Date DATETIME
        NULL,

    Result_Date DATETIME
        NULL,


    -- ======================================================
    -- Result Classification
    -- ======================================================

    Result_Category ENUM(
        'Hematology',
        'Biochemistry',
        'Microbiology',
        'Pathology',
        'Imaging',
        'Other'
    )
        NOT NULL DEFAULT 'Other',


    -- ======================================================
    -- Laboratory Result Values
    -- ======================================================

    Result_Value VARCHAR(255)
        NULL,

    Numeric_Result_Value DECIMAL(10,2)
        NULL,

    Unit VARCHAR(50)
        NULL,

    Reference_Min_Value DECIMAL(10,2)
        NULL,

    Reference_Max_Value DECIMAL(10,2)
        NULL,


    -- ======================================================
    -- Clinical Interpretation
    -- ======================================================

    Result_Status ENUM(
        'Normal',
        'Abnormal',
        'Critical',
        'Pending'
    )
        NOT NULL DEFAULT 'Pending',

    Abnormal_Flag BOOLEAN
        NOT NULL DEFAULT FALSE,

    Severity_Score INT
        NOT NULL DEFAULT 0,

    Clinical_Interpretation TEXT
        NULL,

    Doctor_Remarks TEXT
        NULL,

    Technician_Name VARCHAR(100)
        NULL,

    Machine_Name VARCHAR(100)
        NULL,

    Verified_By VARCHAR(100)
        NULL,

    Verification_Status ENUM(
        'Pending',
        'Verified',
        'Rejected'
    )
        NOT NULL DEFAULT 'Pending',


    -- ======================================================
    -- AI Analytics
    -- ======================================================

    AI_Analyzed BOOLEAN
        NOT NULL DEFAULT FALSE,

    AI_Risk_Category ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
        NOT NULL DEFAULT 'Low',

    AI_Confidence_Score DECIMAL(5,2)
        NULL,

    Used_For_Model_Training BOOLEAN
        NOT NULL DEFAULT FALSE,


    -- ======================================================
    -- Dataset Source Tracking
    -- ======================================================

    Data_Source ENUM(
        'MIMIC-IV',
        'Synthetic',
        'Hospital_Records',
        'Hybrid Dataset'
    )
        NOT NULL DEFAULT 'Synthetic',


    -- ======================================================
    -- Status Information
    -- ======================================================

    Is_Active BOOLEAN
        NOT NULL DEFAULT TRUE,

    Is_Deleted BOOLEAN
        NOT NULL DEFAULT FALSE,

    Record_Version INT
        NOT NULL DEFAULT 1,


    -- ======================================================
    -- Audit Information
    -- ======================================================

    Created_By VARCHAR(50)
        NULL,

    Updated_By VARCHAR(50)
        NULL,

    Created_At TIMESTAMP
        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,


    -- ======================================================
    -- Validation Constraints
    -- ======================================================

    CONSTRAINT chk_plrm63_severity
        CHECK (
            Severity_Score BETWEEN 0 AND 100
        ),


    CONSTRAINT chk_plrm63_ai_confidence
        CHECK (
            AI_Confidence_Score IS NULL
            OR AI_Confidence_Score BETWEEN 0 AND 100
        ),


    CONSTRAINT chk_plrm63_reference_range
        CHECK (
            Reference_Min_Value IS NULL
            OR Reference_Max_Value IS NULL
            OR Reference_Min_Value <= Reference_Max_Value
        ),


    CONSTRAINT chk_plrm63_result_dates
        CHECK (
            Result_Date IS NULL
            OR Sample_Collected_Date IS NULL
            OR Result_Date >= Sample_Collected_Date
        ),


    CONSTRAINT chk_plrm63_record_version
        CHECK (
            Record_Version >= 1
        ),


    -- ======================================================
    -- Foreign Key Constraints
    --
    -- IMPORTANT:
    -- Constraint names are unique to File 63 to prevent
    -- MySQL Error Code 1826.
    -- ======================================================

    CONSTRAINT fk_plrm63_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,


    CONSTRAINT fk_plrm63_lab_result
        FOREIGN KEY (Lab_Result_ID)
        REFERENCES Lab_Results(Lab_Result_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,


    CONSTRAINT fk_plrm63_lab_test
        FOREIGN KEY (Lab_Test_ID)
        REFERENCES Lab_Tests(Lab_Test_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,


    CONSTRAINT fk_plrm63_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_plrm63_appointment
        FOREIGN KEY (Appointment_ID)
        REFERENCES Appointments(Appointment_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_plrm63_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_plrm63_diagnosis
        FOREIGN KEY (Diagnosis_ID)
        REFERENCES Diagnoses(Diagnosis_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- ======================================================
    -- Duplicate Record Prevention
    -- Each laboratory result can appear only once.
    -- ======================================================

    CONSTRAINT uk_plrm63_lab_result
        UNIQUE (
            Lab_Result_ID
        )

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_plrm63_patient
    ON Patient_Lab_Results_Map(Patient_ID);

CREATE INDEX idx_plrm63_lab_result
    ON Patient_Lab_Results_Map(Lab_Result_ID);

CREATE INDEX idx_plrm63_lab_test
    ON Patient_Lab_Results_Map(Lab_Test_ID);

CREATE INDEX idx_plrm63_doctor
    ON Patient_Lab_Results_Map(Doctor_ID);

CREATE INDEX idx_plrm63_appointment
    ON Patient_Lab_Results_Map(Appointment_ID);

CREATE INDEX idx_plrm63_admission
    ON Patient_Lab_Results_Map(Admission_ID);

CREATE INDEX idx_plrm63_diagnosis
    ON Patient_Lab_Results_Map(Diagnosis_ID);

CREATE INDEX idx_plrm63_order_number
    ON Patient_Lab_Results_Map(Lab_Order_Number);

CREATE INDEX idx_plrm63_order_id
    ON Patient_Lab_Results_Map(Lab_Order_ID);

CREATE INDEX idx_plrm63_test_date
    ON Patient_Lab_Results_Map(Test_Date);

CREATE INDEX idx_plrm63_result_date
    ON Patient_Lab_Results_Map(Result_Date);

CREATE INDEX idx_plrm63_category
    ON Patient_Lab_Results_Map(Result_Category);

CREATE INDEX idx_plrm63_result_status
    ON Patient_Lab_Results_Map(Result_Status);

CREATE INDEX idx_plrm63_abnormal
    ON Patient_Lab_Results_Map(Abnormal_Flag);

CREATE INDEX idx_plrm63_verification
    ON Patient_Lab_Results_Map(Verification_Status);

CREATE INDEX idx_plrm63_ai_analyzed
    ON Patient_Lab_Results_Map(AI_Analyzed);

CREATE INDEX idx_plrm63_ai_risk
    ON Patient_Lab_Results_Map(AI_Risk_Category);

CREATE INDEX idx_plrm63_training
    ON Patient_Lab_Results_Map(Used_For_Model_Training);

CREATE INDEX idx_plrm63_active
    ON Patient_Lab_Results_Map(Is_Active);

CREATE INDEX idx_plrm63_data_source
    ON Patient_Lab_Results_Map(Data_Source);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Patient_Lab_Results_Map;