/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : Seed.sql

Purpose :
Populate healthcare_ai_db with Hybrid Healthcare Dataset

Version : 2.1

Author : Diya Lodha & Team
===========================================================
*/


USE healthcare_ai_db;


-- ==========================================================
-- SETTINGS
-- ==========================================================

SET SQL_SAFE_UPDATES = 0;

SET FOREIGN_KEY_CHECKS = 0;



-- ==========================================================
-- LOOKUP TABLE DATA
-- ==========================================================



-- Gender Lookup

INSERT INTO gender_lookup
(
    Gender_Name
)

VALUES
('Male'),
('Female'),
('Other')

ON DUPLICATE KEY UPDATE

Gender_Name = VALUES(Gender_Name);



-- Blood Group Lookup

INSERT IGNORE INTO blood_group_lookup
(
    Blood_Group
)

VALUES
('A+'),
('A-'),
('B+'),
('B-'),
('AB+'),
('AB-'),
('O+'),
('O-');



-- Department Type Lookup

INSERT IGNORE INTO department_type_lookup
(
    Department_Type
)

VALUES
('Clinical'),
('Diagnostic'),
('Administrative'),
('Support');



-- Admission Status Lookup

INSERT INTO admission_status_lookup
(
Admission_Status
)

VALUES

('Admitted'),
('Discharged'),
('Transferred'),
('Cancelled');



-- Appointment Status Lookup

INSERT INTO appointment_status_lookup
(
Appointment_Status
)

VALUES

('Scheduled'),
('Completed'),
('Cancelled'),
('No Show');



-- Billing Status Lookup

INSERT INTO billing_status_lookup
(
Billing_Status
)

VALUES

('Generated'),
('Paid'),
('Pending'),
('Cancelled');



-- Payment Status Lookup

INSERT INTO payment_status_lookup
(
Payment_Status
)

VALUES

('Pending'),
('Paid'),
('Failed'),
('Refunded');



-- Risk Level Lookup

INSERT INTO risk_level_lookup
(
Risk_Level
)

VALUES

('Low'),
('Medium'),
('High'),
('Critical');



-- Model Status Lookup

INSERT INTO model_status_lookup
(
Model_Status
)

VALUES

('Training'),
('Testing'),
('Production'),
('Archived');



-- User Type Lookup

INSERT INTO user_type_lookup
(
User_Type
)

VALUES

('Admin'),
('Doctor'),
('Nurse'),
('Patient'),
('Researcher');



-- Data Source Lookup

INSERT INTO data_source_lookup
(
Source_Name
)

VALUES

('MIMIC-IV'),
('Hospital Records'),
('Synthetic Generator'),
('Hybrid Dataset');



-- Explanation Method Lookup

INSERT INTO explanation_method_lookup
(
Method_Name
)

VALUES

('SHAP'),
('LIME'),
('Feature Importance');



SET FOREIGN_KEY_CHECKS = 1;

-- ==========================================================
-- 02. DEPARTMENTS
-- ==========================================================


SET FOREIGN_KEY_CHECKS = 0;


INSERT INTO departments
(
Department_ID,
Department_Name,
Department_Code,
Description,
Department_Type,
Contact_Number,
Email,
Location,
Floor_Number,
Capacity,
Status
)

VALUES


(
UUID(),
'Cardiology',
'CARD',
'Heart and cardiovascular care department',
'Clinical',
'0204001001',
'cardiology@hospital.com',
'Block A',
2,
50,
'Active'
),


(
UUID(),
'Neurology',
'NEUR',
'Brain and nervous system department',
'Clinical',
'0204001002',
'neurology@hospital.com',
'Block B',
3,
40,
'Active'
),


(
UUID(),
'Orthopedics',
'ORTHO',
'Bone and joint treatment department',
'Clinical',
'0204001003',
'orthopedics@hospital.com',
'Block C',
2,
60,
'Active'
),


(
UUID(),
'Radiology',
'RAD',
'Medical imaging and diagnostics',
'Diagnostic',
'0204001004',
'radiology@hospital.com',
'Block D',
1,
30,
'Active'
),


(
UUID(),
'Intensive Care Unit',
'ICU',
'Critical patient monitoring unit',
'Clinical',
'0204001005',
'icu@hospital.com',
'Block E',
5,
20,
'Active'
);



-- ==========================================================
-- 03. DOCTORS
-- ==========================================================


INSERT INTO doctors
(
Doctor_ID,
First_Name,
Last_Name,
Gender,
Medical_License_No,
Qualification,
Specialization,
Years_of_Experience,
Department_ID,
Phone,
Email,
Joining_Date,
Status
)

SELECT

UUID(),
'Raj',
'Sharma',
'Male',
'MED1001',
'MBBS MD',
'Cardiologist',
12,
Department_ID,
'9876543210',
'raj.sharma@hospital.com',
'2018-06-01',
'Active'

FROM departments

WHERE Department_Code='CARD';



INSERT INTO doctors
(
Doctor_ID,
First_Name,
Last_Name,
Gender,
Medical_License_No,
Qualification,
Specialization,
Years_of_Experience,
Department_ID,
Phone,
Email,
Joining_Date,
Status
)

SELECT

UUID(),
'Priya',
'Patil',
'Female',
'MED1002',
'MBBS MD',
'Neurologist',
10,
Department_ID,
'9876543211',
'priya.patil@hospital.com',
'2019-01-10',
'Active'

FROM departments

WHERE Department_Code='NEUR';



INSERT INTO doctors
(
Doctor_ID,
First_Name,
Last_Name,
Gender,
Medical_License_No,
Qualification,
Specialization,
Years_of_Experience,
Department_ID,
Phone,
Email,
Joining_Date,
Status
)

SELECT

UUID(),
'Amit',
'Kulkarni',
'Male',
'MED1003',
'MBBS MS',
'Orthopedic Surgeon',
8,
Department_ID,
'9876543212',
'amit.kulkarni@hospital.com',
'2020-03-15',
'Active'

FROM departments

WHERE Department_Code='ORTHO';



-- ==========================================================
-- Update Department Heads
-- ==========================================================


UPDATE departments d

JOIN doctors doc

ON d.Department_Code='CARD'

AND doc.Medical_License_No='MED1001'

