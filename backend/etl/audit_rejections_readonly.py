import csv
import os
from pathlib import Path
import getpass
import mysql.connector

ROOT = Path(__file__).resolve().parents[2]
ETL = ROOT / "backend" / "etl"
DATA = ROOT / "datasets" / "synthetic"

def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def clean(value):
    return str(value).strip() if value is not None else ""

password = os.environ.get("MYSQL_PASSWORD")
if not password:
    password = getpass.getpass("MySQL password: ")

conn = mysql.connector.connect(
    host=os.environ.get("MYSQL_HOST", "localhost"),
    port=int(os.environ.get("MYSQL_PORT", "3306")),
    user=os.environ.get("MYSQL_USER", "root"),
    password=password,
    database="healthcare_ai_db",
    charset="utf8mb4",
)

try:
    cur = conn.cursor()

    cur.execute("SELECT Patient_ID FROM patients")
    patients = {clean(r[0]) for r in cur.fetchall()}

    cur.execute("SELECT Doctor_ID FROM doctors")
    doctors = {clean(r[0]) for r in cur.fetchall()}

    cur.execute("SELECT Admission_ID, Patient_ID FROM admissions")
    admissions = {
        clean(aid): clean(pid)
        for aid, pid in cur.fetchall()
    }

    print("\n========== DATABASE LOOKUP COUNTS ==========")
    print(f"Patients:   {len(patients):,}")
    print(f"Doctors:    {len(doctors):,}")
    print(f"Admissions: {len(admissions):,}")

    # Clinical notes: rejected file has note IDs, so recover
    # Doctor_ID and Patient_ID from the original source CSV.
    note_source = {
        clean(r.get("Clinical_Note_ID")): r
        for r in read_csv(DATA / "clinical_notes.csv")
    }
    note_rejects = read_csv(ETL / "66_clinical_notes_rejected.csv")

    missing_note_source = 0
    note_doctor_missing = 0
    note_patient_missing = 0
    note_admission_missing = 0
    note_admission_patient_mismatch = 0

    for rejected in note_rejects:
        note_id = clean(rejected.get("Clinical_Note_ID"))
        row = note_source.get(note_id)

        if row is None:
            missing_note_source += 1
            continue

        doctor_id = clean(row.get("Doctor_ID"))
        patient_id = clean(row.get("Patient_ID"))
        admission_id = clean(row.get("Admission_ID"))

        if not doctor_id or doctor_id not in doctors:
            note_doctor_missing += 1
        if not patient_id or patient_id not in patients:
            note_patient_missing += 1
        if admission_id and admission_id not in admissions:
            note_admission_missing += 1
        elif admission_id and admission_id in admissions:
            if admissions[admission_id] != patient_id:
                note_admission_patient_mismatch += 1

    print("\n========== CLINICAL NOTES ==========")
    print(f"Rejected rows audited: {len(note_rejects):,}")
    print(f"Note IDs absent from source CSV: {missing_note_source:,}")
    print(f"Doctor_ID missing from MySQL doctors: {note_doctor_missing:,}")
    print(f"Patient_ID missing from MySQL patients: {note_patient_missing:,}")
    print(f"Admission_ID missing from MySQL admissions: {note_admission_missing:,}")
    print(f"Admission belongs to another patient: {note_admission_patient_mismatch:,}")

    # Discharge summaries
    discharge_rows = read_csv(ETL / "67_discharge_summaries_rejected.csv")
    discharge_patient_missing = 0
    discharge_admission_missing = 0
    discharge_patient_mismatch = 0
    discharge_doctor_missing = 0

    for row in discharge_rows:
        pid = clean(row.get("Patient_ID"))
        aid = clean(row.get("Admission_ID"))
        did = clean(row.get("Doctor_ID"))

        if not pid or pid not in patients:
            discharge_patient_missing += 1
        if not did or did not in doctors:
            discharge_doctor_missing += 1
        if not aid or aid not in admissions:
            discharge_admission_missing += 1
        elif admissions[aid] != pid:
            discharge_patient_mismatch += 1

    print("\n========== DISCHARGE SUMMARIES ==========")
    print(f"Rejected rows audited: {len(discharge_rows):,}")
    print(f"Patient_ID missing from MySQL patients: {discharge_patient_missing:,}")
    print(f"Doctor_ID missing from MySQL doctors: {discharge_doctor_missing:,}")
    print(f"Admission_ID missing from MySQL admissions: {discharge_admission_missing:,}")
    print(f"Admission belongs to another patient: {discharge_patient_mismatch:,}")

    # ICU stays
    icu_rows = read_csv(ETL / "68_icu_stays_rejected.csv")
    icu_patient_missing = 0
    icu_admission_missing = 0
    icu_patient_mismatch = 0
    icu_doctor_missing = 0

    for row in icu_rows:
        pid = clean(row.get("Patient_ID"))
        aid = clean(row.get("Admission_ID"))
        did = clean(row.get("Doctor_ID"))

        if not pid or pid not in patients:
            icu_patient_missing += 1
        if not did or did not in doctors:
            icu_doctor_missing += 1
        if not aid or aid not in admissions:
            icu_admission_missing += 1
        elif admissions[aid] != pid:
            icu_patient_mismatch += 1

    print("\n========== ICU STAYS ==========")
    print(f"Rejected rows audited: {len(icu_rows):,}")
    print(f"Patient_ID missing from MySQL patients: {icu_patient_missing:,}")
    print(f"Doctor_ID missing from MySQL doctors: {icu_doctor_missing:,}")
    print(f"Admission_ID missing from MySQL admissions: {icu_admission_missing:,}")
    print(f"Admission belongs to another patient: {icu_patient_mismatch:,}")

    print("\nAudit completed. No database records were modified.")

finally:
    conn.close()
