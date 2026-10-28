/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 15_Create_Payments_Table.sql

Purpose : Create Patient Payment Transaction Table

Description :
Stores all hospital payment transactions,
insurance settlements, refunds,
financial verification and AI fraud analysis.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Payments;

-- ===========================================================
-- Create Payments Table
-- ===========================================================

CREATE TABLE Payments (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Payment_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),

    -- =======================================================
    -- Foreign Keys
    -- =======================================================

    Bill_ID CHAR(36)
        NOT NULL,

    Patient_ID CHAR(36)
        NOT NULL,

    Insurance_ID CHAR(36),

    -- =======================================================
    -- Payment Information
    -- =======================================================

    Payment_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Receipt_Number VARCHAR(30)
        UNIQUE,

    Payment_Date DATETIME
        DEFAULT CURRENT_TIMESTAMP,

    Payment_Amount DECIMAL(12,2)
        NOT NULL,

    Payment_Method ENUM(
        'Cash',
        'Credit Card',
        'Debit Card',
        'UPI',
        'Insurance',
        'Bank Transfer',
        'Net Banking',
        'Cheque'
    )
        NOT NULL,

    Payment_Gateway VARCHAR(100),

    Transaction_ID VARCHAR(150)
        UNIQUE,

    Reference_Number VARCHAR(100),

    -- =======================================================
    -- Payment Status
    -- =======================================================

    Payment_Status ENUM(
        'Pending',
        'Successful',
        'Failed',
        'Refunded',
        'Cancelled'
    )
    DEFAULT 'Pending',

    Verification_Status ENUM(
        'Pending',
        'Verified',
        'Rejected'
    )
    DEFAULT 'Pending',

    Received_By VARCHAR(100),

    Verified_By VARCHAR(100),

    -- =======================================================
    -- Payment Distribution
    -- =======================================================

    Insurance_Paid_Amount DECIMAL(12,2)
        DEFAULT 0,

    Patient_Paid_Amount DECIMAL(12,2)
        DEFAULT 0,

    Refund_Amount DECIMAL(12,2)
        DEFAULT 0,

    Refund_Reason TEXT,

    -- =======================================================
    -- Insurance Claim Tracking
    -- =======================================================

    Insurance_Claim_ID VARCHAR(100),

    Claim_Status ENUM(
        'Not Submitted',
        'Submitted',
        'Approved',
        'Rejected',
        'Settled'
    )
    DEFAULT 'Not Submitted',

    -- =======================================================
    -- AI Financial Analytics
    -- =======================================================

    Fraud_Check_Status BOOLEAN
        DEFAULT FALSE,

    Fraud_Risk_Score DECIMAL(5,2)
        DEFAULT 0,

    AI_Verification_Result ENUM(
        'Not Checked',
        'Valid',
        'Suspicious',
        'Fraud'
    )
    DEFAULT 'Not Checked',

    -- =======================================================
    -- Dataset Tracking
    -- =======================================================

    Data_Source ENUM(
        'Synthetic',
        'MIMIC-IV',
        'Hospital_Records'
    )
    DEFAULT 'Synthetic',

    -- =======================================================
    -- System Information
    -- =======================================================

    Is_Active BOOLEAN
        DEFAULT TRUE,

    Is_Deleted BOOLEAN
        DEFAULT FALSE,

    Record_Version INT
        DEFAULT 1,

    -- =======================================================
    -- Audit Information
    -- =======================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    -- =======================================================
    -- Foreign Keys
    -- =======================================================

    CONSTRAINT fk_payment_bill
        FOREIGN KEY (Bill_ID)
        REFERENCES Billing(Bill_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_payment_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_payment_insurance
        FOREIGN KEY (Insurance_ID)
        REFERENCES Insurance_Providers(Insurance_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    -- =======================================================
    -- Check Constraints
    -- =======================================================

    CONSTRAINT chk_payment_amount
        CHECK (
            Payment_Amount >= 0
        ),

    CONSTRAINT chk_patient_paid
        CHECK (
            Patient_Paid_Amount >= 0
        ),

    CONSTRAINT chk_insurance_paid
        CHECK (
            Insurance_Paid_Amount >= 0
        ),

    CONSTRAINT chk_refund_amount
        CHECK (
            Refund_Amount >= 0
        ),

    CONSTRAINT chk_fraud_score
        CHECK (
            Fraud_Risk_Score BETWEEN 0 AND 100
        )

);

-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_payment_number
ON Payments(Payment_Number);

CREATE INDEX idx_receipt_number
ON Payments(Receipt_Number);

CREATE INDEX idx_payment_bill
ON Payments(Bill_ID);

CREATE INDEX idx_payment_patient
ON Payments(Patient_ID);

CREATE INDEX idx_payment_insurance
ON Payments(Insurance_ID);

CREATE INDEX idx_payment_date
ON Payments(Payment_Date);

CREATE INDEX idx_payment_status
ON Payments(Payment_Status);

CREATE INDEX idx_claim_status
ON Payments(Claim_Status);

CREATE INDEX idx_verification_status
ON Payments(Verification_Status);

CREATE INDEX idx_fraud_status
ON Payments(Fraud_Check_Status);

CREATE INDEX idx_data_source
ON Payments(Data_Source);

-- ===========================================================
-- Verification
-- ===========================================================

SHOW TABLES;

DESCRIBE Payments;