SET d.Head_Doctor_ID = doc.Doctor_ID;



UPDATE departments d

JOIN doctors doc

ON d.Department_Code='NEUR'

AND doc.Medical_License_No='MED1002'

SET d.Head_Doctor_ID = doc.Doctor_ID;



-- ==========================================================
-- 04. PATIENTS
-- ==========================================================


INSERT INTO patients
(
Patient_ID,
First_Name,
Last_Name,
Gender,
Date_of_Birth,
Blood_Group,
Phone,
Email,
Nationality,
Preferred_Language,
Height_cm,
Weight_kg
)

VALUES


(
UUID(),
'Amit',
'Joshi',
'Male',
'1995-04-12',
'A+',
'9000000001',
'amit.joshi@gmail.com',
'Indian',
'English',
175,
72
),


(
UUID(),
'Neha',
'Kulkarni',
'Female',
'1998-09-21',
'B+',
'9000000002',
'neha.k@gmail.com',
'Indian',
'Marathi',
160,
55
),


(
UUID(),
'Rahul',
'More',
'Male',
'1987-02-10',
'O+',
'9000000003',
'rahul.more@gmail.com',
'Indian',
'Hindi',
178,
80
),


(
UUID(),
'Sneha',
'Patil',
'Female',
'2000-06-18',
'AB+',
'9000000004',
'sneha.patil@gmail.com',
'Indian',
'English',
165,
60
);



-- ==========================================================
-- 05. INSURANCE PROVIDERS
-- ==========================================================


INSERT INTO insurance_providers
(
Insurance_Provider_ID,
Provider_Name,
Contact_Number,
Email,
Address,
Coverage_Type,
Status
)

VALUES


(
UUID(),
'Star Health Insurance',
'18001001001',
'contact@starhealth.com',
'Mumbai Maharashtra',
'Health Insurance',
'Active'
),


(
UUID(),
'ICICI Lombard Health',
'18001001002',
'health@icicilombard.com',
'Mumbai Maharashtra',
'Health Insurance',
'Active'
),


(
UUID(),
'HDFC ERGO Health',
'18001001003',
'health@hdfcergo.com',
'Mumbai Maharashtra',
'Health Insurance',
'Active'
),


(
UUID(),
'Bajaj Allianz Health',
'18001001004',
'health@bajajallianz.com',
'Pune Maharashtra',
'Health Insurance',
'Active'
);



SET FOREIGN_KEY_CHECKS = 1;



-- Verification

SELECT COUNT(*) AS Department_Count 
FROM departments;


SELECT COUNT(*) AS Doctor_Count 
FROM doctors;


SELECT COUNT(*) AS Patient_Count 
FROM patients;


SELECT COUNT(*) AS Insurance_Count 
FROM insurance_providers;

-- ==========================================================
-- 06. HOSPITAL ROOMS
-- ==========================================================


SET FOREIGN_KEY_CHECKS = 0;



INSERT INTO hospital_rooms
(
Room_ID,
Room_Number,
Room_Type,
Floor_Number,
Department_ID,
Capacity,
Status
)

SELECT

UUID(),
'ICU-101',
'ICU',
5,
Department_ID,
1,
'Available'

FROM departments

WHERE Department_Code='ICU';



INSERT INTO hospital_rooms
(
Room_ID,
Room_Number,
Room_Type,
Floor_Number,
Department_ID,
Capacity,
Status
)

SELECT

UUID(),
'CARD-201',
'General',
2,
Department_ID,
2,
'Available'

FROM departments

WHERE Department_Code='CARD';



INSERT INTO hospital_rooms
(
Room_ID,
Room_Number,
Room_Type,
Floor_Number,
Department_ID,
Capacity,
Status
)

SELECT

UUID(),
'NEUR-301',
'Private',
3,
Department_ID,
1,
'Available'

FROM departments

WHERE Department_Code='NEUR';



-- ==========================================================
-- 07. BEDS
-- ==========================================================


INSERT INTO beds
(
Bed_ID,
Room_ID,
Bed_Number,
Bed_Type,
Bed_Status
)

SELECT

UUID(),
Room_ID,
'ICU-101-A',
'ICU',
'Available'

FROM hospital_rooms

WHERE Room_Number='ICU-101';



INSERT INTO beds
(
Bed_ID,
Room_ID,
Bed_Number,
Bed_Type,
Bed_Status
)

SELECT

UUID(),
Room_ID,
'CARD-201-A',
'General',
'Available'

FROM hospital_rooms

WHERE Room_Number='CARD-201';



INSERT INTO beds
(
Bed_ID,
Room_ID,
Bed_Number,
Bed_Type,
Bed_Status
)

SELECT

UUID(),
Room_ID,
'NEUR-301-A',
'Private',
'Available'

FROM hospital_rooms

WHERE Room_Number='NEUR-301';



-- ==========================================================
-- 08. OPERATION THEATRE
-- ==========================================================


INSERT INTO operation_theatre
(
OT_ID,
OT_Name,
OT_Number,
OT_Type,
Location,
Availability_Status,
Equipment_Status
)

VALUES


(
UUID(),
'Main General OT',
'OT-001',
'General',
'Block F',
'Available',
'Operational'
),


(
UUID(),
'Emergency OT',
'OT-002',
'Emergency',
'Block F',
'Available',
'Operational'
);



-- ==========================================================
-- 09. MEDICAL DEVICES
-- ==========================================================


INSERT INTO medical_devices
(
Device_ID,
Device_Name,
Device_Category,
Manufacturer,
Model_Number,
Serial_Number,
Device_Status,
Location
)

VALUES


(
UUID(),
'Patient Monitor',
'Monitoring',
'Philips',
'PM-500',
'PH001',
'Active',
'ICU'
),


(
UUID(),
'CT Scanner',
'Imaging',
'Siemens',
'CT-700',
'SIE001',
'Active',
'Radiology'
),


(
UUID(),
'Ventilator',
'ICU',
'GE Healthcare',
'VENT-100',
'GE001',
'Active',
'ICU'
);



-- ==========================================================
-- 10. INVENTORY
-- ==========================================================


INSERT INTO inventory
(
Inventory_ID,
Item_Name,
Item_Category,
Manufacturer,
Item_Code,
Quantity_Available,
Minimum_Required_Quantity,
Unit_Type,
Storage_Location,
Inventory_Status
)

