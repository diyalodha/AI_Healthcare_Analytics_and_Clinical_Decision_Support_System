/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 32_Create_Beds_Table.sql

Purpose : Create Hospital Beds Management Table

Description:
Stores hospital bed availability, allocation,
occupancy history, and patient assignment details.

Version : 2.1

Author : Diya Lodha & Team
===========================================================
*/


USE healthcare_ai_db;


DROP TABLE IF EXISTS Beds;



CREATE TABLE Beds (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Bed_ID CHAR(36) NOT NULL PRIMARY KEY,


    -- ======================================================
    -- Foreign Keys
    -- ======================================================

    Room_ID CHAR(36) NOT NULL,

    Patient_ID CHAR(36),



    -- ======================================================
    -- Bed Information
    -- ======================================================

    Bed_Number VARCHAR(20) NOT NULL,


    Bed_Type ENUM(

        'Standard',

        'ICU',

        'Electric',

        'Ventilator',

        'Pediatric',

        'Maternity'

    ) NOT NULL DEFAULT 'Standard',



    Bed_Status ENUM(

        'Available',

        'Occupied',

        'Reserved',

        'Cleaning',

        'Maintenance'

    ) DEFAULT 'Available',



    Occupied_From DATETIME,


    Occupied_To DATETIME,


    Last_Cleaned_Date DATETIME,


    Is_Isolation_Bed BOOLEAN DEFAULT FALSE,


    Ventilator_Available BOOLEAN DEFAULT FALSE,


    Notes TEXT,



    -- ======================================================
    -- Audit Information
    -- ======================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),


    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    ON UPDATE CURRENT_TIMESTAMP,



    -- ======================================================
    -- Constraints
    -- ======================================================


    CONSTRAINT FK_Bed_Room

    FOREIGN KEY(Room_ID)

    REFERENCES Hospital_Rooms(Room_ID)

    ON UPDATE CASCADE

    ON DELETE CASCADE,



    CONSTRAINT FK_Bed_Patient

    FOREIGN KEY(Patient_ID)

    REFERENCES Patients(Patient_ID)

    ON UPDATE CASCADE

    ON DELETE SET NULL,



    CONSTRAINT UK_Room_Bed

    UNIQUE(Room_ID,Bed_Number)


);



-- ==========================================================
-- Indexes
-- ==========================================================


CREATE INDEX IDX_Bed_Room

ON Beds(Room_ID);



CREATE INDEX IDX_Bed_Patient

ON Beds(Patient_ID);



CREATE INDEX IDX_Bed_Status

ON Beds(Bed_Status);



CREATE INDEX IDX_Bed_Type

ON Beds(Bed_Type);