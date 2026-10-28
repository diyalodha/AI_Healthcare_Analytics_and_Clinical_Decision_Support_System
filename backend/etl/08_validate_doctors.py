import os
import mysql.connector
from mysql.connector import Error


# ============================================================
# CONFIGURATION
# ============================================================

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD")
DB_NAME = "healthcare_ai_db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

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


# ============================================================
# MAIN VALIDATION
# ============================================================

def main():

    print("=" * 70)
    print("STEP 08 - VALIDATE DOCTORS")
    print("=" * 70)

    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    print("âœ… Connected to MySQL")
    print()

    # --------------------------------------------------------
    # 1. Total doctors
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM doctors
    """)

    total_doctors = cursor.fetchone()[0]

    print(f"Total doctors                  : {total_doctors:,}")

    # --------------------------------------------------------
    # 2. Unique Doctor IDs
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(DISTINCT Doctor_ID)
        FROM doctors
    """)

    unique_doctor_ids = cursor.fetchone()[0]

    print(
        f"Unique Doctor IDs              : "
        f"{unique_doctor_ids:,}"
    )

    # --------------------------------------------------------
    # 3. NULL Doctor IDs
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM doctors
        WHERE Doctor_ID IS NULL
    """)

    null_doctor_ids = cursor.fetchone()[0]

    print(
        f"NULL Doctor IDs                : "
        f"{null_doctor_ids:,}"
    )

    # --------------------------------------------------------
    # 4. Missing required fields
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM doctors
        WHERE First_Name IS NULL
           OR Last_Name IS NULL
           OR Gender IS NULL
           OR Medical_License_No IS NULL
           OR Qualification IS NULL
           OR Specialization IS NULL
           OR Department_ID IS NULL
           OR Joining_Date IS NULL
    """)

    missing_required = cursor.fetchone()[0]

    print(
        f"Missing required fields        : "
        f"{missing_required:,}"
    )

    # --------------------------------------------------------
    # 5. Duplicate Medical License
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT Medical_License_No
            FROM doctors
            GROUP BY Medical_License_No
            HAVING COUNT(*) > 1
        ) AS duplicates
    """)

    duplicate_licenses = cursor.fetchone()[0]

    print(
        f"Duplicate license groups       : "
        f"{duplicate_licenses:,}"
    )

    # --------------------------------------------------------
    # 6. Duplicate phones
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT Phone
            FROM doctors
            WHERE Phone IS NOT NULL
            GROUP BY Phone
            HAVING COUNT(*) > 1
        ) AS duplicates
    """)

    duplicate_phones = cursor.fetchone()[0]

    print(
        f"Duplicate phone groups         : "
        f"{duplicate_phones:,}"
    )

    # --------------------------------------------------------
    # 7. Duplicate emails
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT Email
            FROM doctors
            WHERE Email IS NOT NULL
            GROUP BY Email
            HAVING COUNT(*) > 1
        ) AS duplicates
    """)

    duplicate_emails = cursor.fetchone()[0]

    print(
        f"Duplicate email groups         : "
        f"{duplicate_emails:,}"
    )

    # --------------------------------------------------------
    # 8. Invalid Department references
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM doctors d
        LEFT JOIN departments dep
            ON d.Department_ID = dep.Department_ID
        WHERE dep.Department_ID IS NULL
    """)

    invalid_departments = cursor.fetchone()[0]

    print(
        f"Invalid Department_ID          : "
        f"{invalid_departments:,}"
    )

    # --------------------------------------------------------
    # 9. Gender distribution
    # --------------------------------------------------------

    print()
    print("Gender distribution:")
    print("-" * 50)

    cursor.execute("""
        SELECT Gender, COUNT(*)
        FROM doctors
        GROUP BY Gender
        ORDER BY Gender
    """)

    for gender, count in cursor.fetchall():

        print(
            f"  {gender:<15} : {count:,}"
        )

    # --------------------------------------------------------
    # 10. Employment type distribution
    # --------------------------------------------------------

    print()
    print("Employment type distribution:")
    print("-" * 50)

    cursor.execute("""
        SELECT Employment_Type, COUNT(*)
        FROM doctors
        GROUP BY Employment_Type
        ORDER BY Employment_Type
    """)

    for employment_type, count in cursor.fetchall():

        print(
            f"  {employment_type:<15} : {count:,}"
        )

    # --------------------------------------------------------
    # 11. Shift distribution
    # --------------------------------------------------------

    print()
    print("Shift distribution:")
    print("-" * 50)

    cursor.execute("""
        SELECT Shift, COUNT(*)
        FROM doctors
        GROUP BY Shift
        ORDER BY Shift
    """)

    for shift, count in cursor.fetchall():

        print(
            f"  {shift:<15} : {count:,}"
        )

    # --------------------------------------------------------
    # 12. Status distribution
    # --------------------------------------------------------

    print()
    print("Status distribution:")
    print("-" * 50)

    cursor.execute("""
        SELECT Status, COUNT(*)
        FROM doctors
        GROUP BY Status
        ORDER BY Status
    """)

    for status, count in cursor.fetchall():

        print(
            f"  {status:<15} : {count:,}"
        )

    # --------------------------------------------------------
    # 13. Doctors per department
    # --------------------------------------------------------

    print()
    print("Doctors per department:")
    print("-" * 50)

    cursor.execute("""
        SELECT
            dep.Department_Name,
            COUNT(d.Doctor_ID) AS Doctor_Count
        FROM departments dep
        LEFT JOIN doctors d
            ON dep.Department_ID = d.Department_ID
        GROUP BY
            dep.Department_ID,
            dep.Department_Name
        ORDER BY Doctor_Count DESC
    """)

    department_results = cursor.fetchall()

    for department_name, doctor_count in department_results:

        print(
            f"  {department_name:<30} : "
            f"{doctor_count:,}"
        )

    # --------------------------------------------------------
    # 14. Doctors with invalid experience
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM doctors
        WHERE Years_of_Experience < 0
    """)

    invalid_experience = cursor.fetchone()[0]

    print()
    print(
        f"Negative experience values     : "
        f"{invalid_experience:,}"
    )

    # --------------------------------------------------------
    # 15. Doctors with invalid consultation fee
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM doctors
        WHERE Consultation_Fee < 0
    """)

    invalid_fees = cursor.fetchone()[0]

    print(
        f"Negative consultation fees     : "
        f"{invalid_fees:,}"
    )

    # --------------------------------------------------------
    # FINAL VALIDATION
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("VALIDATION RESULT")
    print("=" * 70)

    checks_passed = True

    if total_doctors != 1997:
        print(
            f"âš ï¸ Expected 1,997 doctors, "
            f"found {total_doctors:,}"
        )
        checks_passed = False
    else:
        print("âœ… Doctor count = 1,997")

    if unique_doctor_ids != total_doctors:
        print("âŒ Duplicate Doctor_IDs found")
        checks_passed = False
    else:
        print("âœ… Doctor_IDs are unique")

    if null_doctor_ids != 0:
        print("âŒ NULL Doctor_IDs found")
        checks_passed = False
    else:
        print("âœ… No NULL Doctor_IDs")

    if missing_required != 0:
        print("âŒ Missing required doctor fields found")
        checks_passed = False
    else:
        print("âœ… Required fields complete")

    if duplicate_licenses != 0:
        print("âŒ Duplicate medical licenses found")
        checks_passed = False
    else:
        print("âœ… Medical licenses are unique")

    if duplicate_phones != 0:
        print("âŒ Duplicate phone numbers found")
        checks_passed = False
    else:
        print("âœ… Phone numbers are unique")

    if duplicate_emails != 0:
        print("âŒ Duplicate emails found")
        checks_passed = False
    else:
        print("âœ… Email addresses are unique")

    if invalid_departments != 0:
        print("âŒ Invalid Department_ID references found")
        checks_passed = False
    else:
        print("âœ… All Department_ID references are valid")

    if invalid_experience != 0:
        print("âŒ Negative experience values found")
        checks_passed = False
    else:
        print("âœ… Experience values valid")

    if invalid_fees != 0:
        print("âŒ Negative consultation fees found")
        checks_passed = False
    else:
        print("âœ… Consultation fees valid")

    print()

    if checks_passed:
        print("ðŸŽ‰ FINAL STATUS: PASSED")
    else:
        print("âš ï¸ FINAL STATUS: FAILED - REVIEW REQUIRED")

    print("=" * 70)

    cursor.close()
    connection.close()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()