VALUES


(
UUID(),
'Surgical Gloves',
'Surgical Supplies',
'MedCare',
'SG001',
500,
100,
'Boxes',
'Store Room A',
'Available'
),


(
UUID(),
'Syringe',
'Consumables',
'HealthPlus',
'SY001',
1000,
200,
'Pieces',
'Store Room B',
'Available'
),


(
UUID(),
'Blood Collection Kit',
'Laboratory',
'BioLabs',
'BC001',
300,
50,
'Kits',
'Laboratory Store',
'Available'
);



-- ==========================================================
-- 11. BLOOD BANK
-- ==========================================================


INSERT INTO blood_bank
(
Blood_Bank_ID,
Blood_Group,
Units_Available,
Storage_Location,
Status
)

VALUES


(
UUID(),
'A+',
25,
'Blood Bank Room 1',
'Available'
),


(
UUID(),
'B+',
20,
'Blood Bank Room 1',
'Available'
),


(
UUID(),
'O+',
40,
'Blood Bank Room 2',
'Available'
),


(
UUID(),
'AB+',
15,
'Blood Bank Room 2',
'Available'
);



SET FOREIGN_KEY_CHECKS = 1;



-- Verification

SELECT COUNT(*) AS Rooms
FROM hospital_rooms;


SELECT COUNT(*) AS Beds
FROM beds;


SELECT COUNT(*) AS Devices
FROM medical_devices;


SELECT COUNT(*) AS Inventory_Items
FROM inventory;


SELECT COUNT(*) AS Blood_Units
FROM blood_bank;

-- ==========================================================
-- 12. DISEASE MASTER DATA
-- ==========================================================


SET FOREIGN_KEY_CHECKS = 0;



INSERT INTO diseases
(
Disease_ID,
Disease_Name,
Disease_Category,
Description
)

VALUES


(
UUID(),
'Diabetes Mellitus',
'Endocrine',
'Chronic disease affecting blood glucose regulation'
),


(
UUID(),
'Hypertension',
'Cardiovascular',
'High blood pressure condition'
),


(
UUID(),
'Coronary Artery Disease',
'Cardiovascular',
'Disease affecting coronary arteries'
),


(
UUID(),
'Asthma',
'Respiratory',
'Chronic respiratory condition'
),


(
UUID(),
'Pneumonia',
'Respiratory',
'Infection causing lung inflammation'
);



-- ==========================================================
-- 13. MEDICATION MASTER
-- ==========================================================


INSERT INTO medications
(
Medicine_ID,
Medicine_Name,
Generic_Name,
Medicine_Type,
Manufacturer,
Dosage_Form,
Strength,
Status
)

VALUES


(
UUID(),
'Metformin',
'Metformin Hydrochloride',
'Tablet',
'Sun Pharma',
'Tablet',
'500mg',
'Active'
),


(
UUID(),
'Amlodipine',
'Amlodipine Besylate',
'Tablet',
'Cipla',
'Tablet',
'5mg',
'Active'
),


(
UUID(),
'Aspirin',
'Acetylsalicylic Acid',
'Tablet',
'Bayer',
'Tablet',
'75mg',
'Active'
),


(
UUID(),
'Salbutamol',
'Salbutamol Sulphate',
'Inhaler',
'GSK',
'Inhaler',
'100mcg',
'Active'
);



-- ==========================================================
-- 14. MEDICINE STOCK
-- ==========================================================


INSERT INTO medicine_stock
(
Medicine_Stock_ID,
Medicine_ID,
Batch_Number,
Manufacturing_Date,
Expiry_Date,
Quantity_Available,
Minimum_Stock_Level,
Purchase_Price,
Selling_Price,
Supplier_Name,
Stock_Status
)

SELECT

UUID(),
Medicine_ID,
'BATCH001',
'2025-01-01',
'2027-01-01',
500,
50,
10,
15,
'HealthCare Suppliers',
'Available'

FROM medications

WHERE Medicine_Name='Metformin';



-- ==========================================================
-- 15. LAB TEST MASTER
-- ==========================================================


INSERT INTO lab_tests
(
Lab_Test_ID,
Test_Name,
Test_Category,
Description,
Normal_Range
)

VALUES


(
UUID(),
'Complete Blood Count',
'Hematology',
'Blood cell analysis test',
'Normal'
),


(
UUID(),
'Blood Glucose Test',
'Biochemistry',
'Measures glucose level',
'70-120 mg/dL'
),


(
UUID(),
'Lipid Profile',
'Biochemistry',
'Measures cholesterol levels',
'Normal'
),


(
UUID(),
'Chest X-Ray',
'Imaging',
'Chest imaging test',
'Normal'
);



-- ==========================================================
-- 16. DOCTOR SCHEDULES
-- ==========================================================


INSERT INTO doctor_schedules
(
Schedule_ID,
Doctor_ID,
Available_Date,
Start_Time,
End_Time,
Consultation_Type,
Max_Patients,
Schedule_Status
)

SELECT

UUID(),
Doctor_ID,
'2026-07-23',
'09:00:00',
'13:00:00',
'OPD',
20,
'Available'

FROM doctors

LIMIT 3;



-- ==========================================================
-- 17. ROLES
-- ==========================================================


INSERT INTO roles
(
Role_ID,
Role_Name,
Description
)

VALUES


(
UUID(),
'Admin',
'System administrator'
),


(
UUID(),
'Doctor',
'Medical practitioner'
),


(
UUID(),
'Nurse',
'Healthcare support staff'
),


(
UUID(),
'Patient',
'Registered patient'
);



-- ==========================================================
-- 18. USERS
-- ==========================================================


INSERT INTO users
(
User_ID,
Username,
Password_Hash,
Email,
Role_ID,
Status
)

SELECT

UUID(),
'admin_user',
'hashed_password',
'admin@hospital.com',
Role_ID,
'Active'

FROM roles

WHERE Role_Name='Admin';



-- ==========================================================
-- 19. EMERGENCY CONTACTS
-- ==========================================================


INSERT INTO emergency_contacts
(
Emergency_Contact_ID,
Patient_ID,
Contact_Name,
Relationship,
Phone_Number
)

