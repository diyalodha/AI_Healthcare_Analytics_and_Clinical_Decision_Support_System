
/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 70_Create_Patient_Care_Followup_Map.sql

Purpose : Create Patient Care Follow-Up Mapping Table

Description :
Maps patients with their follow-up care activities,
appointments, doctors, diagnoses, prescriptions and
AI-supported follow-up recommendations.

Supports:
- Patient follow-up history
- Post-treatment monitoring
- Chronic disease follow-up
- Appointment tracking
- Doctor follow-up
- AI-supported care planning
- Follow-up outcome analysis
- Dataset traceability

Version : 3.1

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- =========================================================
-- Remove Existing Table
-- =========================================================

DROP TABLE IF EXISTS Patient_Care_Followup_Map;


-- =========================================================
-- Create Patient Care Follow-Up Mapping Table
-- =========================================================

CREATE TABLE Patient_Care_Followup_Map (

    -- =====================================================
    -- Primary Key
    -- =====================================================

    Care_Followup_Map_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =====================================================
    -- Foreign Keys
    -- =====================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36),

    Diagnosis_ID CHAR(36),

    Disease_ID CHAR(36),

    Appointment_ID CHAR(36),

    Admission_ID CHAR(36),

    Prescription_ID CHAR(36),

    Prediction_Session_ID CHAR(36),


    -- =====================================================
    -- Follow-Up Identification
    -- =====================================================

    Followup_Number VARCHAR(30)
        NOT NULL
        UNIQUE,

    Followup_Date DATETIME
        NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    Planned_Followup_Date DATE,

    Followup_Type ENUM(
        'Routine',
        'Post-Treatment',
        'Post-Surgery',
        'Chronic Disease',
        'Medication Review',
        'Diagnostic Review',
        'Emergency Follow-Up',
        'Discharge Follow-Up',
        'Preventive Care',
        'Other'
    )
        DEFAULT 'Routine',


    -- =====================================================
    -- Care Information
    -- =====================================================

    Care_Purpose TEXT,

    Clinical_Condition TEXT,

    Symptoms_Status ENUM(
        'Improved',
        'Stable',
        'Worsened',
        'Resolved',
        'New Symptoms',
        'Unknown'
    )
        DEFAULT 'Unknown',

    Treatment_Response ENUM(
        'Good',
        'Partial',
        'Poor',
        'No Response',
        'Not Applicable'
    )
        DEFAULT 'Not Applicable',

    Medication_Compliance ENUM(
        'Good',
        'Partial',
        'Poor',
        'Unknown',
        'Not Applicable'
    )
        DEFAULT 'Unknown',

    Followup_Notes TEXT,

    Doctor_Recommendations TEXT,

    Patient_Instructions TEXT,


    -- =====================================================
    -- Follow-Up Outcome
    -- =====================================================

    Followup_Status ENUM(
        'Scheduled',
        'Completed',
        'Missed',
        'Cancelled',
        'Rescheduled',
        'Pending'
    )
        DEFAULT 'Scheduled',

    Outcome TEXT,

    Next_Followup_Date DATE,


    -- =====================================================
    -- AI Support
    -- =====================================================

    AI_Followup_Recommended BOOLEAN
        DEFAULT FALSE,

    AI_Risk_Level ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
        DEFAULT 'Low',

    AI_Confidence_Score DECIMAL(5,2),

    AI_Recommendation TEXT,

    Readmission_Risk DECIMAL(5,2),


    -- =====================================================
    -- Doctor Review
    -- =====================================================

    Doctor_Reviewed BOOLEAN
        DEFAULT FALSE,

    Doctor_Feedback TEXT,

    Review_Date DATETIME,


    -- =====================================================
    -- Dataset Tracking
    -- =====================================================

    Data_Source ENUM(
        'MIMIC-IV',
        'Synthetic',
        'Hospital_Records',
        'Hybrid Dataset'
    )
        DEFAULT 'Synthetic',

    Dataset_Version VARCHAR(30),


    -- =====================================================
    -- System Status
    -- =====================================================

    Is_Active BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    Is_Deleted BOOLEAN
        NOT NULL
        DEFAULT FALSE,

    Record_Version INT
        NOT NULL
        DEFAULT 1,


    -- =====================================================
    -- Audit Information
    -- =====================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Created_At TIMESTAMP
        NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,


    -- =====================================================
    -- Foreign Key Constraints
    -- =====================================================

    CONSTRAINT fk_pcfm_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,


    CONSTRAINT fk_pcfm_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_pcfm_diagnosis
        FOREIGN KEY (Diagnosis_ID)
        REFERENCES Diagnoses(Diagnosis_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_pcfm_disease
        FOREIGN KEY (Disease_ID)
        REFERENCES Diseases(Disease_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_pcfm_appointment
        FOREIGN KEY (Appointment_ID)
        REFERENCES Appointments(Appointment_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_pcfm_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_pcfm_prescription
        FOREIGN KEY (Prescription_ID)
        REFERENCES Prescriptions(Prescription_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    CONSTRAINT fk_pcfm_prediction_session
        FOREIGN KEY (Prediction_Session_ID)
        REFERENCES Prediction_Sessions(Prediction_Session_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,


    -- =====================================================
    -- Validation Constraints
    -- =====================================================

    CONSTRAINT chk_pcfm_ai_confidence
        CHECK (
            AI_Confidence_Score IS NULL
            OR AI_Confidence_Score BETWEEN 0 AND 100
        ),


    CONSTRAINT chk_pcfm_readmission_risk
        CHECK (
            Readmission_Risk IS NULL
            OR Readmission_Risk BETWEEN 0 AND 100
        ),


    CONSTRAINT chk_pcfm_record_version
        CHECK (
            Record_Version >= 1
        ),


    CONSTRAINT chk_pcfm_planned_followup
        CHECK (
            Planned_Followup_Date IS NULL
            OR Planned_Followup_Date >= DATE(Followup_Date)
        ),


    CONSTRAINT chk_pcfm_next_followup
        CHECK (
            Next_Followup_Date IS NULL
            OR Planned_Followup_Date IS NULL
            OR Next_Followup_Date >= Planned_Followup_Date
        ),


    CONSTRAINT chk_pcfm_review_date
        CHECK (
            Doctor_Reviewed = FALSE
            OR Review_Date IS NOT NULL
        )

);


-- =========================================================
-- Indexes
-- =========================================================

CREATE INDEX idx_pcfm_followup_number
ON Patient_Care_Followup_Map(Followup_Number);


CREATE INDEX idx_pcfm_patient
ON Patient_Care_Followup_Map(Patient_ID);


CREATE INDEX idx_pcfm_doctor
ON Patient_Care_Followup_Map(Doctor_ID);


CREATE INDEX idx_pcfm_diagnosis
ON Patient_Care_Followup_Map(Diagnosis_ID);


CREATE INDEX idx_pcfm_disease
ON Patient_Care_Followup_Map(Disease_ID);


CREATE INDEX idx_pcfm_appointment
ON Patient_Care_Followup_Map(Appointment_ID);


CREATE INDEX idx_pcfm_admission
ON Patient_Care_Followup_Map(Admission_ID);


CREATE INDEX idx_pcfm_prescription
ON Patient_Care_Followup_Map(Prescription_ID);


CREATE INDEX idx_pcfm_prediction_session
ON Patient_Care_Followup_Map(Prediction_Session_ID);


CREATE INDEX idx_pcfm_followup_date
ON Patient_Care_Followup_Map(Followup_Date);


CREATE INDEX idx_pcfm_planned_date
ON Patient_Care_Followup_Map(Planned_Followup_Date);


CREATE INDEX idx_pcfm_type
ON Patient_Care_Followup_Map(Followup_Type);


CREATE INDEX idx_pcfm_status
ON Patient_Care_Followup_Map(Followup_Status);


CREATE INDEX idx_pcfm_ai_risk
ON Patient_Care_Followup_Map(AI_Risk_Level);


CREATE INDEX idx_pcfm_ai_recommended
ON Patient_Care_Followup_Map(AI_Followup_Recommended);


CREATE INDEX idx_pcfm_source
ON Patient_Care_Followup_Map(Data_Source);


-- =========================================================
-- Verification
-- =========================================================

SHOW TABLES;

DESCRIBE Patient_Care_Followup_Map;


-- =========================================================
-- Foreign Key Verification
-- =========================================================

SELECT
    TABLE_NAME,
    CONSTRAINT_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'healthcare_ai_db'
  AND TABLE_NAME = 'Patient_Care_Followup_Map'
  AND REFERENCED_TABLE_NAME IS NOT NULL;


-- =========================================================
-- Index Verification
-- =========================================================

SHOW INDEX
FROM Patient_Care_Followup_Map;
