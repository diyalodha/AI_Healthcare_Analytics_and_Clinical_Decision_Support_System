# Healthcare Database Design

## Database Name
healthcare_ai_db

---

# Table 1: Patients

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| Patient_ID | VARCHAR(10) | Unique patient identifier |
| First_Name | VARCHAR(50) | Patient first name |
| Last_Name | VARCHAR(50) | Patient last name |
| Date_of_Birth | DATE | Date of birth |
| Age | INT | Current age |
| Gender | VARCHAR(10) | Male / Female / Other |
| Blood_Group | VARCHAR(5) | Blood group |
| Height_cm | DECIMAL(5,2) | Height in centimeters |
| Weight_kg | DECIMAL(5,2) | Weight in kilograms |
| BMI | DECIMAL(4,2) | Body Mass Index |
| Phone | VARCHAR(15) | Contact number |
| Email | VARCHAR(100) | Email address |
| City | VARCHAR(100) | City |
| State | VARCHAR(100) | State |
| Country | VARCHAR(100) | Country |
| Occupation | VARCHAR(100) | Occupation |
| Marital_Status | VARCHAR(20) | Marital status |
| Smoking_Status | VARCHAR(20) | Never / Former / Current |
| Alcohol_Consumption | VARCHAR(20) | Never / Occasional / Regular |
| Physical_Activity | VARCHAR(20) | Low / Moderate / High |
| Family_History | BOOLEAN | Family history of chronic diseases |
| Registration_Date | DATE | First registration date |