SELECT

UUID(),
Patient_ID,
'Family Contact',
'Relative',
'9000000099'

FROM patients

LIMIT 3;



-- ==========================================================
-- 20. NURSE ASSIGNMENTS
-- ==========================================================


INSERT INTO nurse_assignments
(
Assignment_ID,
Patient_ID,
Nurse_ID,
Assignment_Date,
Shift_Type,
Responsibility_Level,
Assignment_Status
)

SELECT

UUID(),
p.Patient_ID,
d.Doctor_ID,
'2026-07-22',
'Morning',
'Primary Nurse',
'Active'

FROM patients p

JOIN doctors d

LIMIT 2;



-- ==========================================================
-- 21. REFERRALS
-- ==========================================================


INSERT INTO referrals
(
Referral_ID,
Patient_ID,
Referring_Doctor_ID,
Receiving_Doctor_ID,
Referral_Date,
Referral_Type,
Referral_Reason,
Priority_Level,
Referral_Status
)

SELECT

UUID(),
p.Patient_ID,
d1.Doctor_ID,
d2.Doctor_ID,
'2026-07-22',
'Internal',
'Specialist consultation required',
'Medium',
'Pending'

FROM patients p

JOIN doctors d1

JOIN doctors d2

WHERE d1.Doctor_ID <> d2.Doctor_ID

LIMIT 2;



SET FOREIGN_KEY_CHECKS = 1;



-- Verification

SELECT COUNT(*) FROM diseases;

SELECT COUNT(*) FROM medications;

SELECT COUNT(*) FROM lab_tests;

SELECT COUNT(*) FROM doctor_schedules;

SELECT COUNT(*) FROM users;

/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : Seed.sql

Section : Patients Seed Data

Purpose :
Insert sample patient records for hybrid healthcare dataset

===========================================================
*/


USE healthcare_ai_db;



-- ==========================================================
-- Clear Existing Data
-- ==========================================================

SET FOREIGN_KEY_CHECKS = 0;


DELETE FROM Patients;


SET FOREIGN_KEY_CHECKS = 1;



-- ==========================================================
-- Insert Patients
-- ==========================================================


INSERT INTO Patients
(
    Patient_ID,
    First_Name,
    Middle_Name,
    Last_Name,
    Gender,
    Date_of_Birth,
    Blood_Group,
    Phone,
    Email,
    Address,
    City,
    State,
    Country,
    Pincode,
    Emergency_Contact_Name,
    Emergency_Contact_Number,
    Registration_Date,
    Patient_Status,
    Created_At
)

VALUES


(
    UUID(),
    'Aarav',
    NULL,
    'Sharma',
    'Male',
    '1995-04-15',
    'O+',
    '9876500001',
    'aarav.sharma@email.com',
    'Shivaji Nagar',
    'Pune',
    'Maharashtra',
    'India',
    '411005',
    'Rohan Sharma',
    '9876500011',
    '2023-01-10',
    'Active',
    CURRENT_TIMESTAMP
),



(
    UUID(),
    'Ananya',
    NULL,
    'Patil',
    'Female',
    '1998-08-22',
    'A+',
    '9876500002',
    'ananya.patil@email.com',
    'Kothrud',
    'Pune',
    'Maharashtra',
    'India',
    '411038',
    'Sonal Patil',
    '9876500012',
    '2023-02-18',
    'Active',
    CURRENT_TIMESTAMP
),



(
    UUID(),
    'Rajesh',
    NULL,
    'Kulkarni',
    'Male',
    '1978-12-05',
    'B+',
    '9876500003',
    'rajesh.kulkarni@email.com',
    'Camp Area',
    'Solapur',
    'Maharashtra',
    'India',
    '413001',
    'Neha Kulkarni',
    '9876500013',
    '2022-11-25',
    'Active',
    CURRENT_TIMESTAMP
),



(
    UUID(),
    'Priya',
    NULL,
    'Deshmukh',
    'Female',
    '1992-06-11',
    'AB+',
    '9876500004',
    'priya.deshmukh@email.com',
    'Viman Nagar',
    'Pune',
    'Maharashtra',
    'India',
    '411014',
    'Amit Deshmukh',
    '9876500014',
    '2024-01-05',
    'Active',
    CURRENT_TIMESTAMP
),



(
    UUID(),
    'Vikram',
    NULL,
    'Joshi',
    'Male',
    '1965-03-29',
    'O-',
    '9876500005',
    'vikram.joshi@email.com',
    'Akurdi',
    'Pune',
    'Maharashtra',
    'India',
    '411035',
    'Meera Joshi',
    '9876500015',
    '2021-07-19',
    'Active',
    CURRENT_TIMESTAMP
);



-- ==========================================================
-- Verification
-- ==========================================================


SELECT COUNT(*) AS Total_Patients
FROM Patients;


SELECT *
FROM Patients;

-- ==========================================================
-- Seed Medications Table
-- ==========================================================

DELETE FROM Medications;


INSERT INTO Medications
(
    Medication_ID,
    Medication_Name,
    Generic_Name,
    Medicine_Type,
    Strength,
    Manufacturer,
    Category,
    Description,
    Status
)

VALUES

(
    UUID(),
    'Metformin',
    'Metformin Hydrochloride',
    'Tablet',
    '500 mg',
    'Sun Pharma',
    'Antidiabetic',
    'Used for management of Type 2 Diabetes',
    'Active'
),


(
    UUID(),
    'Paracetamol',
    'Acetaminophen',
    'Tablet',
    '650 mg',
    'Cipla',
    'Analgesic',
    'Used for fever and pain relief',
    'Active'
),


(
    UUID(),
    'Amlodipine',
    'Amlodipine Besylate',
    'Tablet',
    '5 mg',
    'Dr Reddy Laboratories',
    'Cardiac',
    'Used for blood pressure management',
    'Active'
),


(
    UUID(),
    'Atorvastatin',
    'Atorvastatin Calcium',
    'Tablet',
    '10 mg',
    'Lupin',
    'Cholesterol',
    'Used for cholesterol control',
    'Active'
),


(
    UUID(),
    'Omeprazole',
    'Omeprazole',
    'Capsule',
    '20 mg',
    'Abbott',
    'Gastrointestinal',
    'Used for gastric disorders',
    'Active'
);



