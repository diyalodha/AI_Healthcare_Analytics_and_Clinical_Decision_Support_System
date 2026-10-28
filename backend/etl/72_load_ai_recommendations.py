
import csv
import os
import uuid
from datetime import datetime
from pathlib import Path

import mysql.connector


SOURCE = Path("datasets/synthetic/ai_recommendations.csv")
BATCH_SIZE = 2000
EXPECTED_ROWS = 500_000


def parse_date(value, line_number):
    value = (value or "").strip()
    if not value:
        return None

    for fmt in (
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y",
    ):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass

    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return result.replace(tzinfo=None) if result.tzinfo else result
    except ValueError as exc:
        raise RuntimeError(
            f"Invalid date at CSV line {line_number}: {value}"
        ) from exc


def main():
    if not SOURCE.exists():
        raise SystemExit(f"Source file not found: {SOURCE}")

    password = os.environ.get("MYSQL_PASSWORD")
    if not password:
        raise SystemExit(
            "MYSQL_PASSWORD is missing. Set it in your PowerShell session."
        )

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="healthcare_ai_db",
        autocommit=False,
    )
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT COUNT(*) FROM clinical_decision_recommendations"
        )
        existing = cur.fetchone()[0]

        if existing:
            raise RuntimeError(
                f"Destination already contains {existing} rows; "
                "refusing to overwrite."
            )

        cur.execute("""
            SELECT Prediction_Session_ID, Patient_ID, Prediction_Number,
                   Prediction_Date, Model_Name, Risk_Level
            FROM prediction_sessions
        """)

        sessions = {
            str(sid): {
                "patient": str(patient),
                "number": number,
                "date": date,
                "model": model,
                "risk": risk,
            }
            for sid, patient, number, date, model, risk in cur.fetchall()
        }

        if len(sessions) != EXPECTED_ROWS:
            raise RuntimeError(
                f"Expected {EXPECTED_ROWS:,} prediction sessions; "
                f"found {len(sessions):,}."
            )

        # Map source categories to valid database ENUM values.
        type_map = {
            "Risk Management": "Monitoring",
            "Preventive Care": "Preventive Care",
            "Monitoring": "Monitoring",
            "Treatment Support": "Treatment",
        }

        review_map = {
            "Approved": "Approved",
            "Pending": "Pending",
            # "Reviewed" does not establish approval.
            "Reviewed": "Pending",
        }

        insert_sql = """
            INSERT INTO clinical_decision_recommendations (
                Recommendation_ID,
                Patient_ID,
                Prediction_Session_ID,
                Recommendation_Number,
                Recommendation_Date,
                Recommendation_Type,
                Recommended_Action,
                Recommendation_Status,
                Model_Name,
                AI_Confidence_Score,
                AI_Risk_Level,
                Priority_Level,
                Doctor_Approval_Status,
                Data_Source,
                Is_Active,
                Is_Deleted,
                Record_Version
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        batch = []
        seen_ids = set()
        seen_sessions = set()
        total = 0

        with SOURCE.open(
            "r", encoding="utf-8-sig", newline=""
        ) as file:
            reader = csv.DictReader(file)

            required = {
                "Recommendation_ID",
                "Patient_ID",
                "AI_Prediction_ID",
                "Recommendation_Type",
                "Recommendation_Text",
                "Priority_Level",
                "AI_Confidence",
                "Doctor_Review_Status",
                "Generated_Date",
            }

            missing = required - set(reader.fieldnames or [])
            if missing:
                raise RuntimeError(
                    f"Missing CSV columns: {sorted(missing)}"
                )

            for line_number, row in enumerate(reader, start=2):
                rid = (row["Recommendation_ID"] or "").strip().lower()
                sid = (row["AI_Prediction_ID"] or "").strip()
                patient = (row["Patient_ID"] or "").strip()

                try:
                    if str(uuid.UUID(rid)) != rid:
                        raise ValueError(
                            "UUID is not in canonical format"
                        )
                except (ValueError, AttributeError) as exc:
                    raise RuntimeError(
                        f"Invalid recommendation UUID at line "
                        f"{line_number}: {rid}"
                    ) from exc

                if rid in seen_ids:
                    raise RuntimeError(
                        f"Duplicate recommendation UUID: {rid}"
                    )
                seen_ids.add(rid)

                session = sessions.get(sid)
                if session is None:
                    raise RuntimeError(
                        f"Prediction session missing at line "
                        f"{line_number}: {sid}"
                    )

                if session["patient"] != patient:
                    raise RuntimeError(
                        f"Patient/prediction mismatch at line "
                        f"{line_number}"
                    )

                # Each recommendation receives a unique number.
                recommendation_number = f"REC{total + 1:012d}"

                source_type = (
                    row["Recommendation_Type"] or ""
                ).strip()

                recommendation_type = type_map.get(source_type)
                if recommendation_type is None:
                    raise RuntimeError(
                        f"Unsupported recommendation type at line "
                        f"{line_number}: {source_type}"
                    )

                source_priority = (
                    row["Priority_Level"] or ""
                ).strip()

                if source_priority not in {"Low", "Medium", "High"}:
                    raise RuntimeError(
                        f"Unsupported priority at line {line_number}: "
                        f"{source_priority}"
                    )

                try:
                    # Source confidence uses a 0-1 scale.
                    # Database confidence uses a 0-100 scale.
                    confidence = float(row["AI_Confidence"]) * 100
                except (TypeError, ValueError) as exc:
                    raise RuntimeError(
                        f"Invalid AI confidence at line {line_number}"
                    ) from exc

                if not 0 <= confidence <= 100:
                    raise RuntimeError(
                        f"AI confidence outside 0-1 source scale "
                        f"at line {line_number}"
                    )

                batch.append((
                    rid,
                    patient,
                    sid,
                    recommendation_number,
                    parse_date(
                        row["Generated_Date"], line_number
                    ) or session["date"],
                    recommendation_type,
                    (row["Recommendation_Text"] or "").strip() or None,
                    "Generated",
                    session["model"],
                    round(confidence, 2),
                    session["risk"],
                    source_priority,
                    review_map.get(
                        (row["Doctor_Review_Status"] or "").strip(),
                        "Pending",
                    ),
                    "Synthetic",
                    1,
                    0,
                    1,
                ))

                total += 1

                if len(batch) >= BATCH_SIZE:
                    cur.executemany(insert_sql, batch)
                    batch.clear()

                    if total % 20_000 == 0:
                        print(
                            f"Processed {total:,} recommendation rows..."
                        )

        if batch:
            cur.executemany(insert_sql, batch)

        if total != EXPECTED_ROWS or len(seen_ids) != EXPECTED_ROWS:
            raise RuntimeError(
                f"Expected {EXPECTED_ROWS:,} unique recommendations; "
                f"processed {total:,}."
            )

        cur.execute(
            "SELECT COUNT(*) FROM clinical_decision_recommendations"
        )
        inserted = cur.fetchone()[0]

        if inserted != total:
            raise RuntimeError(
                f"Count mismatch: processed={total}, "
                f"destination={inserted}"
            )

        conn.commit()
        print(
            f"SUCCESS: committed {inserted:,} recommendation records."
        )

    except Exception:
        conn.rollback()
        print("FAILED: transaction rolled back.")
        raise

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
