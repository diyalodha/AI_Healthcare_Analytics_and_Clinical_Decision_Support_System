/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 42_Create_Notifications_Table.sql

Purpose : Create Notification Management Table

Description:
Stores system notifications, AI alerts, appointment
reminders, billing notifications, emergency alerts,
and communication history.

Version : 2.2

Author  : Diya Lodha & Team
===========================================================
*/


USE healthcare_ai_db;



-- ==========================================================
-- Remove Existing Table
-- ==========================================================

DROP TABLE IF EXISTS Notifications;



-- ==========================================================
-- Table : Notifications
-- ==========================================================

CREATE TABLE Notifications (


    -- ======================================================
    -- Primary Key
    -- ======================================================

    Notification_ID CHAR(36)
        NOT NULL PRIMARY KEY DEFAULT (UUID()),



    -- ======================================================
    -- User References
    -- ======================================================

    User_ID CHAR(36),

    Patient_ID CHAR(36),

    Doctor_ID CHAR(36),

    Related_Record_ID CHAR(36),



    -- ======================================================
    -- Notification Information
    -- ======================================================

    Notification_Title VARCHAR(200)
        NOT NULL,

    Notification_Message TEXT
        NOT NULL,

    Notification_Type ENUM(

        'Appointment',
        'Lab Result',
        'Prescription',
        'Emergency',
        'Billing',
        'AI Alert',
        'General',
        'System Update'

    )
    NOT NULL,



    Priority ENUM(

        'Low',
        'Medium',
        'High',
        'Critical'

    )
    DEFAULT 'Medium',



    Notification_Source ENUM(

        'Hospital System',
        'AI Engine',
        'Doctor',
        'Laboratory',
        'Billing',
        'Admin'

    )
    DEFAULT 'Hospital System',



    Delivery_Method ENUM(

        'SMS',
        'Email',
        'Push',
        'System',
        'WhatsApp'

    )
    DEFAULT 'System',



    Notification_Status ENUM(

        'Pending',
        'Sent',
        'Delivered',
        'Failed',
        'Read',
        'Expired'

    )
    DEFAULT 'Pending',



    Is_Read BOOLEAN
        DEFAULT FALSE,

    Read_Time DATETIME,

    Sent_Time DATETIME,

    Expiry_Time DATETIME,



    Retry_Count INT
        DEFAULT 0,



    Delivery_Status_Message VARCHAR(255),

    Read_By VARCHAR(100),

    Action_URL VARCHAR(500),



    -- ======================================================
    -- Dataset Tracking
    -- ======================================================

    Data_Source ENUM(

        'MIMIC-IV',
        'Synthetic',
        'Hospital_Records',
        'Hybrid Dataset'

    )
    DEFAULT 'Synthetic',



    -- ======================================================
    -- Audit Information
    -- ======================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,



    -- ======================================================
    -- Foreign Keys
    -- ======================================================

    CONSTRAINT FK_Notification_User

        FOREIGN KEY(User_ID)

        REFERENCES Users(User_ID)

        ON UPDATE CASCADE

        ON DELETE SET NULL,



    CONSTRAINT FK_Notification_Patient

        FOREIGN KEY(Patient_ID)

        REFERENCES Patients(Patient_ID)

        ON UPDATE CASCADE

        ON DELETE CASCADE,



    CONSTRAINT FK_Notification_Doctor

        FOREIGN KEY(Doctor_ID)

        REFERENCES Doctors(Doctor_ID)

        ON UPDATE CASCADE

        ON DELETE SET NULL

);



-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX IDX_Notification_User
ON Notifications(User_ID);



CREATE INDEX IDX_Notification_Patient
ON Notifications(Patient_ID);



CREATE INDEX IDX_Notification_Doctor
ON Notifications(Doctor_ID);



CREATE INDEX IDX_Notification_Type
ON Notifications(Notification_Type);



CREATE INDEX IDX_Notification_Status
ON Notifications(Notification_Status);



CREATE INDEX IDX_Notification_Priority
ON Notifications(Priority);



CREATE INDEX IDX_Notification_IsRead
ON Notifications(Is_Read);



CREATE INDEX IDX_Notification_SentTime
ON Notifications(Sent_Time);



SHOW TABLES;

DESCRIBE Notifications;