/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 08_Create_Insurance_Providers_Table.sql
Purpose : Create Insurance Providers Master Table
Version : 3.0
Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;


-- ===========================================================
-- Create Insurance Providers Master Table
-- ===========================================================

CREATE TABLE IF NOT EXISTS Insurance_Providers (

    -- =======================================================
    -- Primary Key
    -- =======================================================

    Insurance_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- =======================================================
    -- Provider Information
    -- =======================================================

    Provider_Code VARCHAR(20)
        NOT NULL
        UNIQUE,

    Provider_Name VARCHAR(150)
        NOT NULL
        UNIQUE,

    Insurance_Type ENUM(
        'Government',
        'Private',
        'Employer',
        'TPA'
    )
    NOT NULL,

    Coverage_Type ENUM(
        'Individual',
        'Family',
        'Corporate',
        'Senior Citizen'
    ),

    Contact_Number VARCHAR(20),

    Helpline_Number VARCHAR(20),

    Email VARCHAR(100),

    Claim_Email VARCHAR(100),

    Website VARCHAR(255),

    Claim_Website VARCHAR(255),

    GST_Number VARCHAR(20),

    IRDAI_Registration_No VARCHAR(50),

    Address VARCHAR(255),

    City VARCHAR(100),

    State VARCHAR(100),

    Country VARCHAR(100)
        DEFAULT 'India',

    Postal_Code VARCHAR(10),

    Cashless_Available BOOLEAN
        DEFAULT TRUE,

    Support_Hours VARCHAR(100)
        DEFAULT '24x7',


    -- =======================================================
    -- Status Information
    -- =======================================================

    Status ENUM(
        'Active',
        'Inactive'
    )
    DEFAULT 'Active',

    Is_Active BOOLEAN
        DEFAULT TRUE,

    Is_Deleted BOOLEAN
        DEFAULT FALSE,


    -- =======================================================
    -- System Information
    -- =======================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Record_Version INT
        DEFAULT 1,


    -- =======================================================
    -- Audit Information
    -- =======================================================

    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,


    -- =======================================================
    -- Validation
    -- =======================================================

    CONSTRAINT chk_provider_name
        CHECK (
            LENGTH(Provider_Name) > 2
        )

);


-- ===========================================================
-- Indexes
-- ===========================================================

CREATE INDEX idx_provider_code
ON Insurance_Providers(Provider_Code);

CREATE INDEX idx_provider_name
ON Insurance_Providers(Provider_Name);

CREATE INDEX idx_provider_type
ON Insurance_Providers(Insurance_Type);

CREATE INDEX idx_provider_city
ON Insurance_Providers(City);

CREATE INDEX idx_provider_state
ON Insurance_Providers(State);

CREATE INDEX idx_provider_status
ON Insurance_Providers(Status);


-- ===========================================================
-- Verification
-- ===========================================================

SHOW TABLES;

DESCRIBE Insurance_Providers;