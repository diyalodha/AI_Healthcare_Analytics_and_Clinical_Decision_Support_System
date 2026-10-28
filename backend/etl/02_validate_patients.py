import os
import mysql.connector
from mysql.connector import Error


# ============================================================
# CONFIGURATION
# ============================================================

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD")
DB_NAME = "healthcare_ai_db"


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("        PATIENT TABLE VALIDATION")
print("=" * 70)


# ============================================================
# DATABASE CONNECTION
# ============================================================

try:

    connection = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    print("MySQL connection successful.")

except Error as e:

    print("ERROR connecting to MySQL:")
    print(e)

    raise SystemExit(1)


cursor = connection.cursor()


# ============================================================
# 1. TOTAL PATIENTS
# ============================================================

cursor.execute("""
    SELECT COUNT(*)
    FROM patients
""")

total_patients = cursor.fetchone()[0]

print("\n1. TOTAL PATIENTS")
print("-" * 70)
print(f"Total patients: {total_patients:,}")


# ============================================================
# 2. UNIQUE PATIENT IDs
# ============================================================

cursor.execute("""
    SELECT COUNT(DISTINCT Patient_ID)
    FROM patients
""")

unique_patient_ids = cursor.fetchone()[0]

print("\n2. UNIQUE PATIENT IDs")
print("-" * 70)
print(f"Unique Patient IDs: {unique_patient_ids:,}")


# ============================================================
# 3. NULL PRIMARY KEYS
# ============================================================

cursor.execute("""
    SELECT COUNT(*)
    FROM patients
    WHERE Patient_ID IS NULL
""")

null_patient_ids = cursor.fetchone()[0]

print("\n3. NULL PATIENT IDs")
print("-" * 70)
print(f"NULL Patient IDs: {null_patient_ids:,}")


# ============================================================
# 4. REQUIRED FIELD CHECK
# ============================================================

cursor.execute("""
    SELECT COUNT(*)
    FROM patients
    WHERE First_Name IS NULL
       OR Last_Name IS NULL
       OR Date_of_Birth IS NULL
       OR Gender IS NULL
       OR Registration_Date IS NULL
""")

missing_required = cursor.fetchone()[0]

print("\n4. REQUIRED FIELD CHECK")
print("-" * 70)
print(f"Patients missing required fields: {missing_required:,}")


# ============================================================
# 5. PHONE DUPLICATES
# ============================================================

cursor.execute("""
    SELECT Phone, COUNT(*)
    FROM patients
    WHERE Phone IS NOT NULL
    GROUP BY Phone
    HAVING COUNT(*) > 1
""")

duplicate_phones = cursor.fetchall()

print("\n5. PHONE DUPLICATE CHECK")
print("-" * 70)
print(f"Duplicate phone numbers: {len(duplicate_phones):,}")


# ============================================================
# 6. INVALID BMI
# ============================================================

cursor.execute("""
    SELECT COUNT(*)
    FROM patients
    WHERE BMI IS NOT NULL
      AND (BMI <= 0 OR BMI > 100)
""")

invalid_bmi = cursor.fetchone()[0]

print("\n6. BMI VALIDATION")
print("-" * 70)
print(f"Invalid BMI values: {invalid_bmi:,}")


# ============================================================
# 7. INVALID HEIGHT
# ============================================================

cursor.execute("""
    SELECT COUNT(*)
    FROM patients
    WHERE Height_cm IS NOT NULL
      AND (Height_cm < 30 OR Height_cm > 250)
""")

invalid_height = cursor.fetchone()[0]

print("\n7. HEIGHT VALIDATION")
print("-" * 70)
print(f"Invalid height values: {invalid_height:,}")


# ============================================================
# 8. INVALID WEIGHT
# ============================================================

cursor.execute("""
    SELECT COUNT(*)
    FROM patients
    WHERE Weight_kg IS NOT NULL
      AND (Weight_kg < 2 OR Weight_kg > 300)
""")

invalid_weight = cursor.fetchone()[0]

print("\n8. WEIGHT VALIDATION")
print("-" * 70)
print(f"Invalid weight values: {invalid_weight:,}")


# ============================================================
# 9. GENDER DISTRIBUTION
# ============================================================

cursor.execute("""
    SELECT Gender, COUNT(*)
    FROM patients
    GROUP BY Gender
    ORDER BY Gender
""")

gender_distribution = cursor.fetchall()

print("\n9. GENDER DISTRIBUTION")
print("-" * 70)

for gender, count in gender_distribution:
    print(f"{gender}: {count:,}")


# ============================================================
# 10. STATUS DISTRIBUTION
# ============================================================

cursor.execute("""
    SELECT Status, COUNT(*)
    FROM patients
    GROUP BY Status
    ORDER BY Status
""")

status_distribution = cursor.fetchall()

print("\n10. PATIENT STATUS DISTRIBUTION")
print("-" * 70)

for status, count in status_distribution:
    print(f"{status}: {count:,}")


# ============================================================
# 11. BLOOD GROUP DISTRIBUTION
# ============================================================

cursor.execute("""
    SELECT Blood_Group, COUNT(*)
    FROM patients
    GROUP BY Blood_Group
    ORDER BY Blood_Group
""")

blood_groups = cursor.fetchall()

print("\n11. BLOOD GROUP DISTRIBUTION")
print("-" * 70)

for blood_group, count in blood_groups:
    print(f"{blood_group}: {count:,}")


# ============================================================
# FINAL VALIDATION STATUS
# ============================================================

print("\n" + "=" * 70)
print("FINAL VALIDATION SUMMARY")
print("=" * 70)

checks_passed = True

if total_patients != 100000:
    checks_passed = False

if unique_patient_ids != total_patients:
    checks_passed = False

if null_patient_ids != 0:
    checks_passed = False

if missing_required != 0:
    checks_passed = False

if len(duplicate_phones) != 0:
    checks_passed = False

if invalid_bmi != 0:
    checks_passed = False

if invalid_height != 0:
    checks_passed = False

if invalid_weight != 0:
    checks_passed = False


if checks_passed:

    print("STATUS: PASSED")
    print("Patient table is ready for mapping ETL.")

else:

    print("STATUS: REVIEW REQUIRED")
    print("One or more validation checks failed.")


print("=" * 70)


# ============================================================
# CLEANUP
# ============================================================

cursor.close()
connection.close()

print("\nDatabase connection closed.")
print("Patient validation finished.")