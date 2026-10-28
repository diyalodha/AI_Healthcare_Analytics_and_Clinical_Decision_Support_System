
import csv
import hashlib
import os
import sys
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from getpass import getpass
from pathlib import Path

import mysql.connector


ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "datasets" / "synthetic" / "icu_stays.csv"
REJECT_PATH = ROOT / "backend" / "etl" / "68_icu_stays_rejected.csv"
CHUNK_SIZE = 2000

ICU_TYPES = {
    "Medical ICU": "Medical",
    "Surgical ICU": "Surgical",
    "Cardiac ICU": "Cardiac",
    "Neonatal ICU": "Neonatal",
    "Pediatric ICU": "Pediatric",
    "Trauma ICU": "Trauma",
}

OUTCOMES = {"Recovered", "Transferred", "Expired"}
RISK_LEVELS = {"Low", "Medium", "High", "Critical"}


def clean(value):
    return (value or "").strip()


def parse_datetime(value):
    value = clean(value)
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(
            tzinfo=None
        )
    except ValueError:
        try:
            return datetime.strptime(value[:10], "%Y-%m-%d")
        except ValueError:
            return None


def parse_bool(value):
    value = clean(value).lower()
    if value in {"true", "1", "yes"}:
        return 1
    if value in {"false", "0", "no"}:
        return 0
    return None


def parse_decimal(value):
    value = clean(value)
    if not value:
        return None
    try:
        result = Decimal(value)
        return result if result.is_finite() else None
    except InvalidOperation:
        return None