-- ==========================================================
-- Verification
-- ==========================================================

SELECT COUNT(*) AS Total_Medications
FROM Medications;


SELECT *
FROM Medications;

-- ==========================================================
-- Seed Prescriptions Table
-- ==========================================================


DELETE FROM Prescriptions;



INSERT INTO Prescriptions
(
    Prescription_ID,
    Patient_ID,
    Doctor_ID,
    Medication_ID,
    Prescription_Date,
    Dosage,
    Frequency,
    Duration_Days,
    Route,
    Instructions,
    Prescription_Status
)


SELECT

    UUID(),

    p.Patient_ID,

    doc.Doctor_ID,

    m.Medication_ID,

    CURRENT_DATE,

    '1 Tablet',

    'Twice Daily',

    30,

    'Oral',

    'Take medicine after meals',

    'Active'


FROM Patients p

JOIN Doctors doc

ON 1=1

JOIN Medications m

ON m.Medication_Name = 'Metformin'


LIMIT 10;



-- ==========================================================
-- Verification
-- ==========================================================


SELECT COUNT(*) AS Total_Prescriptions
FROM Prescriptions;


SELECT *
FROM Prescriptions;

-- ==========================================================
-- Seed Lab_Tests Table
-- ==========================================================


DELETE FROM Lab_Tests;



INSERT INTO Lab_Tests
(
    Lab_Test_ID,
    Test_Name,
    Test_Category,
    Description,
    Normal_Range,
    Unit,
    Status
)

VALUES


(
    UUID(),
    'Complete Blood Count',
    'Hematology',
    'Measures blood cells and overall health condition',
    'Normal Range',
    'cells/mcL',
    'Active'
),


(
    UUID(),
    'Blood Glucose Test',
    'Biochemistry',
    'Measures blood sugar level',
    '70-140',
    'mg/dL',
    'Active'
),


(
    UUID(),
    'Lipid Profile',
    'Biochemistry',
    'Measures cholesterol and lipid levels',
    'Normal Range',
    'mg/dL',
    'Active'
),


(
    UUID(),
    'Kidney Function Test',
    'Biochemistry',
    'Evaluates kidney performance',
    'Normal Range',
    'mg/dL',
    'Active'
),


(
    UUID(),
    'Liver Function Test',
    'Biochemistry',
    'Evaluates liver health',
    'Normal Range',
    'U/L',
    'Active'
);



-- ==========================================================
-- Verification
-- ==========================================================


SELECT COUNT(*) AS Total_Lab_Tests
FROM Lab_Tests;


SELECT *
FROM Lab_Tests;

-- ==========================================================
-- Seed Lab_Results Table
-- ==========================================================


DELETE FROM Lab_Results;



INSERT INTO Lab_Results
(
    Lab_Result_ID,
    Patient_ID,
    Lab_Test_ID,
    Doctor_ID,
    Test_Date,
    Result_Value,
    Result_Unit,
    Reference_Range,
    Result_Status,
    Remarks
)


SELECT

    UUID(),

    p.Patient_ID,

    lt.Lab_Test_ID,

    doc.Doctor_ID,

    CURRENT_DATE,

    CASE

        WHEN lt.Test_Name = 'Blood Glucose Test'
        THEN '126'

        WHEN lt.Test_Name = 'Complete Blood Count'
        THEN 'Normal'

        WHEN lt.Test_Name = 'Lipid Profile'
        THEN '185'

        WHEN lt.Test_Name = 'Kidney Function Test'
        THEN 'Normal'

        WHEN lt.Test_Name = 'Liver Function Test'
        THEN 'Normal'

    END,

    CASE

        WHEN lt.Test_Name IN 
        (
            'Blood Glucose Test',
            'Lipid Profile'
        )
        THEN 'mg/dL'

        ELSE 'N/A'

    END,

    lt.Normal_Range,

    'Completed',

    'Routine health examination result'


FROM Patients p

JOIN Lab_Tests lt

JOIN Doctors doc

LIMIT 20;



-- ==========================================================
-- Verification
-- ==========================================================


SELECT COUNT(*) AS Total_Lab_Results
FROM Lab_Results;


SELECT *
FROM Lab_Results;

-- ==========================================================
-- Seed Vital_Signs Table
-- ==========================================================


DELETE FROM Vital_Signs;



INSERT INTO Vital_Signs
(
    Vital_Sign_ID,
    Patient_ID,
    Recorded_By_Doctor_ID,
    Record_Date,
    Temperature,
    Heart_Rate,
    Blood_Pressure_Systolic,
    Blood_Pressure_Diastolic,
    Respiratory_Rate,
    Oxygen_Saturation,
    Blood_Glucose_Level,
    Weight,
    Height,
    Notes
)


SELECT

    UUID(),

    p.Patient_ID,

    doc.Doctor_ID,

    CURRENT_TIMESTAMP,

    98.6,

    78,

    120,

    80,

    18,

    98,

    110,

    65,

    170,

    'Routine vital monitoring'


FROM Patients p

JOIN Doctors doc

LIMIT 20;



-- ==========================================================
-- Verification
-- ==========================================================


SELECT COUNT(*) AS Total_Vital_Records
FROM Vital_Signs;


SELECT *
FROM Vital_Signs;

-- ==========================================================
-- Seed Patient_Allergies Table
-- ==========================================================


DELETE FROM Patient_Allergies;



INSERT INTO Patient_Allergies
(
    Allergy_ID,
    Patient_ID,
    Allergy_Name,
    Allergy_Type,
    Severity,
    Reaction,
    Diagnosed_Date,
    Notes
)


SELECT

    UUID(),

    p.Patient_ID,

    a.Allergy_Name,

    a.Allergy_Type,

    a.Severity,

    a.Reaction,

    CURRENT_DATE,

    'Patient allergy recorded during medical history evaluation'


FROM Patients p

JOIN
(
    SELECT 
        'Penicillin' AS Allergy_Name,
        'Drug' AS Allergy_Type,
        'Moderate' AS Severity,
        'Skin Rash' AS Reaction

    UNION ALL

    SELECT
        'Peanuts',
        'Food',
        'Severe',
        'Breathing Difficulty'

    UNION ALL

    SELECT
        'Dust',
        'Environmental',
        'Mild',
        'Sneezing'

) a

