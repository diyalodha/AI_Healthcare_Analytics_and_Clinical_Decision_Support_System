/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 39_Create_AI_Feedback_Table.sql

Purpose : Create AI Prediction Feedback Table

Description:
Stores doctor validation feedback on AI predictions
for model evaluation and continuous improvement.

Version : 2.1

Author : Diya Lodha & Team
===========================================================
*/


USE healthcare_ai_db;


DROP TABLE IF EXISTS AI_Feedback;



CREATE TABLE AI_Feedback (


    -- ======================================================
    -- Primary Key
    -- ======================================================

    AI_Feedback_ID CHAR(36) NOT NULL PRIMARY KEY,



    -- ======================================================
    -- Foreign Keys
    -- ======================================================


    Patient_ID CHAR(36),


    Doctor_ID CHAR(36),


    Diagnosis_ID CHAR(36),


    Prediction_Session_ID CHAR(36),



    -- ======================================================
    -- AI Prediction Details
    -- ======================================================


    AI_Model_Name VARCHAR(150) NOT NULL,


    Model_Version VARCHAR(50),



    Predicted_Disease VARCHAR(200),



    Prediction_Confidence DECIMAL(5,2),



    Predicted_Result TEXT,



    -- ======================================================
    -- Doctor Validation
    -- ======================================================


    Doctor_Final_Diagnosis VARCHAR(200),



    Prediction_Correct BOOLEAN,



    Feedback_Rating INT,



    Feedback_Category ENUM(

        'Accurate',

        'Partially Accurate',

        'Incorrect'

    ),



    Feedback_Comments TEXT,



    Retraining_Required BOOLEAN DEFAULT FALSE,



    Reviewed_On DATETIME,



    -- ======================================================
    -- Audit
    -- ======================================================


    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    ON UPDATE CURRENT_TIMESTAMP,



    -- ======================================================
    -- Foreign Keys
    -- ======================================================


    CONSTRAINT FK_AI_Feedback_Patient

    FOREIGN KEY(Patient_ID)

    REFERENCES Patients(Patient_ID)

    ON UPDATE CASCADE

    ON DELETE SET NULL,



    CONSTRAINT FK_AI_Feedback_Doctor

    FOREIGN KEY(Doctor_ID)

    REFERENCES Doctors(Doctor_ID)

    ON UPDATE CASCADE

    ON DELETE SET NULL,



    CONSTRAINT FK_AI_Feedback_Diagnosis

    FOREIGN KEY(Diagnosis_ID)

    REFERENCES Diagnoses(Diagnosis_ID)

    ON UPDATE CASCADE

    ON DELETE SET NULL,



    CONSTRAINT FK_AI_Feedback_Session

    FOREIGN KEY(Prediction_Session_ID)

    REFERENCES Prediction_Sessions(Prediction_Session_ID)

    ON UPDATE CASCADE

    ON DELETE SET NULL


);



-- ==========================================================
-- Indexes
-- ==========================================================


CREATE INDEX IDX_AI_Feedback_Model

ON AI_Feedback(AI_Model_Name);



CREATE INDEX IDX_AI_Feedback_Patient

ON AI_Feedback(Patient_ID);



CREATE INDEX IDX_AI_Feedback_Result

ON AI_Feedback(Prediction_Correct);



CREATE INDEX IDX_AI_Feedback_Rating

ON AI_Feedback(Feedback_Rating);