/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 55_Create_Patient_Insurance_Map.sql

Purpose : Create Patient-Insurance Mapping Table

Description:
Stores patient insurance-policy details, including provider,
policy validity, coverage, nominee, and claim information.

Version : 2.2
===========================================================
*/

USE healthcare_ai_db;


-- ==========================================================
-- Remove Existing Table
-- Warning: This deletes any existing table data.
-- ==========================================================

DROP TABLE IF EXISTS Patient_Insurance_Map;


-- ==========================================================
-- Create Patient Insurance Mapping Table
-- ==========================================================

CREATE TABLE Patient_Insurance_Map (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Patient_Insurance_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Key References
    -- ======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Insurance_ID CHAR(36)
        NOT NULL,


    -- ======================================================
    -- Policy Information
    -- ======================================================

    Policy_Number VARCHAR(100)
        NOT NULL,

    Policy_Type ENUM(
        'Individual',
        'Family Floater',
        'Group',
        'Corporate',
        'Government Scheme',
        'Other'
    )
        DEFAULT 'Individual',

    Policy_Holder_Name VARCHAR(150)
        NULL,

    Relationship_To_Policy_Holder VARCHAR(50)
        DEFAULT 'Self',

    Plan_Name VARCHAR(150)
        NULL,


    -- ======================================================
    -- Policy Validity
    -- ======================================================

    Policy_Start_Date DATE
        NOT NULL,

    Policy_End_Date DATE
        NOT NULL,

    Policy_Status ENUM(
        'Active',
        'Expired',
        'Cancelled',
        'Suspended'
    )
        DEFAULT 'Active',


    -- ======================================================
    -- Coverage and Financial Information
    -- ======================================================

    Total_Coverage_Amount DECIMAL(12,2)
        NULL,

    Used_Coverage_Amount DECIMAL(12,2)
        NOT NULL DEFAULT 0.00,

    Remaining_Coverage_Amount DECIMAL(12,2)
        NULL,

    Co_Payment_Percentage DECIMAL(5,2)
        NOT NULL DEFAULT 0.00,

    Deductible_Amount DECIMAL(12,2)
        NOT NULL DEFAULT 0.00,


    -- ======================================================
    -- Claim Information
    -- ======================================================

    Claim_Required BOOLEAN
        NOT NULL DEFAULT FALSE,

    Claim_Number VARCHAR(100)
        NULL,

    Claim_Status ENUM(
        'Not Required',
        'Not Initiated',
        'Submitted',
        'Under Review',
        'Approved',
        'Partially Approved',
        'Rejected',
        'Settled'
    )
        DEFAULT 'Not Required',

    Claim_Submission_Date DATE
        NULL,

    Claim_Settlement_Date DATE
        NULL,

    Claim_Amount DECIMAL(12,2)
        NULL,

    Approved_Claim_Amount DECIMAL(12,2)
        NULL,

    Rejection_Reason TEXT
        NULL,


    -- ======================================================
    -- Nominee and Contact Details
    -- ======================================================

    Nominee_Name VARCHAR(150)
        NULL,

    Nominee_Relationship VARCHAR(50)
        NULL,

    TPA_Name VARCHAR(150)
        NULL,

    TPA_Contact_Number VARCHAR(20)
        NULL,


    -- ======================================================
    -- Dataset Tracking
    -- ======================================================

    Data_Source ENUM(
        'MIMIC-IV',
        'Synthetic',
        'Hospital_Records',
        'Hybrid Dataset'
    )
        NOT NULL DEFAULT 'Synthetic',


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

    CONSTRAINT chk_pi_policy_dates
        CHECK (
            Policy_End_Date >= Policy_Start_Date
        ),

    CONSTRAINT chk_pi_total_coverage
        CHECK (
            Total_Coverage_Amount IS NULL
            OR Total_Coverage_Amount >= 0
        ),

    CONSTRAINT chk_pi_used_coverage
        CHECK (
            Used_Coverage_Amount >= 0
        ),

    CONSTRAINT chk_pi_remaining_coverage
        CHECK (
            Remaining_Coverage_Amount IS NULL
            OR Remaining_Coverage_Amount >= 0
        ),

    CONSTRAINT chk_pi_copayment
        CHECK (
            Co_Payment_Percentage BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_pi_deductible
        CHECK (
            Deductible_Amount >= 0
        ),

    CONSTRAINT chk_pi_claim_amount
        CHECK (
            Claim_Amount IS NULL
            OR Claim_Amount >= 0
        ),

    CONSTRAINT chk_pi_approved_claim
        CHECK (
            Approved_Claim_Amount IS NULL
            OR Approved_Claim_Amount >= 0
        ),

    CONSTRAINT chk_pi_claim_dates
        CHECK (
            Claim_Settlement_Date IS NULL
            OR Claim_Submission_Date IS NULL
            OR Claim_Settlement_Date >= Claim_Submission_Date
        ),


    -- ======================================================
    -- Foreign Key Constraints
    -- ======================================================

    CONSTRAINT fk_pi_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_pi_provider
        FOREIGN KEY (Insurance_ID)
        REFERENCES Insurance_Providers(Insurance_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,


    -- ======================================================
    -- Duplicate Policy Protection
    -- ======================================================

    CONSTRAINT uk_pi_policy_number
        UNIQUE (
            Insurance_ID,
            Policy_Number
        )

);


-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_pi_patient
    ON Patient_Insurance_Map(Patient_ID);

CREATE INDEX idx_pi_insurance_provider
    ON Patient_Insurance_Map(Insurance_ID);

CREATE INDEX idx_pi_policy_number
    ON Patient_Insurance_Map(Policy_Number);

CREATE INDEX idx_pi_policy_status
    ON Patient_Insurance_Map(Policy_Status);

CREATE INDEX idx_pi_policy_end_date
    ON Patient_Insurance_Map(Policy_End_Date);

CREATE INDEX idx_pi_claim_status
    ON Patient_Insurance_Map(Claim_Status);

CREATE INDEX idx_pi_data_source
    ON Patient_Insurance_Map(Data_Source);


-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Patient_Insurance_Map;