LIMIT 15;



-- ==========================================================
-- Verification
-- ==========================================================


SELECT COUNT(*) AS Total_Allergies
FROM Patient_Allergies;


SELECT *
FROM Patient_Allergies;

-- ==========================================================
-- Seed Vaccination_History Table
-- ==========================================================


DELETE FROM Vaccination_History;



INSERT INTO Vaccination_History
(
    Vaccination_ID,
    Patient_ID,
    Vaccine_Name,
    Vaccine_Type,
    Dose_Number,
    Vaccination_Date,
    Administered_By,
    Manufacturer,
    Notes
)


SELECT

    UUID(),

    p.Patient_ID,

    v.Vaccine_Name,

    v.Vaccine_Type,

    v.Dose_Number,

    DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR),

    'Hospital Vaccination Center',

    v.Manufacturer,

    'Vaccination record maintained'


FROM Patients p

JOIN
(
    SELECT
        'COVID-19 Vaccine' AS Vaccine_Name,
        'Preventive' AS Vaccine_Type,
        1 AS Dose_Number,
        'Covishield' AS Manufacturer

    UNION ALL

    SELECT
        'Influenza Vaccine',
        'Preventive',
        1,
        'Sanofi'

    UNION ALL

    SELECT
        'Hepatitis B Vaccine',
        'Preventive',
        3,
        'GSK'

) v

LIMIT 15;



SELECT COUNT(*) AS Total_Vaccinations
FROM Vaccination_History;

-- ==========================================================
-- Seed Clinical_Notes Table
-- ==========================================================


DELETE FROM Clinical_Notes;



INSERT INTO Clinical_Notes
(
    Clinical_Note_ID,
    Patient_ID,
    Doctor_ID,
    Note_Date,
    Note_Type,
    Clinical_Observation,
    Diagnosis_Summary,
    Treatment_Plan,
    Additional_Remarks
)


SELECT

    UUID(),

    p.Patient_ID,

    d.Doctor_ID,

    CURRENT_TIMESTAMP,

    'Consultation',

    'Patient evaluated with routine clinical examination',

    'General health assessment completed',

    'Continue medication and regular monitoring',

    'Follow up after 30 days'


FROM Patients p

JOIN Doctors d

LIMIT 15;



SELECT COUNT(*) AS Total_Clinical_Notes
FROM Clinical_Notes;

-- ==========================================================
-- Seed Medical_Procedures Table
-- ==========================================================


DELETE FROM Medical_Procedures;



INSERT INTO Medical_Procedures
(
    Procedure_ID,
    Patient_ID,
    Doctor_ID,
    Procedure_Name,
    Procedure_Type,
    Procedure_Date,
    Procedure_Status,
    Description,
    Cost
)


SELECT

    UUID(),

    p.Patient_ID,

    d.Doctor_ID,

    pr.Procedure_Name,

    pr.Procedure_Type,

    CURRENT_DATE,

    'Completed',

    pr.Description,

    pr.Cost


FROM Patients p

JOIN Doctors d

JOIN
(
    SELECT
        'Blood Test' AS Procedure_Name,
        'Diagnostic' AS Procedure_Type,
        'Routine blood examination' AS Description,
        500 AS Cost


    UNION ALL


    SELECT
        'ECG',
        'Diagnostic',
        'Heart electrical activity monitoring',
        800


    UNION ALL


    SELECT
        'X-Ray',
        'Imaging',
        'Radiology imaging procedure',
        1200

) pr

LIMIT 15;



SELECT COUNT(*) AS Total_Procedures
FROM Medical_Procedures;

-- ==========================================================
-- Seed Hospital_Rooms Table
-- ==========================================================


DELETE FROM Hospital_Rooms;



INSERT INTO Hospital_Rooms
(
    Room_ID,
    Room_Number,
    Room_Type,
    Department_ID,
    Floor_Number,
    Capacity,
    Availability_Status,
    Notes
)


SELECT

    UUID(),

    r.Room_Number,

    r.Room_Type,

    d.Department_ID,

    r.Floor_Number,

    r.Capacity,

    'Available',

    'Hospital room allocated for patient care'


FROM Departments d

JOIN
(
    SELECT
        '101' AS Room_Number,
        'General' AS Room_Type,
        1 AS Floor_Number,
        2 AS Capacity

    UNION ALL

    SELECT
        '102',
        'Private',
        1,
        1

    UNION ALL

    SELECT
        '201',
        'ICU',
        2,
        1

    UNION ALL

    SELECT
        '202',
        'Semi Private',
        2,
        2

) r

LIMIT 10;



SELECT COUNT(*) AS Total_Rooms
FROM Hospital_Rooms;

-- ==========================================================
-- Seed Beds Table
-- ==========================================================


DELETE FROM Beds;



INSERT INTO Beds
(
    Bed_ID,
    Room_ID,
    Bed_Number,
    Bed_Type,
    Availability_Status,
    Notes
)


SELECT

    UUID(),

    hr.Room_ID,

    b.Bed_Number,

    b.Bed_Type,

    'Available',

    'Bed registered in hospital inventory'


FROM Hospital_Rooms hr

JOIN
(
    SELECT
        'A1' AS Bed_Number,
        'General' AS Bed_Type

    UNION ALL

    SELECT
        'A2',
        'General'

    UNION ALL

    SELECT
        'B1',
        'ICU'

    UNION ALL

    SELECT
        'B2',
        'ICU'

) b

LIMIT 20;



SELECT COUNT(*) AS Total_Beds
FROM Beds;

-- ==========================================================
-- Seed ICU_Stay_Details Table
-- ==========================================================


DELETE FROM ICU_Stay_Details;



INSERT INTO ICU_Stay_Details
(
    ICU_Stay_ID,
    Patient_ID,
    Bed_ID,
    Admission_Date,
    Discharge_Date,
    ICU_Type,
    Reason_For_ICU,
    Ventilator_Required,
    Status,
    Notes
)


SELECT

    UUID(),

    p.Patient_ID,

    b.Bed_ID,

    DATE_SUB(CURRENT_DATE, INTERVAL 5 DAY),

    CURRENT_DATE,

    'Medical ICU',

    'Critical monitoring required',

    FALSE,

    'Completed',

    'Patient monitored under ICU care'


