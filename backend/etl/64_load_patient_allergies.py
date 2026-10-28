
import csv
import os
import hashlib
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
    / "patient_allergies.csv"
)

REJECT_FILE = (
    Path(__file__).resolve().parent
    / "64_patient_allergies_rejected.csv"
)

BATCH_SIZE = 5000

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "database": "healthcare_ai_db",
}

REQUIRED_HEADERS = {
    "Allergy_ID",
    "Patient_ID",
    "Allergen",
    "Category",
    "Severity",
    "Reaction",
    "Diagnosis_Date",
    "Status",
}


# ============================================================
# DATABASE CONNECTION
# ============================================================

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


# ============================================================
# SOURCE IDENTIFIER
# ============================================================

def source_code(source_id):
    """
    Create a stable source identifier within the 30-character
    Allergen_Code column.
    """
    digest = hashlib.sha256(
        source_id.encode("utf-8")
    ).hexdigest()[:26]

    return "SYN-" + digest


# ============================================================
# DATA NORMALIZATION
# ============================================================

def map_category(category, allergen):
    category = category.strip().lower()
    allergen = allergen.strip().lower()

    if category == "medication":
        return "Drug"

    if category == "food":
        return "Food"

    if category == "environmental":
        return "Environmental"

    if category == "material":
        return "Latex" if allergen == "latex" else "Other"

    return None


def map_severity(severity):
    """
    Synthetic dataset normalization only.
    These mappings are not clinical equivalences.
    """
    mapping = {
        "low": ("Mild", 1),
        "medium": ("Moderate", 2),
        "high": ("Severe", 3),
    }

    return mapping.get(severity.strip().lower())


def map_status(status):
    status = status.strip().lower()

    if status == "active":
        return 1

    if status in {"inactive", "resolved"}:
        return 0

    return None


# ============================================================
# REJECTION REPORT
# ============================================================

def write_rejections(rejected_rows):
    fields = ["CSV_Line", "Allergy_ID", "Reason"]

    with REJECT_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rejected_rows)


# ============================================================
# MAIN LOADER
# ============================================================

