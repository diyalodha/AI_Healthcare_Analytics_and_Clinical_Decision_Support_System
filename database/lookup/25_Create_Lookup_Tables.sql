/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 25_Create_All_Lookup_Tables.sql

Purpose :
Create all lookup/master tables used throughout the
healthcare AI database.

Version : 2.2

Author : Diya Lodha & Team
===========================================================
*/


USE healthcare_ai_db;



-- ==========================================================
-- 1. Gender Lookup
-- ==========================================================


DROP TABLE IF EXISTS Gender_Lookup;


CREATE TABLE Gender_Lookup (

    Gender_ID INT AUTO_INCREMENT PRIMARY KEY,

    Gender_Name VARCHAR(50)
        UNIQUE NOT NULL,

    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);


INSERT INTO Gender_Lookup(Gender_Name)

VALUES

('Male'),
('Female'),
('Other');





-- ==========================================================
-- 2. Blood Group Lookup
-- ==========================================================


DROP TABLE IF EXISTS Blood_Group_Lookup;


CREATE TABLE Blood_Group_Lookup (

    Blood_Group_ID INT AUTO_INCREMENT PRIMARY KEY,

    Blood_Group VARCHAR(10)
        UNIQUE NOT NULL,

    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);


INSERT INTO Blood_Group_Lookup(Blood_Group)

VALUES

('A+'),
('A-'),
('B+'),
('B-'),
('AB+'),
('AB-'),
('O+'),
('O-');





-- ==========================================================
-- 3. Department Type Lookup
-- ==========================================================


DROP TABLE IF EXISTS Department_Type_Lookup;


CREATE TABLE Department_Type_Lookup (

    Department_Type_ID INT AUTO_INCREMENT PRIMARY KEY,

    Department_Type VARCHAR(100)
        UNIQUE NOT NULL,

    Description TEXT,

    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);


INSERT INTO Department_Type_Lookup
(
Department_Type,
Description
)

VALUES

('Clinical',
'Patient treatment departments'),

('Diagnostic',
'Testing and investigation departments'),

('Surgical',
'Surgery related departments'),

('Emergency',
'Emergency healthcare services'),

('Administrative',
'Hospital management departments');





-- ==========================================================
-- 4. Appointment Status Lookup
-- ==========================================================


DROP TABLE IF EXISTS Appointment_Status_Lookup;


CREATE TABLE Appointment_Status_Lookup (

    Appointment_Status_ID INT AUTO_INCREMENT PRIMARY KEY,

    Status_Name VARCHAR(50)
        UNIQUE NOT NULL,

    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);


INSERT INTO Appointment_Status_Lookup(Status_Name)

VALUES

('Scheduled'),
('Completed'),
('Cancelled'),
('Rescheduled'),
('No Show');





-- ==========================================================
-- 5. Admission Status Lookup
-- ==========================================================


DROP TABLE IF EXISTS Admission_Status_Lookup;


CREATE TABLE Admission_Status_Lookup (

    Admission_Status_ID INT AUTO_INCREMENT PRIMARY KEY,

    Status_Name VARCHAR(50)
        UNIQUE NOT NULL,

    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);


INSERT INTO Admission_Status_Lookup(Status_Name)

VALUES

('Admitted'),
('Discharged'),
('Transferred'),
('Emergency');





-- ==========================================================
-- 6. Payment Status Lookup
-- ==========================================================


DROP TABLE IF EXISTS Payment_Status_Lookup;


CREATE TABLE Payment_Status_Lookup (

    Payment_Status_ID INT AUTO_INCREMENT PRIMARY KEY,

    Status_Name VARCHAR(50)
        UNIQUE NOT NULL,

    Description TEXT,

    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);


INSERT INTO Payment_Status_Lookup
(
Status_Name,
Description
)

VALUES

('Pending',
'Payment not completed'),

('Successful',
'Payment completed'),

('Failed',
'Payment failed'),

('Refunded',
'Amount refunded'),

('Cancelled',
'Payment cancelled');