FROM Patients p

JOIN Beds b

LIMIT 10;



SELECT COUNT(*) AS Total_ICU_Stays
FROM ICU_Stay_Details;

-- ==========================================================
-- Seed Admissions Table
-- ==========================================================


DELETE FROM Admissions;



INSERT INTO Admissions
(
    Admission_ID,
    Patient_ID,
    Doctor_ID,
    Department_ID,
    Bed_ID,
    Admission_Date,
    Admission_Type,
    Admission_Status,
    Reason_For_Admission,
    Notes
)


SELECT

    UUID(),

    p.Patient_ID,

    d.Doctor_ID,

    dept.Department_ID,

    b.Bed_ID,

    CURRENT_DATE,

    'Emergency',

    'Discharged',

    'Medical evaluation and treatment required',

    'Patient admitted for observation'


FROM Patients p

JOIN Doctors d

JOIN Departments dept

JOIN Beds b

LIMIT 10;



SELECT COUNT(*) AS Total_Admissions
FROM Admissions;

-- ==========================================================
-- Seed Discharge_Summary Table
-- ==========================================================


DELETE FROM Discharge_Summary;



INSERT INTO Discharge_Summary
(
    Discharge_ID,
    Patient_ID,
    Doctor_ID,
    Admission_ID,
    Discharge_Date,
    Final_Diagnosis,
    Treatment_Summary,
    Discharge_Status,
    Follow_Up_Instructions
)


SELECT

    UUID(),

    a.Patient_ID,

    a.Doctor_ID,

    a.Admission_ID,

    CURRENT_DATE,

    'Patient recovered after treatment',

    'Medication and monitoring completed',

    'Stable',

    'Follow up after 30 days'


FROM Admissions a;



SELECT COUNT(*) AS Total_Discharge_Summaries
FROM Discharge_Summary;

-- ==========================================================
-- Seed Emergency_Contacts Table
-- ==========================================================


DELETE FROM Emergency_Contacts;



INSERT INTO Emergency_Contacts
(
    Emergency_Contact_ID,
    Patient_ID,
    Contact_Name,
    Relationship,
    Contact_Number,
    Address,
    Is_Primary
)


SELECT

    UUID(),

    p.Patient_ID,

    e.Contact_Name,

    e.Relationship,

    e.Contact_Number,

    e.Address,

    TRUE


FROM Patients p

JOIN
(
    SELECT

        'Rahul Sharma' AS Contact_Name,

        'Brother' AS Relationship,

        '9876501010' AS Contact_Number,

        'Pune, Maharashtra' AS Address


    UNION ALL


    SELECT

        'Sneha Patil',

        'Sister',

        '9876502020',

        'Solapur, Maharashtra'

) e

LIMIT 10;



SELECT COUNT(*) AS Total_Emergency_Contacts
FROM Emergency_Contacts;

-- ==========================================================
-- Seed Billing Table
-- ==========================================================


DELETE FROM Billing;



INSERT INTO Billing
(
    Billing_ID,
    Patient_ID,
    Admission_ID,
    Billing_Date,
    Total_Amount,
    Discount_Amount,
    Tax_Amount,
    Final_Amount,
    Billing_Status,
    Payment_Status,
    Notes
)


SELECT

    UUID(),

    a.Patient_ID,

    a.Admission_ID,

    CURRENT_DATE,

    25000.00,

    2000.00,

    1500.00,

    24500.00,

    'Generated',

    'Paid',

    'Hospital service billing generated'


FROM Admissions a;



SELECT COUNT(*) AS Total_Bills
FROM Billing;

-- ==========================================================
-- Seed Payments Table
-- ==========================================================


DELETE FROM Payments;



INSERT INTO Payments
(
    Payment_ID,
    Billing_ID,
    Patient_ID,
    Payment_Date,
    Payment_Mode,
    Transaction_ID,
    Amount_Paid,
    Payment_Status,
    Notes
)


SELECT

    UUID(),

    b.Billing_ID,

    b.Patient_ID,

    CURRENT_DATE,

    p.Payment_Mode,

    CONCAT('TXN', FLOOR(RAND()*100000)),

    b.Final_Amount,

    'Completed',

    'Payment completed successfully'


FROM Billing b


JOIN
(
    SELECT 'UPI' AS Payment_Mode

    UNION ALL

    SELECT 'Credit Card'

    UNION ALL

    SELECT 'Insurance'

) p

LIMIT 20;



SELECT COUNT(*) AS Total_Payments
FROM Payments;

-- ==========================================================
-- Seed Patient_Health_Score Table
-- ==========================================================


DELETE FROM Patient_Health_Score;



INSERT INTO Patient_Health_Score
(
    Health_Score_ID,
    Patient_ID,
    Risk_Level,
    Health_Score,
    Calculation_Date,
    Factors_Considered,
    Remarks
)


SELECT

    UUID(),

    p.Patient_ID,

    r.Risk_Level,

    r.Score,

    CURRENT_DATE,

    'Vitals, diagnosis, medication history',

    'AI generated patient health assessment'


FROM Patients p


JOIN
(
    SELECT

        'Low' AS Risk_Level,

        85 AS Score


    UNION ALL


    SELECT

        'Medium',

        65


    UNION ALL


    SELECT

        'High',

        40

) r

LIMIT 15;



SELECT COUNT(*) AS Total_Health_Scores
FROM Patient_Health_Score;

-- ==========================================================
-- Seed Model_Training_Datasets Table
-- ==========================================================


DELETE FROM Model_Training_Datasets;



INSERT INTO Model_Training_Datasets
(
    Dataset_ID,
    Dataset_Name,
    Dataset_Version,
    Dataset_Type,
    Source_Name,
    Source_Type,
    Number_Of_Records,
    Number_Of_Features,
    Target_Column,
    Feature_List,
    Missing_Value_Percentage,
    Duplicate_Record_Count,
    Data_Quality_Score,
    Preprocessing_Method,
    Feature_Engineering_Method,
    Normalization_Method,
    Encoding_Method,
    Train_Test_Split_Ratio,
    Storage_Path,
    File_Format,
    Used_For_Model,
    Model_Version,
    Dataset_Purpose,
    Dataset_Status,
    Prepared_By,
    Approval_Status,
    Created_Date
)

