/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 43_Create_System_Settings_Table.sql

Purpose : Create System Configuration Settings Table

Description:
Stores application-wide configuration settings used
by the AI Healthcare Analytics & Clinical Decision
Support System including AI engine, security,
database, notification, and environment settings.

Version : 2.2

Author  : Diya Lodha & Team
===========================================================
*/


USE healthcare_ai_db;



-- ==========================================================
-- Remove Existing Table
-- ==========================================================

DROP TABLE IF EXISTS System_Settings;



-- ==========================================================
-- Table : System_Settings
-- ==========================================================

CREATE TABLE System_Settings (


    -- ======================================================
    -- Primary Key
    -- ======================================================

    Setting_ID CHAR(36)
        NOT NULL PRIMARY KEY DEFAULT (UUID()),



    -- ======================================================
    -- Setting Information
    -- ======================================================

    Setting_Key VARCHAR(150)
        NOT NULL UNIQUE,


    Setting_Value TEXT,


    Default_Value TEXT,


    Setting_Category VARCHAR(100),


    Setting_Group VARCHAR(100),



    Data_Type ENUM(

        'String',
        'Integer',
        'Decimal',
        'Boolean',
        'JSON'

    )
    DEFAULT 'String',



    Environment ENUM(

        'Development',
        'Testing',
        'Production'

    )
    DEFAULT 'Development',



    Description TEXT,



    Validation_Rule VARCHAR(255),



    Is_Editable BOOLEAN
        DEFAULT TRUE,



    Requires_Restart BOOLEAN
        DEFAULT FALSE,



    Setting_Status ENUM(

        'Active',
        'Inactive',
        'Deprecated'

    )
    DEFAULT 'Active',



    Last_Modified_By VARCHAR(100),



    -- ======================================================
    -- Dataset Tracking
    -- ======================================================

    Data_Source ENUM(

        'System Default',
        'Hospital Configuration',
        'Administrator',
        'Deployment Script'

    )
    DEFAULT 'System Default',



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

CREATE INDEX IDX_Settings_Key
ON System_Settings(Setting_Key);



CREATE INDEX IDX_Settings_Category
ON System_Settings(Setting_Category);



CREATE INDEX IDX_Settings_Group
ON System_Settings(Setting_Group);



CREATE INDEX IDX_Settings_Environment
ON System_Settings(Environment);



CREATE INDEX IDX_Settings_Status
ON System_Settings(Setting_Status);



CREATE INDEX IDX_Settings_Editable
ON System_Settings(Is_Editable);



SHOW TABLES;

DESCRIBE System_Settings;