-- ==========================================================
-- 7. Billing Status Lookup
-- ==========================================================


DROP TABLE IF EXISTS Billing_Status_Lookup;


CREATE TABLE Billing_Status_Lookup (

    Billing_Status_ID INT AUTO_INCREMENT PRIMARY KEY,

    Status_Name VARCHAR(50)
        UNIQUE NOT NULL,

    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);


INSERT INTO Billing_Status_Lookup(Status_Name)

VALUES

('Generated'),
('Pending'),
('Partially Paid'),
('Paid'),
('Cancelled');





-- ==========================================================
-- 8. Risk Level Lookup
-- ==========================================================


DROP TABLE IF EXISTS Risk_Level_Lookup;


CREATE TABLE Risk_Level_Lookup (

    Risk_Level_ID INT AUTO_INCREMENT PRIMARY KEY,

    Risk_Level VARCHAR(50)
        UNIQUE NOT NULL,

    Severity_Score INT,

    Description TEXT,

    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);


INSERT INTO Risk_Level_Lookup
(
Risk_Level,
Severity_Score,
Description
)

VALUES

('Low',1,'Minimal health risk'),

('Medium',2,'Requires monitoring'),

('High',3,'Requires medical attention'),

('Critical',4,'Immediate medical intervention required');





-- ==========================================================
-- 9. User Type Lookup
-- ==========================================================


DROP TABLE IF EXISTS User_Type_Lookup;


CREATE TABLE User_Type_Lookup (

    User_Type_ID INT AUTO_INCREMENT PRIMARY KEY,

    User_Type VARCHAR(50)
        UNIQUE NOT NULL,

    Description TEXT,

    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);


INSERT INTO User_Type_Lookup
(
User_Type,
Description
)

VALUES

('Doctor','Medical practitioner'),

('Admin','System administrator'),

('Staff','Hospital staff member'),

('Researcher','Healthcare data researcher'),

('AI_System','Automated AI service');





-- ==========================================================
-- 10. Data Source Lookup
-- ==========================================================


DROP TABLE IF EXISTS Data_Source_Lookup;


CREATE TABLE Data_Source_Lookup (

    Data_Source_ID INT AUTO_INCREMENT PRIMARY KEY,

    Source_Name VARCHAR(100)
        UNIQUE NOT NULL,

    Description TEXT,

    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);


INSERT INTO Data_Source_Lookup
(
Source_Name,
Description
)

VALUES

('MIMIC-IV',
'Real ICU clinical dataset'),

('Synthetic',
'Artificial healthcare generated data'),

('Hospital_Records',
'Hospital information system data');





-- ==========================================================
-- 11. Model Status Lookup
-- ==========================================================


DROP TABLE IF EXISTS Model_Status_Lookup;


CREATE TABLE Model_Status_Lookup (

    Model_Status_ID INT AUTO_INCREMENT PRIMARY KEY,

    Status_Name VARCHAR(50)
        UNIQUE NOT NULL,

    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);


INSERT INTO Model_Status_Lookup(Status_Name)

VALUES

('Development'),
('Testing'),
('Production'),
('Deprecated');





-- ==========================================================
-- 12. Explanation Method Lookup
-- ==========================================================


DROP TABLE IF EXISTS Explanation_Method_Lookup;


CREATE TABLE Explanation_Method_Lookup (

    Explanation_Method_ID INT AUTO_INCREMENT PRIMARY KEY,

    Method_Name VARCHAR(100)
        UNIQUE NOT NULL,

    Description TEXT,

    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);


INSERT INTO Explanation_Method_Lookup
(
Method_Name,
Description
)

VALUES

('SHAP',
'Feature contribution explanation'),

('LIME',
'Local interpretable model explanation'),

('Feature Importance',
'Model feature ranking'),

('Rule Based',
'Clinical rule explanation');





-- ==========================================================
-- Verification
-- ==========================================================


SHOW TABLES;


SELECT

'All Lookup Tables Created Successfully - Version 2.2'

AS Message;