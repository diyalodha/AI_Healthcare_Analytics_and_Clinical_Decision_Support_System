/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 45_Create_Doctor_Schedules_Table.sql

Purpose : Create Doctor Availability Schedule Table

Version : 2.1

Author  : Diya Lodha & Team
===========================================================
*/


USE healthcare_ai_db;



DROP TABLE IF EXISTS Doctor_Schedules;



CREATE TABLE Doctor_Schedules (


    -- ======================================================
    -- Primary Key
    -- ======================================================

    Schedule_ID CHAR(36)
        NOT NULL PRIMARY KEY DEFAULT (UUID()),



    -- ======================================================
    -- Foreign Keys
    -- ======================================================

    Doctor_ID CHAR(36)
        NOT NULL,


    Department_ID CHAR(36),



    -- ======================================================
    -- Schedule Details
    -- ======================================================

    Available_Date DATE
        NOT NULL,


    Day_Of_Week ENUM(

        'Monday',

        'Tuesday',

        'Wednesday',

        'Thursday',

        'Friday',

        'Saturday',

        'Sunday'

    ),


    Start_Time TIME
        NOT NULL,


    End_Time TIME
        NOT NULL,



    Consultation_Type ENUM(

        'OPD',

        'Emergency',

        'Telemedicine',

        'Surgery'

    )
    DEFAULT 'OPD',



    Max_Patients INT
        DEFAULT 20,


    Current_Booking_Count INT
        DEFAULT 0,



    Schedule_Status ENUM(

        'Available',

        'Unavailable',

        'Leave'

    )
    DEFAULT 'Available',



    Notes TEXT,



    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,


    Updated_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,



    CONSTRAINT FK_Schedule_Doctor

        FOREIGN KEY(Doctor_ID)

        REFERENCES Doctors(Doctor_ID)

        ON UPDATE CASCADE

        ON DELETE CASCADE,



    CONSTRAINT FK_Schedule_Department

        FOREIGN KEY(Department_ID)

        REFERENCES Departments(Department_ID)

        ON UPDATE CASCADE

        ON DELETE SET NULL,



    CONSTRAINT UK_Doctor_Schedule

        UNIQUE(
            Doctor_ID,
            Available_Date,
            Start_Time,
            End_Time
        )


);



CREATE INDEX IDX_Schedule_Doctor

ON Doctor_Schedules(Doctor_ID);



CREATE INDEX IDX_Schedule_Date

ON Doctor_Schedules(Available_Date);



CREATE INDEX IDX_Schedule_Status

ON Doctor_Schedules(Schedule_Status);



SHOW TABLES;