VALUES

(
    UUID(),
    'Hybrid Healthcare Clinical Dataset',
    'v1.0',
    'Hybrid',
    'MIMIC-IV + Synthetic Healthcare Data',
    'Hybrid',
    10000,
    45,
    'Disease_Risk_Level',
    'Age, Gender, Vitals, Diagnosis, Lab Results, Medication History',
    2.5,
    25,
    96.5,
    'Missing value handling and normalization',
    'Feature scaling and clinical feature extraction',
    'Standard Scaling',
    'Label Encoding',
    '80:20',
    '/data/processed/hybrid_healthcare_dataset.csv',
    'CSV',
    'Disease Risk Prediction Model',
    'Model_v1',
    'Training dataset for AI clinical decision support',
    'Active',
    'Diya Lodha',
    'Approved',
    CURRENT_DATE
);



SELECT COUNT(*) AS Total_Datasets
FROM Model_Training_Datasets;

-- ==========================================================
-- Seed Model_Performance_Log Table
-- ==========================================================


DELETE FROM Model_Performance_Log;



INSERT INTO Model_Performance_Log
(
    Performance_Log_ID,
    Dataset_ID,
    Model_Name,
    Model_Version,
    Algorithm,
    Training_Date,
    Accuracy,
    Precision_Score,
    Recall_Score,
    F1_Score,
    ROC_AUC,
    Training_Time_Seconds,
    Validation_Method,
    Model_Status,
    Notes
)


SELECT

    UUID(),

    Dataset_ID,

    'Disease Risk Prediction Model',

    'v1.0',

    'Random Forest Classifier',

    CURRENT_TIMESTAMP,

    0.94,

    0.93,

    0.92,

    0.92,

    0.96,

    245.50,

    'Train-Test Split',

    'Production',

    'Model deployed for clinical risk prediction'


FROM Model_Training_Datasets;



SELECT COUNT(*) AS Total_Model_Logs
FROM Model_Performance_Log;

-- ==========================================================
-- Seed Prediction_Sessions Table
-- ==========================================================


DELETE FROM Prediction_Sessions;



INSERT INTO Prediction_Sessions
(
    Prediction_Session_ID,
    Patient_ID,
    Model_ID,
    Prediction_Date,
    Input_Features,
    Prediction_Result,
    Confidence_Score,
    Risk_Level,
    Status
)


SELECT

    UUID(),

    p.Patient_ID,

    NULL,

    CURRENT_TIMESTAMP,

    'Age,Vitals,Diagnosis,Lab Results',

    'Diabetes Risk Detected',

    0.89,

    'Medium',

    'Completed'


FROM Patients p

LIMIT 10;



SELECT COUNT(*) AS Total_Predictions
FROM Prediction_Sessions;

-- ==========================================================
-- Seed Disease_Risk_Predictions
-- ==========================================================

DELETE FROM Disease_Risk_Predictions;

INSERT INTO Disease_Risk_Predictions
(
    Prediction_ID,
    Patient_ID,
    Disease_ID,
    Prediction_Date,
    Risk_Level,
    Probability_Score,
    Model_Name,
    Prediction_Status,
    Notes
)

SELECT

    UUID(),

    p.Patient_ID,

    d.Disease_ID,

    CURRENT_TIMESTAMP,

    'Medium',

    0.84,

    'Disease Risk Prediction Model',

    'Completed',

    'AI generated prediction'

FROM Patients p

JOIN Diseases d

LIMIT 10;



SELECT COUNT(*) FROM Disease_Risk_Predictions;

-- ==========================================================
-- Seed Explainable_AI_Results
-- ==========================================================

DELETE FROM Explainable_AI_Results;

INSERT INTO Explainable_AI_Results
(
    Explanation_ID,
    Prediction_ID,
    Explanation_Method,
    Important_Features,
    Explanation_Text,
    Generated_At
)

SELECT

    UUID(),

    Prediction_ID,

    'SHAP',

    'Age, Blood Pressure, Blood Glucose',

    'Blood glucose and age contributed most to prediction.',

    CURRENT_TIMESTAMP

FROM Disease_Risk_Predictions;



SELECT COUNT(*) FROM Explainable_AI_Results;

-- ==========================================================
-- Seed Clinical_Decision_Recommendations
-- ==========================================================

DELETE FROM Clinical_Decision_Recommendations;

INSERT INTO Clinical_Decision_Recommendations
(
    Recommendation_ID,
    Patient_ID,
    Prediction_ID,
    Recommendation_Text,
    Recommendation_Type,
    Priority_Level,
    Recommendation_Status,
    Generated_Date
)

SELECT

    UUID(),

    dr.Patient_ID,

    dr.Prediction_ID,

    'Recommend lifestyle modification and quarterly monitoring.',

    'Preventive',

    'Medium',

    'Pending',

    CURRENT_DATE

FROM Disease_Risk_Predictions dr;



SELECT COUNT(*) FROM Clinical_Decision_Recommendations;

-- ==========================================================
-- Seed AI_Feedback
-- ==========================================================

DELETE FROM AI_Feedback;

INSERT INTO AI_Feedback
(
    Feedback_ID,
    Prediction_ID,
    Doctor_ID,
    Feedback_Rating,
    Feedback_Text,
    Submitted_Date
)

SELECT

    UUID(),

    dr.Prediction_ID,

    d.Doctor_ID,

    5,

    'Prediction aligns with clinical diagnosis.',

    CURRENT_DATE

FROM Disease_Risk_Predictions dr

JOIN Doctors d

LIMIT 10;



SELECT COUNT(*) FROM AI_Feedback;

-- ==========================================================
-- Seed AI_Model_History
-- ==========================================================

DELETE FROM AI_Model_History;

INSERT INTO AI_Model_History
(
    History_ID,
    Model_Name,
    Model_Version,
    Algorithm,
    Accuracy,
    Deployment_Date,
    Status,
    Notes
)

VALUES
(
    UUID(),
    'Disease Risk Prediction Model',
    'v1.0',
    'Random Forest',
    0.94,
    CURRENT_DATE,
    'Active',
    'Initial production deployment'
);



SELECT COUNT(*) FROM AI_Model_History;
