import os

import mysql.connector
from mysql.connector import Error

# ==============================================================
# CONFIGURATION
# ==============================================================

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD")
DB_NAME = "healthcare_ai_db"


# ==============================================================
# DATABASE CONNECTION
# ==============================================================

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print(f"âŒ Database connection failed: {e}")

    return None


# ==============================================================
# MAIN VALIDATION
# ==============================================================

def main():

    print("=" * 70)
    print("        AI HEALTHCARE PROJECT - DISEASE VALIDATION")
    print("=" * 70)
    print(f"Database     : {DB_NAME}")
    print("Table        : diseases")
    print("=" * 70)
    print()

    connection = get_connection()

    if connection is None:
        return

    print("MySQL connection successful.")
    print()

    cursor = connection.cursor()

    checks_passed = True

    # ==========================================================
    # 1. TOTAL DISEASES
    # ==========================================================

    print("1. TOTAL DISEASES")
    print("-" * 70)

    cursor.execute("""
        SELECT COUNT(*)
        FROM diseases
    """)

    total_diseases = cursor.fetchone()[0]

    print(f"Total diseases: {total_diseases:,}")

    # ==========================================================
    # 2. UNIQUE DISEASE IDs
    # ==========================================================

    print()
    print("2. UNIQUE DISEASE IDs")
    print("-" * 70)

    cursor.execute("""
        SELECT COUNT(DISTINCT Disease_ID)
        FROM diseases
    """)

    unique_disease_ids = cursor.fetchone()[0]

    print(f"Unique Disease_IDs: {unique_disease_ids:,}")

    # ==========================================================
    # 3. NULL DISEASE IDs
    # ==========================================================

    print()
    print("3. NULL DISEASE IDs")
    print("-" * 70)

    cursor.execute("""
        SELECT COUNT(*)
        FROM diseases
        WHERE Disease_ID IS NULL
    """)

    null_disease_ids = cursor.fetchone()[0]

    print(f"NULL Disease_IDs: {null_disease_ids:,}")

    # ==========================================================
    # 4. REQUIRED FIELD VALIDATION
    # ==========================================================

    print()
    print("4. REQUIRED FIELD VALIDATION")
    print("-" * 70)

    cursor.execute("""
        SELECT COUNT(*)
        FROM diseases
        WHERE Disease_Name IS NULL
           OR TRIM(Disease_Name) = ''
    """)

    missing_names = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM diseases
        WHERE ICD10_Code IS NULL
           OR TRIM(ICD10_Code) = ''
    """)

    missing_icd = cursor.fetchone()[0]

    print(f"Missing Disease_Name : {missing_names:,}")
    print(f"Missing ICD10_Code   : {missing_icd:,}")

    # ==========================================================
    # 5. DUPLICATE DISEASE NAMES
    # ==========================================================

    print()
    print("5. DUPLICATE DISEASE NAMES")
    print("-" * 70)

    cursor.execute("""
        SELECT
            Disease_Name,
            COUNT(*) AS Disease_Count
        FROM diseases
        GROUP BY Disease_Name
        HAVING COUNT(*) > 1
        ORDER BY Disease_Name
    """)

    duplicate_names = cursor.fetchall()

    if duplicate_names:

        for disease_name, count in duplicate_names:
            print(f"{disease_name:<40} -> {count}")

        print()
        print("â„¹ï¸ Duplicate Disease_Name values are allowed.")
        print("   Disease_ID is the unique identifier.")

    else:

        print("No duplicate Disease_Name values found.")

    # ==========================================================
    # 6. DUPLICATE DISEASE IDs
    # ==========================================================

    print()
    print("6. DUPLICATE DISEASE IDs")
    print("-" * 70)

    cursor.execute("""
        SELECT
            Disease_ID,
            COUNT(*) AS Disease_Count
        FROM diseases
        GROUP BY Disease_ID
        HAVING COUNT(*) > 1
    """)

    duplicate_id_rows = cursor.fetchall()

    duplicate_id_groups = len(duplicate_id_rows)

    if duplicate_id_groups == 0:

        print("No duplicate Disease_IDs found.")

    else:

        print(f"âŒ Duplicate Disease_ID groups: {duplicate_id_groups}")

        for disease_id, count in duplicate_id_rows[:20]:
            print(f"{disease_id} -> {count}")

        checks_passed = False

    # ==========================================================
    # 7. DUPLICATE ICD10 CODES
    # ==========================================================

    print()
    print("7. DUPLICATE ICD10 CODES")
    print("-" * 70)

    cursor.execute("""
        SELECT
            ICD10_Code,
            COUNT(*) AS Code_Count
        FROM diseases
        WHERE ICD10_Code IS NOT NULL
        GROUP BY ICD10_Code
        HAVING COUNT(*) > 1
        ORDER BY ICD10_Code
    """)

    duplicate_icd_rows = cursor.fetchall()

    duplicate_icd_groups = len(duplicate_icd_rows)

    if duplicate_icd_groups == 0:

        print("No duplicate ICD10 codes found.")

    else:

        print(
            f"âŒ Duplicate ICD10 code groups: "
            f"{duplicate_icd_groups}"
        )

        for icd_code, count in duplicate_icd_rows[:20]:
            print(f"{icd_code} -> {count}")

        checks_passed = False

    # ==========================================================
    # 8. DISEASE TYPE VALIDATION
    # ==========================================================

    print()
    print("8. DISEASE TYPE VALIDATION")
    print("-" * 70)

    cursor.execute("""
        SELECT COUNT(*)
        FROM diseases
        WHERE Disease_Type IS NULL
    """)

    null_disease_type = cursor.fetchone()[0]

    print(f"NULL Disease_Type: {null_disease_type:,}")

    # ==========================================================
    # 9. DISEASE TYPE DISTRIBUTION
    # ==========================================================

    print()
    print("9. DISEASE TYPE DISTRIBUTION")
    print("-" * 70)

    cursor.execute("""
        SELECT
            Disease_Type,
            COUNT(*)
        FROM diseases
        GROUP BY Disease_Type
        ORDER BY Disease_Type
    """)

    disease_type_results = cursor.fetchall()

    for disease_type, count in disease_type_results:

        print(f"{str(disease_type):<20} : {count:,}")

    # ==========================================================
    # 10. DISEASE CATEGORY DISTRIBUTION
    # ==========================================================

    print()
    print("10. DISEASE CATEGORY DISTRIBUTION")
    print("-" * 70)

    cursor.execute("""
        SELECT
            Disease_Category,
            COUNT(*)
        FROM diseases
        GROUP BY Disease_Category
        ORDER BY Disease_Category
    """)

    category_results = cursor.fetchall()

    for category, count in category_results:

        print(f"{str(category):<25} : {count:,}")

    # ==========================================================
    # 11. SEVERITY DISTRIBUTION
    # ==========================================================

    print()
    print("11. SEVERITY DISTRIBUTION")
    print("-" * 70)

    cursor.execute("""
        SELECT
            Severity,
            COUNT(*)
        FROM diseases
        GROUP BY Severity
        ORDER BY Severity
    """)

    severity_results = cursor.fetchall()

    for severity, count in severity_results:

        print(f"{str(severity):<15} : {count:,}")

    # ==========================================================
    # 12. STATUS DISTRIBUTION
    # ==========================================================

    print()
    print("12. STATUS DISTRIBUTION")
    print("-" * 70)

    cursor.execute("""
        SELECT
            Status,
            COUNT(*)
        FROM diseases
        GROUP BY Status
        ORDER BY Status
    """)

    status_results = cursor.fetchall()

    for status, count in status_results:

        print(f"{str(status):<15} : {count:,}")

    # ==========================================================
    # 13. HOSPITALIZATION FLAG
    # ==========================================================

    print()
    print("13. HOSPITALIZATION FLAG")
    print("-" * 70)

    cursor.execute("""
        SELECT
            Requires_Hospitalization,
            COUNT(*)
        FROM diseases
        GROUP BY Requires_Hospitalization
        ORDER BY Requires_Hospitalization
    """)

    hospitalization_results = cursor.fetchall()

    for flag, count in hospitalization_results:

        label = "Yes" if flag == 1 else "No"

        print(f"{label:<10} : {count:,}")

    # ==========================================================
    # 14. CONTAGIOUS FLAG
    # ==========================================================

    print()
    print("14. CONTAGIOUS FLAG")
    print("-" * 70)

    cursor.execute("""
        SELECT
            Is_Contagious,
            COUNT(*)
        FROM diseases
        GROUP BY Is_Contagious
        ORDER BY Is_Contagious
    """)

    contagious_results = cursor.fetchall()

    for flag, count in contagious_results:

        label = "Yes" if flag == 1 else "No"

        print(f"{label:<10} : {count:,}")

    # ==========================================================
    # 15. SAMPLE DISEASE RECORDS
    # ==========================================================

    print()
    print("15. SAMPLE DISEASE RECORDS")
    print("-" * 70)

    cursor.execute("""
        SELECT
            Disease_ID,
            Disease_Name,
            ICD10_Code,
            Disease_Category,
            Disease_Type,
            Severity,
            Status
        FROM diseases
        ORDER BY Disease_Name, Disease_ID
        LIMIT 10
    """)

    sample_records = cursor.fetchall()

    for record in sample_records:

        print(record)

    # ==========================================================
    # FINAL VALIDATION
    # ==========================================================

    print()
    print("=" * 70)
    print("FINAL VALIDATION")
    print("=" * 70)

    # ----------------------------------------------------------
    # Total count
    # ----------------------------------------------------------

    if total_diseases != 250:

        print(
            f"âŒ Expected 250 diseases, "
            f"found {total_diseases:,}."
        )

        checks_passed = False

    else:

        print("âœ… Disease count = 250")

    # ----------------------------------------------------------
    # Unique Disease IDs
    # ----------------------------------------------------------

    if unique_disease_ids != total_diseases:

        print("âŒ Duplicate Disease_IDs detected.")

        checks_passed = False

    else:

        print("âœ… Disease_IDs are unique")

    # ----------------------------------------------------------
    # NULL Disease IDs
    # ----------------------------------------------------------

    if null_disease_ids != 0:

        print("âŒ NULL Disease_IDs detected.")

        checks_passed = False

    else:

        print("âœ… No NULL Disease_IDs")

    # ----------------------------------------------------------
    # Disease names
    # ----------------------------------------------------------

    if missing_names != 0:

        print("âŒ Missing Disease_Name values detected.")

        checks_passed = False

    else:

        print("âœ… Disease_Name values complete")

    # ----------------------------------------------------------
    # ICD codes
    # ----------------------------------------------------------

    if missing_icd != 0:

        print("âŒ Missing ICD10_Code values detected.")

        checks_passed = False

    else:

        print("âœ… ICD10_Code values complete")

    # ----------------------------------------------------------
    # Duplicate ICD codes
    # ----------------------------------------------------------

    if duplicate_icd_groups != 0:

        print("âŒ Duplicate ICD10_Code values detected.")

        checks_passed = False

    else:

        print("âœ… ICD10_Code values are unique")

    # ----------------------------------------------------------
    # Disease type
    # ----------------------------------------------------------

    if null_disease_type != 0:

        print("âŒ NULL Disease_Type values detected.")

        checks_passed = False

    else:

        print("âœ… Disease_Type values complete")

    # ----------------------------------------------------------
    # Final result
    # ----------------------------------------------------------

    print()

    if checks_passed:

        print("ðŸŽ‰ FINAL STATUS: PASSED")

    else:

        print("âš ï¸ FINAL STATUS: REVIEW REQUIRED")

    print("=" * 70)

    # ==========================================================
    # CLOSE CONNECTION
    # ==========================================================

    cursor.close()
    connection.close()

    print()
    print("Database connection closed.")
    print("Disease validation finished.")


# ==============================================================
# RUN
# ==============================================================

if __name__ == "__main__":
    main()
