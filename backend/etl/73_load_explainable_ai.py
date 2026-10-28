import csv
import os
import uuid
from datetime import datetime
from pathlib import Path

import mysql.connector


SOURCE = Path("datasets/synthetic/explainable_ai.csv")
BATCH_SIZE = 2000
EXPECTED_ROWS = 500_000


def parse_date(value, line_number):
    value = (value or "").strip()
    if not value:
        return None

    for fmt in (
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

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ["MYSQL_PASSWORD"],
        database="healthcare_ai_db",
        autocommit=False,
    )
    cur = conn.cursor()

    try:
        cur.execute("SELECT COUNT(*) FROM explainable_ai_results")
        existing = cur.fetchone()[0]
        if existing:
            raise RuntimeError(
                f"Destination already contains {existing} rows; "
                "refusing to overwrite."
            )

        cur.execute("""
            SELECT Prediction_Session_ID, Patient_ID, Prediction_Number,
                   Prediction_Date, Model_Name, Confidence_Score
            FROM prediction_sessions
        """)

        sessions = {
            str(sid): {
                "patient": str(patient),
                "number": number,
                "date": date,
                "model": model,
                "confidence": confidence,
            }
            for sid, patient, number, date, model, confidence
            in cur.fetchall()
        }

        if len(sessions) != EXPECTED_ROWS:
            raise RuntimeError(
                f"Expected {EXPECTED_ROWS:,} prediction sessions; "
                f"found {len(sessions):,}."
            )

        method_map = {
            "SHAP": "SHAP",
            "LIME": "LIME",
            "Feature Importance": "Feature Importance",
            "Rule Based Explanation": "Rule Based",
        }

        insert_sql = """
            INSERT INTO explainable_ai_results (
                XAI_Result_ID, Prediction_Session_ID, Patient_ID,
                Prediction_Number, Prediction_Date, Model_Name,
                Explanation_Method, Important_Features, Feature_Contribution,
                Explanation_Text, Model_Decision, Confidence_Explanation,
                Confidence_Score, Doctor_Approval_Status, Data_Source
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        batch = []
        seen_ids = set()
        total = 0

        with SOURCE.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            required = {
                "Explainability_ID", "AI_Prediction_ID", "Patient_ID",
                "Feature_Name", "Feature_Value", "Contribution_Score",
                "Impact_Level", "Explanation",
                "Model_Interpretation_Method", "Generated_Date",
            }
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise RuntimeError(
                    f"Missing CSV columns: {sorted(missing)}"
                )

            for line_number, row in enumerate(reader, start=2):
                xid = (row["Explainability_ID"] or "").strip().lower()
                sid = (row["AI_Prediction_ID"] or "").strip()
                patient = (row["Patient_ID"] or "").strip()

                try:
                    if str(uuid.UUID(xid)) != xid:
                        raise ValueError("UUID is not in canonical format")
                except (ValueError, AttributeError) as exc:
                    raise RuntimeError(
                        f"Invalid explanation UUID at line {line_number}: {xid}"
                    ) from exc

                if xid in seen_ids:
                    raise RuntimeError(f"Duplicate explanation UUID: {xid}")
                seen_ids.add(xid)

                session = sessions.get(sid)
                if session is None:
                    raise RuntimeError(
                        f"Prediction session missing at CSV line "
                        f"{line_number}: {sid}"
                    )

                if session["patient"] != patient:
                    raise RuntimeError(
                        f"Patient/prediction mismatch at CSV line {line_number}"
                    )

                method = method_map.get(
                    (row["Model_Interpretation_Method"] or "").strip(),
                    "Other",
                )

                feature = (row["Feature_Name"] or "").strip()
                feature_value = (row["Feature_Value"] or "").strip()
                contribution = (row["Contribution_Score"] or "").strip()
                impact = (row["Impact_Level"] or "").strip()
                explanation = (row["Explanation"] or "").strip()

                contribution_text = (
                    f"Feature value: {feature_value}; "
                    f"source contribution score: {contribution}; "
                    f"source impact label: {impact}"
                )

                # Unique explanation reference. The original prediction
                # number remains available through Prediction_Session_ID.
                xai_number = f"XAI{total + 1:012d}"

                batch.append((
                    xid,
                    sid,
                    patient,
                    xai_number,
                    parse_date(row["Generated_Date"], line_number)
                    or session["date"],
                    session["model"],
                    method,
                    feature or None,
                    contribution_text,
                    explanation or None,
                    None,
                    "Synthetic demo explanation; not independently "
                    "clinically validated.",
                    session["confidence"],
                    "Pending",
                    "Synthetic",
                ))
                total += 1

                if len(batch) >= BATCH_SIZE:
                    cur.executemany(insert_sql, batch)
                    batch.clear()

                    if total % 20_000 == 0:
                        print(f"Processed {total:,} explanation rows...")

        if batch:
            cur.executemany(insert_sql, batch)

        if total != EXPECTED_ROWS or len(seen_ids) != EXPECTED_ROWS:
            raise RuntimeError(
                f"Expected {EXPECTED_ROWS:,} unique explanations; "
                f"processed {total:,}."
            )

        cur.execute("SELECT COUNT(*) FROM explainable_ai_results")
        inserted = cur.fetchone()[0]
        if inserted != total:
            raise RuntimeError(
                f"Count mismatch: processed={total}, destination={inserted}"
            )

        conn.commit()
        print(f"SUCCESS: committed {inserted:,} explainability records.")
        print("Source explanation UUIDs and prediction links preserved.")
        print("Doctor approval remains Pending.")

    except Exception:
        conn.rollback()
        print("FAILED: transaction rolled back.")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
