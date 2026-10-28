
import csv
import hashlib
import os
import sys
from datetime import date, datetime
from getpass import getpass
from pathlib import Path

import mysql.connector


ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "datasets" / "synthetic" / "discharge_summary.csv"
REJECT_PATH = ROOT / "backend" / "etl" / "67_discharge_summaries_rejected.csv"

CHUNK_SIZE = 5000

ALLOWED_STATUSES = {"Recovered", "Improved", "Referred", "Expired"}
CONDITION_TO_STATUS = {
    "Stable": "NotSpecified",
    "Critical": "NotSpecified",
    "Improved": "Improved",
    "Referred": "Referred",
}
ALLOWED_RISKS = {"Low", "Medium", "High", "Critical"}


def clean(value):
    return (value or "").strip()


def parse_date(value):
    value = clean(value)
    if not value:
        return None

    try:
        return date.fromisoformat(value[:10])
    except (ValueError, TypeError):
        return None


def normalize_mysql_date(value):
    """Convert MySQL DATE or DATETIME values to Python date."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return parse_date(value)
    return None


def make_number(source_id):
    digest = hashlib.sha256(source_id.encode("utf-8")).hexdigest()[:24]
    return f"DS-{digest}"


def reject_row(writer, row, reason):
    output = dict(row)
    output["Reject_Reason"] = reason
    writer.writerow(output)


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Source CSV not found: {CSV_PATH}")

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
        patients = {str(row[0]) for row in cur.fetchall()}

        cur.execute("SELECT Doctor_ID FROM doctors")
        doctors = {str(row[0]) for row in cur.fetchall()}

        cur.execute(
            "SELECT Admission_ID, Patient_ID, Admission_Date FROM admissions"
        )
        admissions = {
            str(admission_id): (
                str(patient_id),
                normalize_mysql_date(admission_date),
            )
            for admission_id, patient_id, admission_date in cur.fetchall()
        }

        # Source IDs are stored in Created_By so resume checks remain stable.
        # The value is kept short enough for the destination VARCHAR(50).
        cur.execute("""
            SELECT Created_By
            FROM discharge_summary
            WHERE Created_By LIKE 'SRC:%'
        """)
        imported_source_ids = {
            value[4:] for (value,) in cur.fetchall() if value
        }

        print(f"Patients available: {len(patients):,}")
        print(f"Doctors available: {len(doctors):,}")
        print(f"Admissions available: {len(admissions):,}")
        print(f"Previously imported source IDs: {len(imported_source_ids):,}")

        with CSV_PATH.open(
            "r", encoding="utf-8-sig", newline=""
        ) as source, REJECT_PATH.open(
            "w", encoding="utf-8-sig", newline=""
        ) as reject_file:

            reader = csv.DictReader(source)
            fieldnames = list(reader.fieldnames or []) + ["Reject_Reason"]

            reject_writer = csv.DictWriter(
                reject_file,
                fieldnames=fieldnames,
                extrasaction="ignore",
            )
            reject_writer.writeheader()

            for row in reader:
                source_id = clean(row.get("Discharge_Summary_ID"))
                patient_id = clean(row.get("Patient_ID"))
                admission_id = clean(row.get("Admission_ID"))
                doctor_id = clean(row.get("Doctor_ID"))
                diagnosis = clean(row.get("Final_Diagnosis"))
                condition = clean(row.get("Discharge_Condition"))
                risk = clean(row.get("Readmission_Risk"))

                if not source_id:
                    reject_row(reject_writer, row, "Missing Discharge_Summary_ID")
                    rejected += 1
                    continue

                if source_id in imported_source_ids:
                    skipped += 1
                    continue

                if not patient_id or patient_id not in patients:
                    reject_row(reject_writer, row, "Patient_ID missing or not found")
                    rejected += 1
                    continue

                if not admission_id or admission_id not in admissions:
                    reject_row(reject_writer, row, "Admission_ID missing or not found")
                    rejected += 1
                    continue

                admission_patient_id, admission_date = admissions[admission_id]

                if admission_patient_id != patient_id:
                    reject_row(
                        reject_writer,
                        row,
                        "Admission belongs to a different patient",
                    )
                    rejected += 1
                    continue

                if not diagnosis:
                    reject_row(reject_writer, row, "Final_Diagnosis is missing")
                    rejected += 1
                    continue

                # Preserve the source condition; map it separately to a valid database status.
                if condition not in CONDITION_TO_STATUS:
                    reject_row(
                        reject_writer,
                        row,
                        f"No approved status mapping for condition: {condition}",
                    )
                    rejected += 1
                    continue

                discharge_status = CONDITION_TO_STATUS[condition]

                if risk and risk not in ALLOWED_RISKS:
                    reject_row(
                        reject_writer,
                        row,
                        f"Unsupported Readmission_Risk: {risk}",
                    )
                    rejected += 1
                    continue

                discharge_date = parse_date(row.get("Discharge_Date"))
                if discharge_date is None:
                    reject_row(
                        reject_writer,
                        row,
                        "Discharge_Date is missing or invalid",
                    )
                    rejected += 1
                    continue

                if admission_date and discharge_date < admission_date:
                    reject_row(
                        reject_writer,
                        row,
                        "Discharge_Date is earlier than Admission_Date",
                    )
                    rejected += 1
                    continue

                # Doctor is optional in the destination schema.
                # Do not attach an unknown doctor ID.
                if not doctor_id or doctor_id not in doctors:
                    doctor_id = None

                discharge_number = make_number(source_id)
                length_of_stay = (
                    (discharge_date - admission_date).days
                    if admission_date is not None
                    else None
                )

                batch.append((
                    admission_id,
                    patient_id,
                    doctor_id,
                    discharge_number,
                    admission_date,
                    discharge_date,
                    length_of_stay,
                    diagnosis,
                    clean(row.get("Hospital_Course")) or None,
                    clean(row.get("Follow_Up_Instructions")) or None,
                    condition,
                    discharge_status,
                    risk or "Low",
                    "Synthetic",
                    1,
                    1,
                    f"SRC:{source_id}",
                ))

                imported_source_ids.add(source_id)

                if len(batch) >= CHUNK_SIZE:
                    cur.executemany("""
                        INSERT INTO discharge_summary (
                            Admission_ID,
                            Patient_ID,
                            Doctor_ID,
                            Discharge_Number,
                            Admission_Date,
                            Discharge_Date,
                            Length_Of_Stay_Days,
                            Final_Diagnosis,
                            Treatment_Provided,
                            Follow_Up_Instructions,
                            Condition_At_Discharge,
                            Discharge_Status,
                            Readmission_Risk_Level,
                            Data_Source,
                            Is_Active,
                            Record_Version,
                            Created_By
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """, batch)
                    conn.commit()
                    inserted += len(batch)
                    batch.clear()
                    print(f"Inserted this run: {inserted:,}")

            if batch:
                cur.executemany("""
                    INSERT INTO discharge_summary (
                        Admission_ID,
                        Patient_ID,
                        Doctor_ID,
                        Discharge_Number,
                        Admission_Date,
                        Discharge_Date,
                        Length_Of_Stay_Days,
                        Final_Diagnosis,
                        Treatment_Provided,
                        Follow_Up_Instructions,
                        Condition_At_Discharge,
                        Discharge_Status,
                        Readmission_Risk_Level,
                        Data_Source,
                        Is_Active,
                        Record_Version,
                        Created_By
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, batch)
                conn.commit()
                inserted += len(batch)
                batch.clear()

        cur.execute("SELECT COUNT(*) FROM discharge_summary")
        total_rows = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*)
            FROM discharge_summary
            WHERE Data_Source = 'Synthetic'
        """)
        synthetic_rows = cur.fetchone()[0]

        print("\n========== DISCHARGE SUMMARY LOAD FINISHED ==========")
        print(f"Inserted this run: {inserted:,}")
        print(f"Already imported/skipped: {skipped:,}")
        print(f"Rejected source rows: {rejected:,}")
        print(f"Total discharge_summary rows: {total_rows:,}")
        print(f"Synthetic discharge summary rows: {synthetic_rows:,}")
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