def main():

    if not CSV_FILE.is_file():
        raise FileNotFoundError(
            f"Source CSV not found: {CSV_FILE}"
        )

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # ----------------------------------------------------
        # 1. Load patient IDs for foreign-key validation
        # ----------------------------------------------------

        cursor.execute("SELECT Patient_ID FROM patients")

        patient_ids = {
            str(row[0]).strip()
            for row in cursor.fetchall()
        }

        print(f"Patient IDs available: {len(patient_ids):,}")

        # ----------------------------------------------------
        # 2. Validate complete CSV before inserting anything
        # ----------------------------------------------------

        valid_rows = []
        rejected_rows = []
        seen_source_ids = set()

        with CSV_FILE.open(
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("CSV has no header row.")

            missing_headers = (
                REQUIRED_HEADERS - set(reader.fieldnames)
            )

            if missing_headers:
                raise ValueError(
                    "Missing CSV columns: "
                    f"{sorted(missing_headers)}"
                )

            for line_number, row in enumerate(reader, start=2):

                source_id = (
                    row.get("Allergy_ID") or ""
                ).strip()

                patient_id = (
                    row.get("Patient_ID") or ""
                ).strip()

                allergen = (
                    row.get("Allergen") or ""
                ).strip()

                category = map_category(
                    row.get("Category") or "",
                    allergen
                )

                severity_result = map_severity(
                    row.get("Severity") or ""
                )

                reaction = (
                    row.get("Reaction") or ""
                ).strip()

                active_value = map_status(
                    row.get("Status") or ""
                )

                errors = []

                if not source_id:
                    errors.append("Missing Allergy_ID")

                elif source_id in seen_source_ids:
                    errors.append("Duplicate Allergy_ID in CSV")

                else:
                    seen_source_ids.add(source_id)

                if not patient_id:
                    errors.append("Missing Patient_ID")

                elif patient_id not in patient_ids:
                    errors.append(
                        "Patient_ID not found in patients"
                    )

                if not allergen:
                    errors.append("Missing Allergen")

                if category is None:
                    errors.append("Unsupported Category")

                if severity_result is None:
                    errors.append("Unsupported Severity")

                if active_value is None:
                    errors.append("Unsupported Status")

                if errors:
                    rejected_rows.append({
                        "CSV_Line": line_number,
                        "Allergy_ID": source_id,
                        "Reason": "; ".join(errors),
                    })
                    continue

                severity, severity_score = severity_result

                valid_rows.append({
                    "source_id": source_id,
                    "source_code": source_code(source_id),
                    "patient_id": patient_id,
                    "allergen": allergen[:150],
                    "category": category,
                    "severity": severity,
                    "severity_score": severity_score,
                    "reaction": reaction or None,
                    "is_active": active_value,
                    "notes": (
                        "Synthetic source Allergy_ID="
                        f"{source_id}"
                    ),
                })

        # ----------------------------------------------------
        # 3. Save validation failures before loading
        # ----------------------------------------------------

        write_rejections(rejected_rows)

        print(
            "Total source rows validated: "
            f"{len(valid_rows) + len(rejected_rows):,}"
        )
        print(f"Valid rows: {len(valid_rows):,}")
        print(f"Rejected rows: {len(rejected_rows):,}")
        print(f"Reject report: {REJECT_FILE}")

        # ----------------------------------------------------
        # 4. Read existing records for duplicate prevention
        # ----------------------------------------------------

        cursor.execute("""
            SELECT
                Patient_ID,
                Allergy_Name,
                Allergen_Code,
                Notes
            FROM patient_allergies
        """)

        existing_records = cursor.fetchall()

        # Identify source IDs already imported by this loader.
        existing_source_ids = set()

        # A row is recognized as one of ours only when its
        # Notes field contains our exact source-ID marker.
        for patient_id, allergy_name, code, notes in existing_records:

            if not notes:
                continue

            marker = "Synthetic source Allergy_ID="

            if notes.startswith(marker):
                existing_source_ids.add(
                    notes[len(marker):].strip()
                )

        # Refuse to load if any existing source ID appears more
        # than once in the destination. Do not modify existing rows.
        source_id_counts = {}

        for patient_id, allergy_name, code, notes in existing_records:

            if not notes:
                continue

            marker = "Synthetic source Allergy_ID="

            if notes.startswith(marker):
                source_id = notes[len(marker):].strip()
                source_id_counts[source_id] = (
                    source_id_counts.get(source_id, 0) + 1
                )

        duplicates_in_database = [
            source_id
            for source_id, count in source_id_counts.items()
            if count > 1
        ]

        if duplicates_in_database:
            raise RuntimeError(
                "Duplicate imported Allergy_ID markers already exist "
                "in patient_allergies. No new rows were inserted. "
                "Inspect duplicate source IDs before continuing."
            )

        # Also detect collisions in the derived codes.
        code_to_source = {}

        for row in valid_rows:
            code = row["source_code"]
            source_id = row["source_id"]

            if code in code_to_source:
                if code_to_source[code] != source_id:
                    raise RuntimeError(
                        "Source-code collision detected. "
                        "No records were inserted."
                    )

            code_to_source[code] = source_id

        print(
            "Previously imported source IDs: "
            f"{len(existing_source_ids):,}"
        )

        # ----------------------------------------------------
        # 5. Prepare insert statement
        # ----------------------------------------------------

        insert_sql = """
            INSERT INTO patient_allergies (
                Patient_ID,
                Allergy_Name,
                Allergen_Code,
                Allergy_Category,
                Allergy_Severity,
                Reaction_Severity_Score,
                Reaction,
                First_Observed_Date,
                Is_Active,
                Is_Deleted,
                Verification_Status,
                Data_Source,
                Record_Version,
                Notes
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                NULL, %s, 0, 'Pending', 'Synthetic', 1, %s
            )
        """

        # ----------------------------------------------------
        # 6. Insert in batches; commit after each batch
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
                row["allergen"],
                row["source_code"],
                row["category"],
                row["severity"],
                row["severity_score"],
                row["reaction"],
                row["is_active"],
                row["notes"],
            ))

            # Prevent re-adding the same source ID during this run.
            existing_source_ids.add(row["source_id"])

            if len(pending) >= BATCH_SIZE:
                cursor.executemany(insert_sql, pending)
                connection.commit()

                inserted += len(pending)
                pending.clear()

                print(f"Inserted: {inserted:,} rows")

        if pending:
            cursor.executemany(insert_sql, pending)
            connection.commit()

            inserted += len(pending)
            pending.clear()

        # ----------------------------------------------------
        # 7. Final verification
        # ----------------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) FROM patient_allergies"
        )
        final_count = cursor.fetchone()[0]

        print("\n========== ALLERGY LOAD FINISHED ==========")
        print(f"Inserted this run: {inserted:,}")
        print(f"Already imported/skipped: {skipped:,}")
        print(f"Rejected source rows: {len(rejected_rows):,}")
        print(f"Total rows now in patient_allergies: {final_count:,}")
        print(f"Rejected-row report: {REJECT_FILE}")

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
