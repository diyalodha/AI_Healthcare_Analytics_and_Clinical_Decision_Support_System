/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 23_Create_Roles_Table.sql

Purpose : Create User Roles Management Table

Version : 2.2

Author  : Diya Lodha & Team
===========================================================
*/


USE healthcare_ai_db;



DROP TABLE IF EXISTS Roles;



CREATE TABLE Roles (


    -- ======================================================
    -- Primary Key
    -- ======================================================

    Role_ID CHAR(36)
        NOT NULL PRIMARY KEY DEFAULT (UUID()),



    -- ======================================================
    -- Role Information
    -- ======================================================


    Role_Name VARCHAR(100)
        NOT NULL UNIQUE,


    Role_Description TEXT,



    -- ======================================================
    -- Permission Management
    -- ======================================================


    Can_View_Patient_Data BOOLEAN
        DEFAULT FALSE,


    Can_Modify_Patient_Data BOOLEAN
        DEFAULT FALSE,


    Can_View_AI_Predictions BOOLEAN
        DEFAULT FALSE,


    Can_Approve_Recommendations BOOLEAN
        DEFAULT FALSE,


    Can_Manage_Users BOOLEAN
        DEFAULT FALSE,


    Can_View_Financial_Data BOOLEAN
        DEFAULT FALSE,



    -- ======================================================
    -- Status
    -- ======================================================


    Role_Status ENUM(

        'Active',

        'Inactive'

    )
    DEFAULT 'Active',



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



-- ======================================================
-- Indexes
-- ======================================================


CREATE INDEX IDX_Role_Name

ON Roles(Role_Name);



CREATE INDEX IDX_Role_Status

ON Roles(Role_Status);



SHOW TABLES;

DESCRIBE Roles;