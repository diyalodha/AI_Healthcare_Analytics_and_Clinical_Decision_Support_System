import csv
import os
import mysql.connector
from collections import Counter

CSV_FILE = r"datasets\synthetic\medical_procedures.csv"

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ["MYSQL_PASSWORD"],
    database="healthcare_ai_db"
)

cursor = conn.cursor()

# Load database reference IDs
cursor.execute("SELECT Patient_ID FROM patients")
patients = {row[0] for row in cursor.fetchall()}

cursor.execute("""
    SELECT Admission_ID, Patient_ID, Department_ID, Admitting_Doctor_ID
    FROM admissions
""")
admissions = {
    row[0]: {
        "patient": row[1],
        "department": row[2],
        "doctor": row[3]
    }
    for row in cursor.fetchall()
}

cursor.execute("SELECT Doctor_ID, Department_ID FROM doctors")
doctors = {
    row[0]: row[1]
    for row in cursor.fetchall()
}

cursor.execute("SELECT Department_ID FROM departments")
departments = {row[0] for row in cursor.fetchall()}

# Counters
total = 0
valid_patient = 0
valid_admission = 0
valid_doctor = 0
valid_department = 0

admission_patient_match = 0
admission_doctor_match = 0
admission_department_match = 0
doctor_department_match = 0

statuses = Counter()
types = Counter()
names = Counter()

print("=" * 70)
print("STEP 62A - PROCEDURE SOURCE CONSISTENCY CHECK")
print("=" * 70)

with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        total += 1

        patient_id = row["Patient_ID"].strip()
        admission_id = row["Admission_ID"].strip()
        doctor_id = row["Doctor_ID"].strip()
        department_id = row["Department_ID"].strip()

        if patient_id in patients:
            valid_patient += 1

        if admission_id in admissions:
            valid_admission += 1

        if doctor_id in doctors:
            valid_doctor += 1

        if department_id in departments:
            valid_department += 1

        if admission_id in admissions:

            admission = admissions[admission_id]

            if admission["patient"] == patient_id:
                admission_patient_match += 1

            if admission["doctor"] == doctor_id:
                admission_doctor_match += 1

            if admission["department"] == department_id:
                admission_department_match += 1

        if doctor_id in doctors:
            if doctors[doctor_id] == department_id:
                doctor_department_match += 1

        statuses[row["Procedure_Status"]] += 1
        types[row["Procedure_Type"]] += 1
        names[row["Procedure_Name"]] += 1

print("\nSOURCE")
print("-" * 70)
print(f"CSV rows:                         {total:,}")

print("\nID VALIDATION")
print("-" * 70)
print(f"Valid Patient_ID:                 {valid_patient:,}")
print(f"Valid Admission_ID:               {valid_admission:,}")
print(f"Valid Doctor_ID:                  {valid_doctor:,}")
print(f"Valid Department_ID:              {valid_department:,}")

print("\nRELATIONSHIP VALIDATION")
print("-" * 70)
print(f"Admission -> Patient matches:     {admission_patient_match:,}")
print(f"Admission -> Doctor matches:      {admission_doctor_match:,}")
print(f"Admission -> Department matches:  {admission_department_match:,}")
print(f"Doctor -> Department matches:     {doctor_department_match:,}")

print("\nPROCEDURE STATUS")
print("-" * 70)
for key, value in statuses.items():
    print(f"{key}: {value:,}")

print("\nPROCEDURE TYPES")
print("-" * 70)
for key, value in types.items():
    print(f"{key}: {value:,}")

print("\nPROCEDURE NAMES")
print("-" * 70)
print(f"Unique procedure names:            {len(names):,}")

for name, count in names.most_common(15):
    print(f"{name}: {count:,}")

cursor.close()
conn.close()

print("\n" + "=" * 70)
print("CHECK COMPLETE")
print("=" * 70)