def stable_number(source_id):
    digest = hashlib.sha256(source_id.encode("utf-8")).hexdigest()[:24]
    return f"ICU-{digest}"


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

    password = os.environ.get("MYSQL_PASSWORD")
    if not password:
        password = getpass("MySQL password: ")

    conn = mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=password,
        database="healthcare_ai_db",
        charset="utf8mb4",
    )
    conn.autocommit = False

    inserted = 0
    skipped = 0
    rejected = 0
    batch = []

    try:
        cur = conn.cursor()

        cur.execute("SELECT Patient_ID FROM patients")
        patients = {str(r[0]) for r in cur.fetchall()}

        cur.execute("SELECT Doctor_ID FROM doctors")
        doctors = {str(r[0]) for r in cur.fetchall()}

        cur.execute("SELECT Admission_ID, Patient_ID FROM admissions")
        admissions = {
            str(admission_id): str(patient_id)
            for admission_id, patient_id in cur.fetchall()
        }

        cur.execute("""
            SELECT ICU_Stay_Number
            FROM icu_stay_details
            WHERE ICU_Stay_Number LIKE 'ICU-%'
        """)
        existing_numbers = {r[0] for r in cur.fetchall()}

        print(f"Patients available: {len(patients):,}")
        print(f"Doctors available: {len(doctors):,}")
        print(f"Admissions available: {len(admissions):,}")
        print(f"Existing generated ICU numbers: {len(existing_numbers):,}")

        with CSV_PATH.open(
            "r", encoding="utf-8-sig", newline=""
        ) as source, REJECT_PATH.open(
            "w", encoding="utf-8-sig", newline=""
        ) as reject_file:

            reader = csv.DictReader(source)
            reject_writer = csv.DictWriter(
                reject_file,
                fieldnames=list(reader.fieldnames or []) + ["Reject_Reason"],
                extrasaction="ignore",
            )
            reject_writer.writeheader()

            for row in reader:
                source_id = clean(row.get("ICU_Stay_ID"))
                patient_id = clean(row.get("Patient_ID"))
                admission_id = clean(row.get("Admission_ID"))
                doctor_id = clean(row.get("Doctor_ID"))

                if not source_id:
                    reason = "Missing ICU_Stay_ID"
                elif not patient_id or patient_id not in patients:
                    reason = "Patient_ID missing or not found"
                elif not admission_id or admission_id not in admissions:
                    reason = "Admission_ID missing or not found"
                elif admissions[admission_id] != patient_id:
                    reason = "Admission belongs to a different patient"
                else:
                    reason = None

                if reason:
                    reject_file_row = dict(row)
                    reject_file_row["Reject_Reason"] = reason
                    reject_writer.writerow(reject_file_row)
                    rejected += 1
                    continue

                stay_number = stable_number(source_id)
                if stay_number in existing_numbers:
                    skipped += 1
                    continue

                icu_type = ICU_TYPES.get(clean(row.get("ICU_Type")))
                if not icu_type:
                    reason = f"Unsupported ICU_Type: {clean(row.get('ICU_Type'))}"
                    reject_writer.writerow({**row, "Reject_Reason": reason})
                    rejected += 1
                    continue

                outcome = clean(row.get("Outcome"))
                if outcome not in OUTCOMES:
                    reject_writer.writerow({
                        **row,
                        "Reject_Reason": f"Unsupported Outcome: {outcome}",
                    })
                    rejected += 1
                    continue

                admission_dt = parse_datetime(row.get("ICU_Admission_Date"))
                discharge_dt = parse_datetime(row.get("ICU_Discharge_Date"))
                if admission_dt is None or discharge_dt is None:
                    reject_writer.writerow({
                        **row,
                        "Reject_Reason": "Invalid ICU admission/discharge datetime",
                    })
                    rejected += 1
                    continue

                if discharge_dt < admission_dt:
                    reject_writer.writerow({
                        **row,
                        "Reject_Reason": "ICU discharge is earlier than ICU admission",
                    })
                    rejected += 1
                    continue

                ventilator = parse_bool(row.get("Ventilator_Required"))
                if ventilator is None:
                    reject_writer.writerow({
                        **row,
                        "Reject_Reason": "Invalid Ventilator_Required value",
                    })
                    rejected += 1
                    continue

                severity = clean(row.get("Severity_Level"))
                # Do not infer a calibrated AI risk level from severity labels.
                # Leave AI_Risk_Level at its database default.
                length_days = parse_decimal(row.get("Length_of_Stay_Days"))
                if length_days is not None and length_days < 0:
                    length_days = None

                if not doctor_id or doctor_id not in doctors:
                    doctor_id = None

                batch.append((
                    admission_id,
                    patient_id,
                    doctor_id,
                    stay_number,
                    icu_type,
                    admission_dt,
                    discharge_dt,
                    length_days,
                    f"Synthetic source ICU_Stay_ID={source_id}; "
                    f"Severity_Level={severity or 'Unknown'}",
                    ventilator,
                    outcome,
                    "Synthetic",
                    1,
                    1,
                    f"SRC:{source_id}",
                ))
                existing_numbers.add(stay_number)

                if len(batch) >= CHUNK_SIZE:
                    cur.executemany("""
                        INSERT INTO icu_stay_details (
                            Admission_ID,
                            Patient_ID,
                            Doctor_ID,
                            ICU_Stay_Number,
                            ICU_Type,
                            Admission_DateTime,
                            Discharge_DateTime,
                            Length_Of_Stay_Days,
                            Admission_Reason,
                            Ventilator_Required,
                            ICU_Outcome,
                            Data_Source,
                            Is_Active,
                            Record_Version,
                            Created_By
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s
                        )
                    """, batch)
                    conn.commit()
                    inserted += len(batch)
                    batch.clear()
                    print(f"Inserted this run: {inserted:,}")

            if batch:
                cur.executemany("""
                    INSERT INTO icu_stay_details (
                        Admission_ID,
                        Patient_ID,
                        Doctor_ID,
                        ICU_Stay_Number,
                        ICU_Type,
                        Admission_DateTime,
                        Discharge_DateTime,
                        Length_Of_Stay_Days,
                        Admission_Reason,
                        Ventilator_Required,
                        ICU_Outcome,
                        Data_Source,
                        Is_Active,
                        Record_Version,
                        Created_By
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s
                    )
                """, batch)
                conn.commit()
                inserted += len(batch)

        cur.execute("SELECT COUNT(*) FROM icu_stay_details")
        total = cur.fetchone()[0]

        print("\n========== ICU STAYS LOAD FINISHED ==========")
        print(f"Inserted this run: {inserted:,}")
        print(f"Already imported/skipped: {skipped:,}")
        print(f"Rejected source rows: {rejected:,}")
        print(f"Total icu_stay_details rows: {total:,}")
        print(f"Reject report: {REJECT_PATH}")

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nERROR: {exc}")
        sys.exit(1)
