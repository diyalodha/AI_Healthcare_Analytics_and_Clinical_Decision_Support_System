/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 13_Create_Lab_Results_Table.sql

Purpose : Create Lab Results Transaction Table

Description :
Stores laboratory investigation results for patients.
Supports hospital workflow, AI prediction,
clinical analytics and explainable AI.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Lab_Results;

-- ===========================================================
-- Create Lab Results Table
-- ===========================================================

CREATE TABLE Lab_Results (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Lab_Result_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),

    -- =======================================================
    -- Foreign Keys
    -- =======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Lab_Test_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36),

    Appointment_ID CHAR(36),

    Admission_ID CHAR(36),

    Diagnosis_ID CHAR(36),

    -- =======================================================
    -- Lab Order Information
    -- =======================================================

    Lab_Order_Number VARCHAR(30)
        UNIQUE,

    Lab_Order_ID CHAR(36),

    -- =======================================================
    -- Test Information
    -- =======================================================

    Test_Date DATETIME
        NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    Sample_Type VARCHAR(100),

    Sample_Collected_Date DATETIME,

    Result_Date DATETIME,

    Result_Category ENUM(
        'Hematology',
        'Biochemistry',
        'Microbiology',
        'Pathology',
        'Imaging',
        'Other'
    )
    DEFAULT 'Other',

    -- =======================================================
    -- Result Values
    -- =======================================================

    Result_Value VARCHAR(255),

    Numeric_Result_Value DECIMAL(10,2),

    Unit VARCHAR(50),

    Reference_Min_Value DECIMAL(10,2),

    Reference_Max_Value DECIMAL(10,2),

    -- =======================================================
    -- Clinical Interpretation
    -- =======================================================

    Result_Status ENUM(
        'Normal',
        'Abnormal',
        'Critical',
        'Pending'
    )
    DEFAULT 'Pending',

    Abnormal_Flag BOOLEAN
        DEFAULT FALSE,

    Severity_Score INT
        DEFAULT 0,

    Clinical_Interpretation TEXT,

    Doctor_Remarks TEXT,

    Technician_Name VARCHAR(100),

    Machine_Name VARCHAR(100),

    Verified_By VARCHAR(100),

    Verification_Status ENUM(
        'Pending',
        'Verified',
        'Rejected'
    )
    DEFAULT 'Pending',

    -- =======================================================
    -- AI Analytics
    -- =======================================================

    AI_Analyzed BOOLEAN
        DEFAULT FALSE,

    AI_Risk_Category ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
        DEFAULT 'Low',

    AI_Confidence_Score DECIMAL(5,2),

    Used_For_Model_Training BOOLEAN
        DEFAULT FALSE,

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

    CONSTRAINT fk_lab_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_lab_test
        FOREIGN KEY (Lab_Test_ID)
        REFERENCES Lab_Tests(Lab_Test_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_lab_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_lab_appointment
        FOREIGN KEY (Appointment_ID)
        REFERENCES Appointments(Appointment_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_lab_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_lab_diagnosis
        FOREIGN KEY (Diagnosis_ID)
        REFERENCES Diagnoses(Diagnosis_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    -- =======================================================
    -- Check Constraints
    -- =======================================================

    CONSTRAINT chk_lab_severity
        CHECK (
            Severity_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_ai_confidence
        CHECK (
            AI_Confidence_Score IS NULL
            OR AI_Confidence_Score BETWEEN 0 AND 100
        )

);

-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_lab_patient
ON Lab_Results(Patient_ID);

CREATE INDEX idx_lab_test
ON Lab_Results(Lab_Test_ID);

CREATE INDEX idx_lab_doctor
ON Lab_Results(Doctor_ID);

CREATE INDEX idx_lab_appointment
ON Lab_Results(Appointment_ID);

CREATE INDEX idx_lab_admission
ON Lab_Results(Admission_ID);

CREATE INDEX idx_lab_diagnosis
ON Lab_Results(Diagnosis_ID);

CREATE INDEX idx_lab_date
ON Lab_Results(Test_Date);

CREATE INDEX idx_lab_status
ON Lab_Results(Result_Status);

CREATE INDEX idx_lab_category
ON Lab_Results(Result_Category);

CREATE INDEX idx_lab_ai
ON Lab_Results(AI_Analyzed);

CREATE INDEX idx_lab_risk
ON Lab_Results(AI_Risk_Category);

CREATE INDEX idx_lab_source
ON Lab_Results(Data_Source);

-- ===========================================================
-- Verification
-- ===========================================================

SHOW TABLES;

DESCRIBE Lab_Results;/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 13_Create_Lab_Results_Table.sql

Purpose : Create Lab Results Transaction Table

Description :
Stores laboratory investigation results for patients.
Supports hospital workflow, AI prediction,
clinical analytics and explainable AI.

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

DROP TABLE IF EXISTS Lab_Results;

-- ===========================================================
-- Create Lab Results Table
-- ===========================================================

CREATE TABLE Lab_Results (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Lab_Result_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),

    -- =======================================================
    -- Foreign Keys
    -- =======================================================

    Patient_ID CHAR(36)
        NOT NULL,

    Lab_Test_ID CHAR(36)
        NOT NULL,

    Doctor_ID CHAR(36),

    Appointment_ID CHAR(36),

    Admission_ID CHAR(36),

    Diagnosis_ID CHAR(36),

    -- =======================================================
    -- Lab Order Information
    -- =======================================================

    Lab_Order_Number VARCHAR(30)
        UNIQUE,

    Lab_Order_ID CHAR(36),

    -- =======================================================
    -- Test Information
    -- =======================================================

    Test_Date DATETIME
        NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    Sample_Type VARCHAR(100),

    Sample_Collected_Date DATETIME,

    Result_Date DATETIME,

    Result_Category ENUM(
        'Hematology',
        'Biochemistry',
        'Microbiology',
        'Pathology',
        'Imaging',
        'Other'
    )
    DEFAULT 'Other',

    -- =======================================================
    -- Result Values
    -- =======================================================

    Result_Value VARCHAR(255),

    Numeric_Result_Value DECIMAL(10,2),

    Unit VARCHAR(50),

    Reference_Min_Value DECIMAL(10,2),

    Reference_Max_Value DECIMAL(10,2),

    -- =======================================================
    -- Clinical Interpretation
    -- =======================================================

    Result_Status ENUM(
        'Normal',
        'Abnormal',
        'Critical',
        'Pending'
    )
    DEFAULT 'Pending',

    Abnormal_Flag BOOLEAN
        DEFAULT FALSE,

    Severity_Score INT
        DEFAULT 0,

    Clinical_Interpretation TEXT,

    Doctor_Remarks TEXT,

    Technician_Name VARCHAR(100),

    Machine_Name VARCHAR(100),

    Verified_By VARCHAR(100),

    Verification_Status ENUM(
        'Pending',
        'Verified',
        'Rejected'
    )
    DEFAULT 'Pending',

    -- =======================================================
    -- AI Analytics
    -- =======================================================

    AI_Analyzed BOOLEAN
        DEFAULT FALSE,

    AI_Risk_Category ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    )
        DEFAULT 'Low',

    AI_Confidence_Score DECIMAL(5,2),

    Used_For_Model_Training BOOLEAN
        DEFAULT FALSE,

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

    CONSTRAINT fk_lab_patient
        FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_lab_test
        FOREIGN KEY (Lab_Test_ID)
        REFERENCES Lab_Tests(Lab_Test_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_lab_doctor
        FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_lab_appointment
        FOREIGN KEY (Appointment_ID)
        REFERENCES Appointments(Appointment_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_lab_admission
        FOREIGN KEY (Admission_ID)
        REFERENCES Admissions(Admission_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_lab_diagnosis
        FOREIGN KEY (Diagnosis_ID)
        REFERENCES Diagnoses(Diagnosis_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    -- =======================================================
    -- Check Constraints
    -- =======================================================

    CONSTRAINT chk_lab_severity
        CHECK (
            Severity_Score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_ai_confidence
        CHECK (
            AI_Confidence_Score IS NULL
            OR AI_Confidence_Score BETWEEN 0 AND 100
        )

);

-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_lab_patient
ON Lab_Results(Patient_ID);

CREATE INDEX idx_lab_test
ON Lab_Results(Lab_Test_ID);

CREATE INDEX idx_lab_doctor
ON Lab_Results(Doctor_ID);

CREATE INDEX idx_lab_appointment
ON Lab_Results(Appointment_ID);

CREATE INDEX idx_lab_admission
ON Lab_Results(Admission_ID);

CREATE INDEX idx_lab_diagnosis
ON Lab_Results(Diagnosis_ID);

CREATE INDEX idx_lab_date
ON Lab_Results(Test_Date);

CREATE INDEX idx_lab_status
ON Lab_Results(Result_Status);

CREATE INDEX idx_lab_category
ON Lab_Results(Result_Category);

CREATE INDEX idx_lab_ai
ON Lab_Results(AI_Analyzed);

CREATE INDEX idx_lab_risk
ON Lab_Results(AI_Risk_Category);

CREATE INDEX idx_lab_source
ON Lab_Results(Data_Source);

-- ===========================================================
-- Verification
-- ===========================================================

SHOW TABLES;

DESCRIBE Lab_Results;