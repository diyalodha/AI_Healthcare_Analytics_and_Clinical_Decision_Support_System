USE healthcare_ai_db;

-- 1. Patient demographics and health indicators
CREATE OR REPLACE VIEW vw_patient_demographics AS
SELECT
    Gender,
    CASE
        WHEN Date_of_Birth IS NULL THEN 'Unknown'
        WHEN TIMESTAMPDIFF(YEAR, Date_of_Birth, CURDATE()) < 18 THEN 'Under 18'
        WHEN TIMESTAMPDIFF(YEAR, Date_of_Birth, CURDATE()) < 36 THEN '18-35'
        WHEN TIMESTAMPDIFF(YEAR, Date_of_Birth, CURDATE()) < 51 THEN '36-50'
        WHEN TIMESTAMPDIFF(YEAR, Date_of_Birth, CURDATE()) < 66 THEN '51-65'
        ELSE '66+'
    END AS Age_Group,
    COUNT(*) AS Patient_Count,
    ROUND(AVG(BMI), 2) AS Average_BMI,
    ROUND(AVG(Latest_Health_Score), 2) AS Average_Health_Score
FROM patients
WHERE COALESCE(Is_Deleted, 0) = 0
GROUP BY Gender, Age_Group;

-- 2. Disease trends by diagnosis month
CREATE OR REPLACE VIEW vw_disease_trends AS
SELECT
    DATE_FORMAT(d.Diagnosis_Date, '%Y-%m') AS Diagnosis_Month,
    ds.Disease_ID,
    ds.Disease_Name,
    ds.Disease_Category,
    COUNT(*) AS Diagnosis_Count,
    SUM(CASE WHEN d.Is_Primary_Diagnosis = 1 THEN 1 ELSE 0 END)
        AS Primary_Diagnosis_Count
FROM diagnoses d
JOIN diseases ds ON ds.Disease_ID = d.Disease_ID
WHERE COALESCE(d.Is_Deleted, 0) = 0
GROUP BY
    DATE_FORMAT(d.Diagnosis_Date, '%Y-%m'),
    ds.Disease_ID,
    ds.Disease_Name,
    ds.Disease_Category;

-- 3. Hospital admission summaries
CREATE OR REPLACE VIEW vw_admission_summary AS
SELECT
    DATE_FORMAT(Admission_Date, '%Y-%m') AS Admission_Month,
    Admission_Type,
    Current_Status,
    COUNT(*) AS Admission_Count,
    ROUND(AVG(Length_of_Stay), 2) AS Average_Length_of_Stay,
    SUM(CASE WHEN Is_Emergency = 1 THEN 1 ELSE 0 END)
        AS Emergency_Admissions,
    SUM(CASE WHEN Is_ICU_Admission = 1 THEN 1 ELSE 0 END)
        AS ICU_Admissions
FROM admissions
WHERE COALESCE(Is_Deleted, 0) = 0
GROUP BY
    DATE_FORMAT(Admission_Date, '%Y-%m'),
    Admission_Type,
    Current_Status;

-- 4. Laboratory results flagged as abnormal
CREATE OR REPLACE VIEW vw_abnormal_lab_results AS
SELECT
    Lab_Result_ID,
    Patient_ID,
    Lab_Test_ID,
    Diagnosis_ID,
    Admission_ID,
    Test_Date,
    Result_Category,
    Result_Value,
    Numeric_Result_Value,
    Unit,
    Reference_Min_Value,
    Reference_Max_Value,
    Result_Status,
    Abnormal_Flag,
    Severity_Score,
    AI_Risk_Category
FROM lab_results
WHERE Abnormal_Flag = 1
  AND COALESCE(Is_Deleted, 0) = 0;

-- 5. AI prediction summaries
CREATE OR REPLACE VIEW vw_ai_prediction_summary AS
SELECT
    Prediction_Type,
    Risk_Level,
    Prediction_Status,
    COUNT(*) AS Prediction_Count,
    ROUND(AVG(Prediction_Score), 4) AS Average_Prediction_Score,
    ROUND(AVG(Confidence_Score), 4) AS Average_Confidence_Score
FROM prediction_sessions
WHERE COALESCE(Is_Deleted, 0) = 0
GROUP BY Prediction_Type, Risk_Level, Prediction_Status;

-- 6. AI recommendation summaries
CREATE OR REPLACE VIEW vw_ai_recommendation_summary AS
SELECT
    Recommendation_Type,
    Priority_Level,
    Doctor_Approval_Status,
    Recommendation_Status,
    COUNT(*) AS Recommendation_Count,
    ROUND(AVG(AI_Confidence_Score), 2) AS Average_AI_Confidence
FROM clinical_decision_recommendations
WHERE COALESCE(Is_Deleted, 0) = 0
GROUP BY
    Recommendation_Type,
    Priority_Level,
    Doctor_Approval_Status,
    Recommendation_Status;
