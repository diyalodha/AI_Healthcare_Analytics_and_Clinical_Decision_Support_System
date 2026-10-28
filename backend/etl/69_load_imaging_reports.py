
import csv
import hashlib
import os
import sys
from datetime import datetime
from getpass import getpass
from pathlib import Path

import mysql.connector


ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "datasets" / "synthetic" / "imaging_reports.csv"
REJECT_PATH = ROOT / "backend" / "etl" / "69_imaging_reports_rejected.csv"

BATCH_SIZE = 2000

ALLOWED_TYPES = {
    "X-Ray",
    "CT Scan",
    "MRI",
    "Ultrasound",
    "PET Scan",
    "Mammography",
    "ECG",
    "Echocardiography",
    "Other",
}

# The database does not support "Final".
# This is a schema-compatibility mapping, not proof of clinical verification.
STATUS_MAP = {
    "Final": "Completed",
    "Pending": "Pending",
    "Completed": "Completed",
    "Verified": "Verified",
    "Rejected": "Rejected",
}


def clean(value):
    return (value or "").strip()


def stable_report_number(source_id):
    digest = hashlib.sha256(
        source_id.encode("utf-8")
    ).hexdigest()[:24]
    return f"IMG-{digest}"


def parse_datetime(value):
    value = clean(value)
    if not value:
        return None

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.replace(tzinfo=None)
    except ValueError:
        try:
            return datetime.strptime(value[:10], "%Y-%m-%d")
        except ValueError:
            return None


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

    insert_sql = """
        INSERT INTO imaging_reports (
            Patient_ID,
            Doctor_ID,
            Admission_ID,
            Imaging_Report_Number,
            Imaging_Type,
            Body_Part,
            Imaging_Date,
            Clinical_Indication,
            Findings,
            Impression,
            Report_Status,
            Data_Source,
            Is_Active,
            Record_Version,
            Created_By
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
    """

    try:
        cur = conn.cursor()

        cur.execute("SELECT Patient_ID FROM patients")
        patients = {str(row[0]) for row in cur.fetchall()}

        cur.execute("SELECT Doctor_ID FROM doctors")
        doctors = {str(row[0]) for row in cur.fetchall()}

        cur.execute("SELECT Admission_ID, Patient_ID FROM admissions")
        admissions = {
            str(admission_id): str(patient_id)
            for admission_id, patient_id in cur.fetchall()
        }

        cur.execute("""
            SELECT Imaging_Report_Number
            FROM imaging_reports
            WHERE Imaging_Report_Number LIKE 'IMG-%'
        """)
        existing_numbers = {row[0] for row in cur.fetchall()}

        print(f"Patients available: {len(patients):,}")
        print(f"Doctors available: {len(doctors):,}")
        print(f"Admissions available: {len(admissions):,}")
        print(f"Existing generated report numbers: {len(existing_numbers):,}")

        with CSV_PATH.open(
            "r", encoding="utf-8-sig", newline=""
        ) as source, REJECT_PATH.open(
            "w", encoding="utf-8-sig", newline=""
        ) as reject_file:

            reader = csv.DictReader(source)

            required_columns = {
                "Imaging_Report_ID",
                "Patient_ID",
                "Admission_ID",
                "Radiology_Department_ID",
                "Doctor_ID",
                "Imaging_Type",
                "Body_Part",
                "Imaging_Date",
                "Findings",
                "Impression",
                "Report_Status",
            }

            missing_columns = required_columns - set(
                reader.fieldnames or []
            )
            if missing_columns:
                raise ValueError(
                    "CSV is missing required columns: "
                    + ", ".join(sorted(missing_columns))
                )

            reject_writer = csv.DictWriter(
                reject_file,
                fieldnames=list(reader.fieldnames) + ["Reject_Reason"],
                extrasaction="ignore",
            )
            reject_writer.writeheader()

            def reject(row, reason):
                nonlocal rejected
                reject_writer.writerow({
                    **row,
                    "Reject_Reason": reason,
                })
                rejected += 1

            for row in reader:
                source_id = clean(row.get("Imaging_Report_ID"))
                patient_id = clean(row.get("Patient_ID"))
                doctor_id = clean(row.get("Doctor_ID"))
                admission_id = clean(row.get("Admission_ID"))

                if not source_id:
                    reject(row, "Missing Imaging_Report_ID")
                    continue

                report_number = stable_report_number(source_id)

                if report_number in existing_numbers:
                    skipped += 1
                    continue

                if not patient_id or patient_id not in patients:
                    reject(row, "Patient_ID missing or not found")
                    continue

                imaging_type = clean(row.get("Imaging_Type"))
                if imaging_type not in ALLOWED_TYPES:
                    reject(
                        row,
                        f"Unsupported Imaging_Type: {imaging_type}",
                    )
                    continue

                imaging_date = parse_datetime(row.get("Imaging_Date"))
                if imaging_date is None:
                    reject(row, "Missing or invalid Imaging_Date")
                    continue

                source_status = clean(row.get("Report_Status"))
                report_status = STATUS_MAP.get(source_status)
                if report_status is None:
                    reject(
                        row,
                        f"Unsupported Report_Status: {source_status}",
                    )
                    continue

                # Keep only valid foreign keys.
                # Do not attach an admission to the wrong patient.
                if (
                    not admission_id
                    or admission_id not in admissions
                    or admissions[admission_id] != patient_id
                ):
                    admission_id = None

                if not doctor_id or doctor_id not in doctors:
                    doctor_id = None

                source_department = clean(
                    row.get("Radiology_Department_ID")
                )
                clinical_indication = (
                    f"Source Radiology_Department_ID={source_department}"
                    if source_department
                    else None
                )

                batch.append((
                    patient_id,
                    doctor_id,
                    admission_id,
                    report_number,
                    imaging_type,
                    clean(row.get("Body_Part")) or None,
                    imaging_date,
                    clinical_indication,
                    clean(row.get("Findings")) or None,
                    clean(row.get("Impression")) or None,
                    report_status,
                    "Synthetic",
                    1,
                    1,
                    f"SRC:{source_id}",
                ))

                existing_numbers.add(report_number)

                if len(batch) >= BATCH_SIZE:
                    cur.executemany(insert_sql, batch)
                    conn.commit()
                    inserted += len(batch)
                    batch.clear()
                    print(f"Inserted this run: {inserted:,}")

            if batch:
                cur.executemany(insert_sql, batch)
                conn.commit()
                inserted += len(batch)
                batch.clear()

        cur.execute("SELECT COUNT(*) FROM imaging_reports")
        total_rows = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*)
            FROM imaging_reports
            WHERE Data_Source = 'Synthetic'
        """)
        synthetic_rows = cur.fetchone()[0]

        print("\n========== IMAGING REPORTS LOAD FINISHED ==========")
        print(f"Inserted this run: {inserted:,}")
        print(f"Already imported/skipped: {skipped:,}")
        print(f"Rejected source rows: {rejected:,}")
        print(f"Total imaging_reports rows: {total_rows:,}")
        print(f"Synthetic imaging report rows: {synthetic_rows:,}")
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
