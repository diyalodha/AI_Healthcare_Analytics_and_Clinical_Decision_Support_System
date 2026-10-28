
import csv
import os
import hashlib
from datetime import datetime
from pathlib import Path

import mysql.connector
from mysql.connector import Error


PROJECT_DIR = Path(__file__).resolve().parents[2]
CSV_FILE = PROJECT_DIR / "datasets" / "synthetic" / "clinical_notes.csv"
REJECT_FILE = Path(__file__).resolve().parent / "66_clinical_notes_rejected.csv"

BATCH_SIZE = 5000
SOURCE_MARKER = "Synthetic source Clinical_Note_ID="

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "database": "healthcare_ai_db",
}

REQUIRED_HEADERS = {
    "Clinical_Note_ID",
    "Patient_ID",
    "Admission_ID",
    "Doctor_ID",
    "Note_Type",
    "Note_Date",
    "Clinical_Text",
    "Priority",
    "Status",
}


def get_connection():
    password = os.environ.get("MYSQL_PASSWORD")
    if not password:
        import getpass
        password = getpass.getpass("MySQL password: ")

    return mysql.connector.connect(
        **DB_CONFIG,
        password=password,
        autocommit=False,
    )


def clean(value):
    return str(value).strip() if value is not None else ""


def parse_date(value):
    value = clean(value)
    if not value:
        return None

    formats = (
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%d/%m/%Y",
    )

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass

    try:
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        ).date()
    except ValueError:
        return None


def map_note_type(value):
    value = clean(value).lower()

    mapping = {
        "consultation": "Consultation",
        "consultation note": "Consultation",
        "progress": "Progress",
        "progress note": "Progress",
        "discharge": "Discharge",
        "discharge note": "Discharge",
        "discharge summary": "Discharge",
        "nursing": "Nursing",
        "nursing note": "Nursing",
        "emergency": "Emergency",
        "emergency note": "Emergency",
        "follow-up": "Follow-Up",
        "follow up": "Follow-Up",
        "follow up note": "Follow-Up",
        "follow-up note": "Follow-Up",
        "followup": "Follow-Up",
        "icu": "ICU",
        "icu note": "ICU",
        "general": "General",
        "general note": "General",
    }

    return mapping.get(value)


def map_note_status(value):
    value = clean(value).lower()

    mapping = {
        "draft": "Draft",
        "reviewed": "Reviewed",
        "approved": "Approved",
        "archived": "Archived",
        "completed": "Reviewed",
    }

    return mapping.get(value)


