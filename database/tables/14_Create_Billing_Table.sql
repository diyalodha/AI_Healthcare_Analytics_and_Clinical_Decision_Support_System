/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 14_Create_Billing_Table.sql

Purpose : Create Hospital Billing Transaction Table

Description :
Stores hospital billing, insurance claims,
payment tracking, AI financial analytics,
fraud detection and healthcare cost analysis.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Billing;

-- ===========================================================
-- Create Billing Table
-- ===========================================================

CREATE TABLE Billing (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Bill_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),

    -- =======================================================
    -- Foreign Keys
    -- =======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Admission_ID CHAR(36),

    Appointment_ID CHAR(36),

    Diagnosis_ID CHAR(36),

    Prescription_ID CHAR(36),

    Insurance_ID CHAR(36),

    -- =======================================================
    -- Billing Information
    -- =======================================================

    Billing_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Invoice_Number VARCHAR(100)
        UNIQUE,

    Bill_Date DATETIME
        DEFAULT CURRENT_TIMESTAMP,

    Due_Date DATE,

    Paid_Date DATE,

    Billing_Type ENUM(
        'Admission',
        'Consultation',
        'Lab_Test',
        'Medication',
        'Surgery',
        'Emergency',
        'Other'
    )
    DEFAULT 'Other',

    Description TEXT,

    -- =======================================================
    -- Individual Charges
    -- =======================================================

    Consultation_Charges DECIMAL(12,2)
        DEFAULT 0,

    Lab_Charges DECIMAL(12,2)
        DEFAULT 0,

    Medication_Charges DECIMAL(12,2)
        DEFAULT 0,

    Room_Charges DECIMAL(12,2)
        DEFAULT 0,

    Procedure_Charges DECIMAL(12,2)
        DEFAULT 0,

    Other_Charges DECIMAL(12,2)
        DEFAULT 0,

    -- =======================================================
    -- Financial Summary
    -- =======================================================

    Total_Amount DECIMAL(12,2)
        NOT NULL,

    Insurance_Coverage DECIMAL(12,2)
        DEFAULT 0,

    Discount_Amount DECIMAL(12,2)
        DEFAULT 0,

    Tax_Amount DECIMAL(12,2)
        DEFAULT 0,

    Final_Amount DECIMAL(12,2)
        NOT NULL,

    Outstanding_Amount DECIMAL(12,2)
        DEFAULT 0,

    -- =======================================================
    -- Payment Information
    -- =======================================================

    Payment_Method ENUM(
        'Cash',
        'Card',
        'UPI',
        'Net Banking',
        'Insurance',
        'Cheque'
    ),

    Payment_Status ENUM(
        'Pending',
        'Partially Paid',
        'Paid',
        'Cancelled',
        'Refunded'
    )
    DEFAULT 'Pending',

    Billing_Status ENUM(
        'Generated',
        'Submitted',
        'Approved',
        'Closed'
    )
    DEFAULT 'Generated',

    Insurance_Claim_Number VARCHAR(50),

    -- =======================================================
    -- AI Financial Analytics
    -- =======================================================

    Cost_Category ENUM(
        'Routine',
        'Emergency',
        'Chronic Disease',
        'Surgery',
        'Preventive Care'
    )
    DEFAULT 'Routine',

    AI_Cost_Analysis_Status BOOLEAN
        DEFAULT FALSE,

    Predicted_Future_Cost DECIMAL(12,2),

    Fraud_Risk_Flag BOOLEAN
        DEFAULT FALSE,

    AI_Fraud_Risk_Score DECIMAL(5,2),

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

    CONSTRAINT fk_billing_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_billing_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_billing_appointment
        FOREIGN KEY (Appointment_ID)
        REFERENCES Appointments(Appointment_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_billing_diagnosis
        FOREIGN KEY (Diagnosis_ID)
        REFERENCES Diagnoses(Diagnosis_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_billing_prescription
        FOREIGN KEY (Prescription_ID)
        REFERENCES Prescriptions(Prescription_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_billing_insurance
        FOREIGN KEY (Insurance_ID)
        REFERENCES Insurance_Providers(Insurance_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    -- =======================================================
    -- Check Constraints
    -- =======================================================

    CONSTRAINT chk_total_amount
        CHECK (Total_Amount >= 0),

    CONSTRAINT chk_final_amount
        CHECK (Final_Amount >= 0),

    CONSTRAINT chk_outstanding_amount
        CHECK (Outstanding_Amount >= 0),

    CONSTRAINT chk_discount_amount
        CHECK (Discount_Amount >= 0),

    CONSTRAINT chk_tax_amount
        CHECK (Tax_Amount >= 0),

    CONSTRAINT chk_insurance_coverage
        CHECK (Insurance_Coverage >= 0),

    CONSTRAINT chk_ai_fraud_score
        CHECK (
            AI_Fraud_Risk_Score IS NULL
            OR AI_Fraud_Risk_Score BETWEEN 0 AND 100
        )

);

-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_billing_number
ON Billing(Billing_Number);

CREATE INDEX idx_billing_patient
ON Billing(Patient_ID);

CREATE INDEX idx_billing_admission
ON Billing(Admission_ID);

CREATE INDEX idx_billing_appointment
ON Billing(Appointment_ID);

CREATE INDEX idx_billing_diagnosis
ON Billing(Diagnosis_ID);

CREATE INDEX idx_billing_prescription
ON Billing(Prescription_ID);

CREATE INDEX idx_billing_insurance
ON Billing(Insurance_ID);

CREATE INDEX idx_billing_date
ON Billing(Bill_Date);

CREATE INDEX idx_payment_status
ON Billing(Payment_Status);

CREATE INDEX idx_billing_status
ON Billing(Billing_Status);

CREATE INDEX idx_fraud_flag
ON Billing(Fraud_Risk_Flag);

CREATE INDEX idx_cost_category
ON Billing(Cost_Category);

-- ===========================================================
-- Verification
-- ===========================================================

SHOW TABLES;

DESCRIBE Billing;