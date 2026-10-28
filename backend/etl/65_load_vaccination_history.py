
import csv
import os
import hashlib
from datetime import datetime
from pathlib import Path

import mysql.connector
from mysql.connector import Error


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parents[2]

CSV_FILE = (
    PROJECT_DIR
    / "datasets"
    / "synthetic"
    / "vaccination_history.csv"
)

REJECT_FILE = (
    Path(__file__).resolve().parent
    / "65_vaccination_history_rejected.csv"
)

BATCH_SIZE = 5000

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "database": "healthcare_ai_db",
}

REQUIRED_HEADERS = {
    "Vaccination_ID",
    "Patient_ID",
    "Vaccine_Name",
    "Disease_Prevented",
    "Dose_Number",
    "Vaccination_Date",
    "Vaccination_Status",
    "Administered_By",
}

SOURCE_MARKER = "Synthetic source Vaccination_ID="


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    password = os.environ.get("MYSQL_PASSWORD")

    if not password:
        import getpass
        password = getpass.getpass("MySQL password: ")

    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=password,
        database=DB_CONFIG["database"],
        autocommit=False,
    )


# ============================================================
# HELPERS
# ============================================================

def clean_string(value):
    if value is None:
        return ""

    return str(value).strip()


def parse_date(value):
    value = clean_string(value)

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
            continue

    try:
        # Handles ISO dates containing a time or timezone.
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        ).date()
    except ValueError:
        return None


def parse_positive_integer(value):
    value = clean_string(value)

    if not value:
        return None

    try:
        number = int(value)
    except (ValueError, TypeError):
        return None

    return number if number > 0 else None


def stable_vaccine_code(source_id):
    digest = hashlib.sha256(
        source_id.encode("utf-8")
    ).hexdigest()[:26]

    return "SYN-" + digest


def map_vaccine_category(vaccine_name):
    """
    Use only conservative name-based classification.
    Uncertain categories default to Other.
    """
    name = vaccine_name.strip().lower()

    if any(term in name for term in (
        "covid", "coronavirus", "sars-cov-2"
    )):
        return "COVID-19"

    if any(term in name for term in (
        "influenza", "flu vaccine", "flu shot"
    )):
        return "Influenza"

    if any(term in name for term in (
        "yellow fever",
        "typhoid",
        "travel vaccine",
        "japanese encephalitis",
        "rabies",
    )):
        return "Travel"

    if any(term in name for term in (
        "childhood",
        "pediatric",
        "paediatric",
        "mmr",
        "dtap",
        "opv",
        "ipv",
        "bcg",
        "hib",
        "rotavirus",
    )):
        return "Childhood"

    return "Other"


def map_status(value):
    value = clean_string(value).lower()

    mapping = {
        "completed": "Completed",
        "complete": "Completed",
        "pending": "Pending",
        "booster due": "Booster Due",
        "booster_due": "Booster Due",
    }

    return mapping.get(value)


def write_rejections(rows):
    fields = ["CSV_Line", "Vaccination_ID", "Reason"]

    with REJECT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


# ============================================================
# MAIN
# ============================================================