def write_rejections(rows):
    fields = ["CSV_Line", "Clinical_Note_ID", "Reason"]

    with REJECT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    if not CSV_FILE.is_file():
        raise FileNotFoundError(
            f"Clinical notes CSV not found: {CSV_FILE}"
        )

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Reference IDs
        cursor.execute("SELECT Patient_ID FROM patients")
        patient_ids = {clean(r[0]) for r in cursor.fetchall()}

        cursor.execute("SELECT Doctor_ID FROM doctors")
        doctor_ids = {clean(r[0]) for r in cursor.fetchall()}

        cursor.execute("SELECT Admission_ID, Patient_ID FROM admissions")
        admission_patient = {
            clean(admission_id): clean(patient_id)
            for admission_id, patient_id in cursor.fetchall()
        }

        print(f"Patients available: {len(patient_ids):,}")
        print(f"Doctors available: {len(doctor_ids):,}")
        print(f"Admissions available: {len(admission_patient):,}")

        valid_rows = []
        rejected = []
        seen_source_ids = set()

        # Validate all source records before writing anything.
        with CSV_FILE.open(
            "r", newline="", encoding="utf-8-sig"
        ) as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("CSV has no header row.")

            missing = REQUIRED_HEADERS - set(reader.fieldnames)
            if missing:
                raise ValueError(
                    f"Missing CSV columns: {sorted(missing)}"
                )

            for line, row in enumerate(reader, start=2):
                source_id = clean(row.get("Clinical_Note_ID"))
                patient_id = clean(row.get("Patient_ID"))
                doctor_id = clean(row.get("Doctor_ID"))
                source_admission_id = clean(row.get("Admission_ID"))
                note_type = map_note_type(row.get("Note_Type"))
                note_status = map_note_status(row.get("Status"))
                note_date = parse_date(row.get("Note_Date"))
                clinical_text = clean(row.get("Clinical_Text"))

                errors = []

                if not source_id:
                    errors.append("Missing Clinical_Note_ID")
                elif source_id in seen_source_ids:
                    errors.append("Duplicate Clinical_Note_ID in CSV")
                else:
                    seen_source_ids.add(source_id)

                if not patient_id or patient_id not in patient_ids:
                    errors.append("Patient_ID missing or not found")

                if not doctor_id or doctor_id not in doctor_ids:
                    errors.append("Doctor_ID missing or not found")

                if note_type is None:
                    errors.append(
                        "Unsupported Note_Type: "
                        + clean(row.get("Note_Type"))
                    )

                if note_status is None:
                    errors.append(
                        "Unsupported Status: "
                        + clean(row.get("Status"))
                    )

                if note_date is None:
                    errors.append("Missing or invalid Note_Date")

                if not clinical_text:
                    errors.append("Clinical_Text is empty")

                if errors:
                    rejected.append({
                        "CSV_Line": line,
                        "Clinical_Note_ID": source_id,
                        "Reason": "; ".join(errors),
                    })
                    continue

                # Never attach a note to another patient's admission.
                # Preserve the source ID in the title for traceability.
                admission_id = None
                admission_note = (
                    source_admission_id
                    if source_admission_id
                    else "None"
                )

                if (
                    source_admission_id in admission_patient
                    and admission_patient[source_admission_id] == patient_id
                ):
                    admission_id = source_admission_id

                title = (
                    f"{SOURCE_MARKER}{source_id}"
                    f" | Source Note_Date={note_date.isoformat()}"
                    f" | Source Admission_ID={admission_note}"
                    f" | Source Priority={clean(row.get('Priority')) or 'Not supplied'}"
                )

                if len(title) > 200:
                    rejected.append({
                        "CSV_Line": line,
                        "Clinical_Note_ID": source_id,
                        "Reason": "Generated Note_Title exceeds 200 characters",
                    })
                    continue

                note_number = "CN-" + hashlib.sha256(
                    source_id.encode("utf-8")
                ).hexdigest()[:24]

                valid_rows.append((
                    source_id,
                    patient_id,
                    doctor_id,
                    admission_id,
                    note_number,
                    note_type,
                    title,
                    clinical_text,
                    note_status,
                ))

        write_rejections(rejected)

        print(f"\nSource rows: {len(valid_rows) + len(rejected):,}")
        print(f"Valid rows: {len(valid_rows):,}")
        print(f"Rejected rows: {len(rejected):,}")
        print(f"Reject report: {REJECT_FILE}")

        # Restart safety: identify previously imported source IDs.
        cursor.execute("""
            SELECT Note_Title
            FROM clinical_notes
            WHERE Note_Title LIKE %s
        """, (f"{SOURCE_MARKER}%",))

        existing_ids = set()
        duplicate_existing_ids = set()

        for (title,) in cursor.fetchall():
            title = clean(title)
            if not title.startswith(SOURCE_MARKER):
                continue

            source_id = title[len(SOURCE_MARKER):].split(" | ")[0]
            if source_id in existing_ids:
                duplicate_existing_ids.add(source_id)
            existing_ids.add(source_id)

        if duplicate_existing_ids:
            raise RuntimeError(
                "Duplicate source markers already exist in clinical_notes. "
                "No new rows inserted; investigate the destination first."
            )

        valid_source_ids = {r[0] for r in valid_rows}
        if existing_ids - valid_source_ids:
            raise RuntimeError(
                "Destination contains source IDs absent from this CSV. "
                "No new rows inserted; investigate before continuing."
            )

        print(f"Previously imported source IDs: {len(existing_ids):,}")

        insert_sql = """
            INSERT INTO clinical_notes (
                Patient_ID,
                Doctor_ID,
                Admission_ID,
                Note_Number,
                Note_Type,
                Note_Title,
                Clinical_Note,
                Note_Status,
                Data_Source,
                Is_Active,
                Is_Deleted,
                Record_Version
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s,
                'Synthetic', 1, 0, 1
            )
        """

        inserted = 0
        skipped = 0
        batch = []

        for (
            source_id,
            patient_id,
            doctor_id,
            admission_id,
            note_number,
            note_type,
            title,
            clinical_text,
            note_status,
        ) in valid_rows:

            if source_id in existing_ids:
                skipped += 1
                continue

            batch.append((
                patient_id,
                doctor_id,
                admission_id,
                note_number,
                note_type,
                title,
                clinical_text,
                note_status,
            ))

            existing_ids.add(source_id)

            if len(batch) >= BATCH_SIZE:
                cursor.executemany(insert_sql, batch)
                connection.commit()
                inserted += len(batch)
                batch.clear()
                print(f"Inserted: {inserted:,}")

        if batch:
            cursor.executemany(insert_sql, batch)
            connection.commit()
            inserted += len(batch)

        cursor.execute("SELECT COUNT(*) FROM clinical_notes")
        total = cursor.fetchone()[0]

        print("\n========== CLINICAL NOTES LOAD FINISHED ==========")
        print(f"Inserted this run: {inserted:,}")
        print(f"Already imported/skipped: {skipped:,}")
        print(f"Rejected source rows: {len(rejected):,}")
        print(f"Total clinical_notes rows: {total:,}")
        print(f"Reject report: {REJECT_FILE}")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    try:
        main()
    except (Error, OSError, ValueError, RuntimeError) as exc:
        print(f"\nLOAD STOPPED: {exc}")
        raise
