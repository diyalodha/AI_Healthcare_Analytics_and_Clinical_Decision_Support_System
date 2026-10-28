
import csv
import hashlib
import os
import sys
from decimal import Decimal, InvalidOperation
from getpass import getpass
from pathlib import Path

import mysql.connector


ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "datasets" / "synthetic" / "medical_images_metadata.csv"
REJECT_PATH = ROOT / "backend" / "etl" / "70_medical_images_metadata_rejected.csv"

BATCH_SIZE = 2000

STATUS_MAP = {
    "Stored": "Available",
    "Available": "Available",
    "Archived": "Archived",
    "Deleted": "Deleted",
}


def clean(value):
    return (value or "").strip()


def stable_hash(source_id):
    return hashlib.sha256(source_id.encode("utf-8")).hexdigest()[:24]


def stable_image_number(source_id):
    return f"IM-{stable_hash(source_id)}"


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
        INSERT INTO medical_images_metadata (
            Image_Metadata_ID,
            Imaging_Report_ID,
            Patient_ID,
            Image_Number,
            Image_File_Name,
            Original_File_Name,
            Image_Format,
            Image_Size_MB,
            Storage_Path,
            Checksum_Hash,
            Image_Status,
            Modality,
            Body_Part,
            Acquisition_Date,
            Data_Source,
            Is_Active,
            Record_Version,
            Created_By
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    try:
        cur = conn.cursor()

        # Map synthetic report numbers back to their database report IDs.
        cur.execute("""
            SELECT
                Imaging_Report_ID,
                Patient_ID,
                Imaging_Report_Number,
                Body_Part,
                Imaging_Date
            FROM imaging_reports
            WHERE Imaging_Report_Number LIKE 'IMG-%'
        """)

        reports = {
            report_number: {
                "report_id": str(report_id),
                "patient_id": str(patient_id),
                "body_part": body_part,
                "imaging_date": imaging_date,
            }
            for (
                report_id,
                patient_id,
                report_number,
                body_part,
                imaging_date,
            ) in cur.fetchall()
        }

        cur.execute("""
            SELECT Image_Metadata_ID
            FROM medical_images_metadata
        """)
        existing_ids = {str(row[0]) for row in cur.fetchall()}

        print(f"Matching generated imaging reports: {len(reports):,}")
        print(f"Existing metadata IDs: {len(existing_ids):,}")

        required_columns = {
            "Image_Metadata_ID",
            "Imaging_Report_ID",
            "Patient_ID",
            "Admission_ID",
            "Image_Type",
            "File_Format",
            "Image_Size_MB",
            "Modality",
            "Machine_ID",
            "Storage_Location",
            "Image_Status",
        }

        with CSV_PATH.open(
            "r", encoding="utf-8-sig", newline=""
        ) as source, REJECT_PATH.open(
            "w", encoding="utf-8-sig", newline=""
        ) as reject_file:

            reader = csv.DictReader(source)

            missing = required_columns - set(reader.fieldnames or [])
            if missing:
                raise ValueError(
                    "CSV is missing required columns: "
                    + ", ".join(sorted(missing))
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
                metadata_id = clean(row.get("Image_Metadata_ID"))
                source_report_id = clean(row.get("Imaging_Report_ID"))
                patient_id = clean(row.get("Patient_ID"))

                if not metadata_id:
                    reject(row, "Missing Image_Metadata_ID")
                    continue

                if metadata_id in existing_ids:
                    skipped += 1
                    continue

                # Recreate the deterministic report number used by loader 69.
                report_number = (
                    f"IMG-{stable_hash(source_report_id)}"
                    if source_report_id else ""
                )
                report = reports.get(report_number)

                if report is None:
                    reject(
                        row,
                        "Imaging_Report_ID has no matching imported report",
                    )
                    continue

                if not patient_id:
                    reject(row, "Missing Patient_ID")
                    continue

                if patient_id != report["patient_id"]:
                    reject(
                        row,
                        "Patient_ID does not match the linked imaging report",
                    )
                    continue

                image_format = clean(row.get("File_Format")) or None
                if image_format and len(image_format) > 20:
                    reject(row, "File_Format exceeds 20 characters")
                    continue

                raw_size = clean(row.get("Image_Size_MB"))
                image_size = None

                if raw_size:
                    try:
                        image_size = Decimal(raw_size)
                        if (
                            not image_size.is_finite()
                            or image_size < 0
                            or image_size > Decimal("99999999.99")
                        ):
                            raise InvalidOperation
                        image_size = image_size.quantize(Decimal("0.01"))
                    except (InvalidOperation, ValueError):
                        reject(row, "Invalid Image_Size_MB")
                        continue

                source_status = clean(row.get("Image_Status"))
                image_status = STATUS_MAP.get(source_status)

                if image_status is None:
                    reject(
                        row,
                        f"Unsupported Image_Status: {source_status}",
                    )
                    continue

                modality = clean(row.get("Modality")) or None
                if modality and len(modality) > 100:
                    reject(row, "Modality exceeds 100 characters")
                    continue

                storage_path = clean(row.get("Storage_Location")) or None
                if storage_path and len(storage_path) > 500:
                    reject(row, "Storage_Location exceeds 500 characters")
                    continue

                # The source has no actual filename or checksum.
                # This is an explicit metadata placeholder, not a real file.
                image_number = stable_image_number(metadata_id)
                placeholder_name = f"METADATA_ONLY_{stable_hash(metadata_id)}"

                batch.append((
                    metadata_id,
                    report["report_id"],
                    patient_id,
                    image_number,
                    placeholder_name,
                    None,                         # Original_File_Name unknown
                    image_format,
                    image_size,
                    storage_path,                 # Source value preserved
                    None,                         # Checksum not provided
                    image_status,
                    modality,
                    report["body_part"],          # From linked imaging report
                    report["imaging_date"],       # From linked imaging report
                    "Synthetic",
                    1,
                    1,
                    f"SRC:{metadata_id}",
                ))

                existing_ids.add(metadata_id)

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

        cur.execute("SELECT COUNT(*) FROM medical_images_metadata")
        total_rows = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*)
            FROM medical_images_metadata
            WHERE Data_Source = 'Synthetic'
        """)
        synthetic_rows = cur.fetchone()[0]

        print("\n========== MEDICAL IMAGE METADATA LOAD FINISHED ==========")
        print(f"Inserted this run: {inserted:,}")
        print(f"Already imported/skipped: {skipped:,}")
        print(f"Rejected source rows: {rejected:,}")
        print(f"Total medical_images_metadata rows: {total_rows:,}")
        print(f"Synthetic metadata rows: {synthetic_rows:,}")
        print(f"Reject report: {REJECT_PATH}")
        print(
            "\nNote: metadata rows do not confirm that physical image "
            "files exist."
        )

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