def main():
    if not CSV_FILE.is_file():
        raise FileNotFoundError(
            f"Vaccination CSV not found: {CSV_FILE}"
        )

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # ----------------------------------------------------
        # 1. Read valid patient and doctor identifiers
        # ----------------------------------------------------

        cursor.execute("SELECT Patient_ID FROM patients")

        patient_ids = {
            str(row[0]).strip()
            for row in cursor.fetchall()
        }

        cursor.execute("SELECT Doctor_ID FROM doctors")

        doctor_ids = {
            str(row[0]).strip()
            for row in cursor.fetchall()
        }

        print(f"Patients available: {len(patient_ids):,}")
        print(f"Doctors available: {len(doctor_ids):,}")

        # ----------------------------------------------------
        # 2. Validate the entire source before inserting
        # ----------------------------------------------------

        valid_rows = []
        rejected_rows = []
        seen_ids = set()

        with CSV_FILE.open(
            "r",
            newline="",
            encoding="utf-8-sig",
        ) as file:

            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("CSV has no header row.")

            missing = REQUIRED_HEADERS - set(reader.fieldnames)

            if missing:
                raise ValueError(
                    f"Missing CSV columns: {sorted(missing)}"
                )

            for line_number, row in enumerate(reader, start=2):
                source_id = clean_string(
                    row.get("Vaccination_ID")
                )
                patient_id = clean_string(
                    row.get("Patient_ID")
                )
                vaccine_name = clean_string(
                    row.get("Vaccine_Name")
                )
                disease_prevented = clean_string(
                    row.get("Disease_Prevented")
                )
                dose_number = parse_positive_integer(
                    row.get("Dose_Number")
                )
                vaccination_date = parse_date(
                    row.get("Vaccination_Date")
                )
                vaccination_status = map_status(
                    row.get("Vaccination_Status")
                )
                administered_by = clean_string(
                    row.get("Administered_By")
                )

                errors = []

                if not source_id:
                    errors.append("Missing Vaccination_ID")
                elif source_id in seen_ids:
                    errors.append(
                        "Duplicate Vaccination_ID in CSV"
                    )
                else:
                    seen_ids.add(source_id)

                if not patient_id:
                    errors.append("Missing Patient_ID")
                elif patient_id not in patient_ids:
                    errors.append(
                        "Patient_ID not found in patients"
                    )

                if not vaccine_name:
                    errors.append("Missing Vaccine_Name")
                elif len(vaccine_name) > 150:
                    errors.append(
                        "Vaccine_Name exceeds 150 characters"
                    )

                if dose_number is None:
                    errors.append(
                        "Dose_Number must be a positive integer"
                    )

                if vaccination_date is None:
                    errors.append(
                        "Missing or invalid Vaccination_Date"
                    )

                if vaccination_status is None:
                    errors.append(
                        "Unsupported Vaccination_Status"
                    )

                if errors:
                    rejected_rows.append({
                        "CSV_Line": line_number,
                        "Vaccination_ID": source_id,
                        "Reason": "; ".join(errors),
                    })
                    continue

                # Only use Administered_By as a doctor FK when
                # it exactly matches a real Doctor_ID.
                # Names or unknown identifiers are not used as FKs.
                doctor_id = (
                    administered_by
                    if administered_by in doctor_ids
                    else None
                )

                category = map_vaccine_category(vaccine_name)

                notes_parts = [
                    SOURCE_MARKER + source_id,
                    "Source Disease_Prevented="
                    + (disease_prevented or "Not supplied"),
                ]

                if administered_by and doctor_id is None:
                    notes_parts.append(
                        "Source Administered_By="
                        + administered_by
                    )

                valid_rows.append({
                    "source_id": source_id,
                    "patient_id": patient_id,
                    "doctor_id": doctor_id,
                    "vaccine_name": vaccine_name,
                    "vaccine_code": stable_vaccine_code(source_id),
                    "category": category,
                    "dose_number": dose_number,
                    "vaccination_date": vaccination_date,
                    "vaccination_status": vaccination_status,
                    "notes": " | ".join(notes_parts),
                })

        # ----------------------------------------------------
        # 3. Write rejection report before any insert
        # ----------------------------------------------------

        write_rejections(rejected_rows)

        print(f"\nSource rows: {len(valid_rows) + len(rejected_rows):,}")
        print(f"Valid rows: {len(valid_rows):,}")
        print(f"Rejected rows: {len(rejected_rows):,}")
        print(f"Reject report: {REJECT_FILE}")

        # ----------------------------------------------------
        # 4. Detect previously imported source records
        # ----------------------------------------------------

        cursor.execute("""
            SELECT Notes
            FROM vaccination_history
            WHERE Notes IS NOT NULL
        """)

        existing_source_ids = set()
        existing_marker_counts = {}

        for (notes,) in cursor.fetchall():
            for part in notes.split(" | "):
                if part.startswith(SOURCE_MARKER):
                    source_id = part[len(SOURCE_MARKER):].strip()

                    if source_id:
                        existing_source_ids.add(source_id)
                        existing_marker_counts[source_id] = (
                            existing_marker_counts.get(source_id, 0) + 1
                        )

        duplicate_ids = [
            source_id
            for source_id, count in existing_marker_counts.items()
            if count > 1
        ]

        if duplicate_ids:
            raise RuntimeError(
                "Duplicate imported source IDs already exist "
                "in vaccination_history. No new rows inserted."
            )

        # Verify that any previously imported ID is consistent
        # with this CSV before proceeding.
        csv_ids = {row["source_id"] for row in valid_rows}

        unexpected_existing = existing_source_ids - csv_ids

        if unexpected_existing:
            raise RuntimeError(
                "The destination contains source IDs not present "
                "in the current CSV. No new rows inserted. "
                "Inspect the destination before continuing."
            )

        print(
            "Previously imported source IDs: "
            f"{len(existing_source_ids):,}"
        )

        # ----------------------------------------------------
        # 5. Insert statement
        # ----------------------------------------------------

        insert_sql = """
            INSERT INTO vaccination_history (
                Patient_ID,
                Administered_By_Doctor_ID,
                Vaccine_Name,
                Vaccine_Code,
                Vaccine_Category,
                Dose_Number,
                Vaccination_Date,
                Vaccination_Status,
                Verification_Status,
                Data_Source,
                Is_Active,
                Is_Deleted,
                Record_Version,
                Notes
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s,
                'Pending', 'Synthetic', 1, 0, 1, %s
            )
        """

        # ----------------------------------------------------
        # 6. Batch insert with commits and restart protection
        # ----------------------------------------------------

        pending = []
        inserted = 0
        skipped = 0

        for row in valid_rows:
            if row["source_id"] in existing_source_ids:
                skipped += 1
                continue

            pending.append((
                row["patient_id"],
                row["doctor_id"],
                row["vaccine_name"],
                row["vaccine_code"],
                row["category"],
                row["dose_number"],
                row["vaccination_date"],
                row["vaccination_status"],
                row["notes"],
            ))

            # Avoid duplicates during this run too.
            existing_source_ids.add(row["source_id"])

            if len(pending) >= BATCH_SIZE:
                cursor.executemany(insert_sql, pending)
                connection.commit()

                inserted += len(pending)
                pending.clear()

                print(f"Inserted: {inserted:,}")

        if pending:
            cursor.executemany(insert_sql, pending)
            connection.commit()
            inserted += len(pending)

        # ----------------------------------------------------
        # 7. Final counts
        # ----------------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) FROM vaccination_history"
        )
        final_count = cursor.fetchone()[0]

        print("\n========== VACCINATION LOAD FINISHED ==========")
        print(f"Inserted this run: {inserted:,}")
        print(f"Already imported/skipped: {skipped:,}")
        print(f"Rejected source rows: {len(rejected_rows):,}")
        print(
            "Total vaccination_history rows: "
            f"{final_count:,}"
        )
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
