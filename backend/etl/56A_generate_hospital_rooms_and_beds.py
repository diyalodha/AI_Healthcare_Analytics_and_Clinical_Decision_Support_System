import os
import sys
import uuid
import random
from decimal import Decimal

import mysql.connector


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = r"E:\College Final Year\Major Project\Healthcare_AI_Project"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": "healthcare_ai_db",
}

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

BATCH_SIZE = 5000


# ============================================================
# DEPARTMENT-SPECIFIC ROOM CONFIGURATION
# ============================================================

DEPARTMENT_CONFIG = {
    "Administration": {
        "prefix": "ADMIN",
        "room_type": "General",
        "capacity": 2,
        "daily_charge": Decimal("800.00"),
    },
    "Blood Bank": {
        "prefix": "BLOOD",
        "room_type": "General",
        "capacity": 2,
        "daily_charge": Decimal("700.00"),
    },
    "Cardiology": {
        "prefix": "CARD",
        "room_type": "Private",
        "capacity": 1,
        "daily_charge": Decimal("3500.00"),
    },
    "Dentistry": {
        "prefix": "DENT",
        "room_type": "General",
        "capacity": 2,
        "daily_charge": Decimal("1200.00"),
    },
    "Dermatology": {
        "prefix": "DERM",
        "room_type": "Private",
        "capacity": 1,
        "daily_charge": Decimal("2500.00"),
    },
    "Emergency Medicine": {
        "prefix": "EMER",
        "room_type": "Emergency",
        "capacity": 2,
        "daily_charge": Decimal("3000.00"),
    },
    "ENT": {
        "prefix": "ENT",
        "room_type": "General",
        "capacity": 2,
        "daily_charge": Decimal("1800.00"),
    },
    "Gastroenterology": {
        "prefix": "GASTRO",
        "room_type": "Semi-Private",
        "capacity": 2,
        "daily_charge": Decimal("2800.00"),
    },
    "General Medicine": {
        "prefix": "GENMED",
        "room_type": "General",
        "capacity": 4,
        "daily_charge": Decimal("1500.00"),
    },
    "Gynecology": {
        "prefix": "GYNE",
        "room_type": "Semi-Private",
        "capacity": 2,
        "daily_charge": Decimal("2500.00"),
    },
    "ICU": {
        "prefix": "ICU",
        "room_type": "ICU",
        "capacity": 1,
        "daily_charge": Decimal("8000.00"),
    },
    "Nephrology": {
        "prefix": "NEPH",
        "room_type": "Semi-Private",
        "capacity": 2,
        "daily_charge": Decimal("3000.00"),
    },
    "Neurology": {
        "prefix": "NEURO",
        "room_type": "Private",
        "capacity": 1,
        "daily_charge": Decimal("3500.00"),
    },
    "Obstetrics": {
        "prefix": "OBS",
        "room_type": "Semi-Private",
        "capacity": 2,
        "daily_charge": Decimal("3000.00"),
    },
    "Oncology": {
        "prefix": "ONCO",
        "room_type": "Private",
        "capacity": 1,
        "daily_charge": Decimal("4000.00"),
    },
    "Operation Theatre": {
        "prefix": "OT",
        "room_type": "Operation Theater",
        "capacity": 1,
        "daily_charge": Decimal("10000.00"),
    },
    "Ophthalmology": {
        "prefix": "OPHTH",
        "room_type": "Private",
        "capacity": 1,
        "daily_charge": Decimal("2500.00"),
    },
    "Orthopedics": {
        "prefix": "ORTHO",
        "room_type": "Semi-Private",
        "capacity": 2,
        "daily_charge": Decimal("3000.00"),
    },
    "Pathology Laboratory": {
        "prefix": "PATH",
        "room_type": "General",
        "capacity": 2,
        "daily_charge": Decimal("1200.00"),
    },
    "Pediatrics": {
        "prefix": "PEDIA",
        "room_type": "PICU",
        "capacity": 1,
        "daily_charge": Decimal("5000.00"),
    },
    "Pharmacy": {
        "prefix": "PHARM",
        "room_type": "General",
        "capacity": 2,
        "daily_charge": Decimal("1000.00"),
    },
    "Physiotherapy": {
        "prefix": "PHYSIO",
        "room_type": "General",
        "capacity": 2,
        "daily_charge": Decimal("1500.00"),
    },
    "Psychiatry": {
        "prefix": "PSYCH",
        "room_type": "Private",
        "capacity": 1,
        "daily_charge": Decimal("2800.00"),
    },
    "Pulmonology": {
        "prefix": "PULMO",
        "room_type": "Semi-Private",
        "capacity": 2,
        "daily_charge": Decimal("3000.00"),
    },
    "Radiology": {
        "prefix": "RAD",
        "room_type": "General",
        "capacity": 2,
        "daily_charge": Decimal("1800.00"),
    },
}


# ============================================================
# BED TYPE RULES
# ============================================================

def get_bed_type(room_type, bed_number):
    """
    Determine a clinically appropriate bed type.
    """

    if room_type == "ICU":
        return "ICU"

    if room_type == "PICU":
        return "Pediatric"

    if room_type == "Emergency":
        return "Standard"

    if room_type == "Operation Theater":
        return "Electric"

    if room_type in ("Private", "Deluxe"):
        return "Electric"

    return "Standard"


def is_isolation_bed(room_type):
    """
    Isolation beds are mainly associated with ICU/PICU/emergency
    environments in this synthetic dataset.
    """

    if room_type in ("ICU", "PICU", "Isolation"):
        return 1

    return 0


def ventilator_available(room_type, bed_type):
    """
    Ventilator availability is primarily associated with ICU beds.
    """

    if room_type == "ICU":
        return 1

    if bed_type == "Ventilator":
        return 1

    return 0


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
        )

        print("Database connection successful.")
        return connection

    except mysql.connector.Error as e:
        print(f"Database connection failed: {e}")
        sys.exit(1)


# ============================================================
# LOAD DEPARTMENTS
# ============================================================

def load_departments(cursor):

    cursor.execute("""
        SELECT Department_ID, Department_Name
        FROM departments
        ORDER BY Department_Name
    """)

    rows = cursor.fetchall()

    departments = {}

    for department_id, department_name in rows:
        departments[department_name] = department_id

    print(f"Departments found in database: {len(departments)}")

    return departments


# ============================================================
# CLEAR EXISTING MASTER DATA
# ============================================================

def clear_existing_data(cursor, connection):

    cursor.execute("SELECT COUNT(*) FROM beds")
    bed_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM hospital_rooms")
    room_count = cursor.fetchone()[0]

    print()
    print("Existing master data:")
    print(f"  Hospital rooms : {room_count}")
    print(f"  Beds           : {bed_count}")

    if room_count == 0 and bed_count == 0:
        print("No existing room/bed data to clear.")
        return

    print()
    print("Clearing existing hospital room and bed master data...")

    # Beds must be deleted first because they reference rooms.
    cursor.execute("DELETE FROM beds")

    # Rooms can now be deleted.
    cursor.execute("DELETE FROM hospital_rooms")

    connection.commit()

    print("Existing room/bed data cleared successfully.")


# ============================================================
# INSERT ROOMS
# ============================================================

def insert_rooms(cursor, connection, departments):

    room_sql = """
        INSERT INTO hospital_rooms (
            Room_ID,
            Department_ID,
            Room_Code,
            Room_Number,
            Room_Type,
            Floor_Number,
            Capacity,
            Current_Occupancy,
            Daily_Charges,
            Room_Status,
            Description,
            Is_Active,
            Record_Version,
            Created_By,
            Updated_By
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
    """

    batch = []
    total_rooms = 0

    for department_name, config in DEPARTMENT_CONFIG.items():

        if department_name not in departments:
            raise RuntimeError(
                f"Department '{department_name}' was not found in database."
            )

        department_id = departments[department_name]

        for room_number in range(101, 1000):

            room_id = str(uuid.uuid4())

            room_code = f"{config['prefix']}-{room_number}"

            floor_number = ((room_number - 101) // 100) + 1

            room_type = config["room_type"]
            capacity = config["capacity"]
            daily_charge = config["daily_charge"]

            description = (
                f"{room_type} room {room_number} "
                f"for {department_name} department."
            )

            row = (
                room_id,
                department_id,
                room_code,
                str(room_number),
                room_type,
                floor_number,
                capacity,
                0,
                daily_charge,
                "Available",
                description,
                1,
                1,
                "56A_SCRIPT",
                "56A_SCRIPT",
            )

            batch.append(row)
            total_rooms += 1

            if len(batch) >= BATCH_SIZE:

                cursor.executemany(room_sql, batch)
                connection.commit()

                print(f"Rooms inserted: {total_rooms:,}")

                batch.clear()

    if batch:
        cursor.executemany(room_sql, batch)
        connection.commit()

        print(f"Rooms inserted: {total_rooms:,}")

    return total_rooms


# ============================================================
# LOAD ROOM IDS FOR BED GENERATION
# ============================================================

def load_rooms(cursor):

    cursor.execute("""
        SELECT
            Room_ID,
            Room_Number,
            Room_Type,
            Capacity
        FROM hospital_rooms
        ORDER BY Room_ID
    """)

    rooms = cursor.fetchall()

    print(f"Rooms available for bed generation: {len(rooms):,}")

    return rooms


# ============================================================
# INSERT BEDS
# ============================================================

def insert_beds(cursor, connection, rooms):

    bed_sql = """
        INSERT INTO beds (
            Bed_ID,
            Room_ID,
            Patient_ID,
            Bed_Number,
            Bed_Code,
            Bed_Type,
            Bed_Status,
            Occupied_From,
            Occupied_To,
            Last_Cleaned_Date,
            Is_Isolation_Bed,
            Ventilator_Available,
            Bed_Condition,
            Notes,
            Is_Active,
            Record_Version,
            Created_By,
            Updated_By
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s
        )
    """

    batch = []
    total_beds = 0

    for room_id, room_number, room_type, capacity in rooms:

        for bed_number in range(1, capacity + 1):

            bed_id = str(uuid.uuid4())

            bed_number_text = str(bed_number)

            bed_code = f"{room_id[:8]}-B{bed_number}"

            bed_type = get_bed_type(room_type, bed_number)

            isolation = is_isolation_bed(room_type)

            ventilator = ventilator_available(room_type, bed_type)

            row = (
                bed_id,
                room_id,
                None,
                bed_number_text,
                bed_code,
                bed_type,
                "Available",
                None,
                None,
                None,
                isolation,
                ventilator,
                "Good",
                f"Initial master bed record for {room_type} room.",
                1,
                1,
                "56A_SCRIPT",
                "56A_SCRIPT",
            )

            batch.append(row)
            total_beds += 1

            if len(batch) >= BATCH_SIZE:

                cursor.executemany(bed_sql, batch)
                connection.commit()

                print(f"Beds inserted: {total_beds:,}")

                batch.clear()

    if batch:
        cursor.executemany(bed_sql, batch)
        connection.commit()

        print(f"Beds inserted: {total_beds:,}")

    return total_beds


# ============================================================
# VALIDATION
# ============================================================

def validate(cursor, expected_rooms, expected_beds):

    print()
    print("=" * 70)
    print("56A VALIDATION")
    print("=" * 70)

    cursor.execute("""
        SELECT COUNT(*)
        FROM hospital_rooms
    """)

    actual_rooms = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM beds
    """)

    actual_beds = cursor.fetchone()[0]

    print(f"Expected rooms : {expected_rooms:,}")
    print(f"Actual rooms   : {actual_rooms:,}")
    print()

    print(f"Expected beds  : {expected_beds:,}")
    print(f"Actual beds    : {actual_beds:,}")

    # Room department validation
    cursor.execute("""
        SELECT COUNT(*)
        FROM hospital_rooms hr
        LEFT JOIN departments d
            ON hr.Department_ID = d.Department_ID
        WHERE d.Department_ID IS NULL
    """)

    orphan_rooms = cursor.fetchone()[0]

    # Bed room validation
    cursor.execute("""
        SELECT COUNT(*)
        FROM beds b
        LEFT JOIN hospital_rooms hr
            ON b.Room_ID = hr.Room_ID
        WHERE hr.Room_ID IS NULL
    """)

    orphan_beds = cursor.fetchone()[0]

    # Room number range
    cursor.execute("""
        SELECT
            MIN(CAST(Room_Number AS UNSIGNED)),
            MAX(CAST(Room_Number AS UNSIGNED)),
            COUNT(DISTINCT Room_Number)
        FROM hospital_rooms
    """)

    min_room, max_room, unique_room_numbers = cursor.fetchone()

    # Room codes
    cursor.execute("""
        SELECT COUNT(*), COUNT(DISTINCT Room_Code)
        FROM hospital_rooms
    """)

    room_code_total, unique_room_codes = cursor.fetchone()

    # Bed codes
    cursor.execute("""
        SELECT COUNT(*), COUNT(DISTINCT Bed_Code)
        FROM beds
    """)

    bed_code_total, unique_bed_codes = cursor.fetchone()

    # Capacity validation
    cursor.execute("""
        SELECT COUNT(*)
        FROM hospital_rooms
        WHERE Capacity <= 0
           OR Current_Occupancy < 0
           OR Current_Occupancy > Capacity
    """)

    invalid_capacity = cursor.fetchone()[0]

    # Bed status validation
    cursor.execute("""
        SELECT COUNT(*)
        FROM beds
        WHERE Bed_Status <> 'Available'
    """)

    non_available_beds = cursor.fetchone()[0]

    print()
    print("Validation checks:")
    print(f"  Orphan rooms              : {orphan_rooms}")
    print(f"  Orphan beds               : {orphan_beds}")
    print(f"  Minimum room number       : {min_room}")
    print(f"  Maximum room number       : {max_room}")
    print(f"  Unique room numbers       : {unique_room_numbers}")
    print(f"  Room codes                : {room_code_total:,}")
    print(f"  Unique room codes         : {unique_room_codes:,}")
    print(f"  Bed codes                 : {bed_code_total:,}")
    print(f"  Unique bed codes          : {unique_bed_codes:,}")
    print(f"  Invalid room capacity     : {invalid_capacity}")
    print(f"  Non-available beds        : {non_available_beds}")

    # Department-wise room counts
    cursor.execute("""
        SELECT
            d.Department_Name,
            COUNT(hr.Room_ID) AS Room_Count
        FROM departments d
        LEFT JOIN hospital_rooms hr
            ON d.Department_ID = hr.Department_ID
        GROUP BY d.Department_ID, d.Department_Name
        ORDER BY d.Department_Name
    """)

    department_rows = cursor.fetchall()

    print()
    print("Rooms by department:")
    print("-" * 50)

    department_failure = False

    for department_name, room_count in department_rows:

        print(f"  {department_name:<25} {room_count:>5}")

        if room_count != 899:
            department_failure = True

    # Room type distribution
    cursor.execute("""
        SELECT
            Room_Type,
            COUNT(*) AS Room_Count
        FROM hospital_rooms
        GROUP BY Room_Type
        ORDER BY Room_Type
    """)

    room_types = cursor.fetchall()

    print()
    print("Room type distribution:")
    print("-" * 40)

    for room_type, count in room_types:
        print(f"  {room_type:<20} {count:>8,}")

    # Bed type distribution
    cursor.execute("""
        SELECT
            Bed_Type,
            COUNT(*) AS Bed_Count
        FROM beds
        GROUP BY Bed_Type
        ORDER BY Bed_Type
    """)

    bed_types = cursor.fetchall()

    print()
    print("Bed type distribution:")
    print("-" * 40)

    for bed_type, count in bed_types:
        print(f"  {bed_type:<20} {count:>8,}")

    print()
    print("=" * 70)

    passed = (
        actual_rooms == expected_rooms
        and actual_beds == expected_beds
        and orphan_rooms == 0
        and orphan_beds == 0
        and min_room == 101
        and max_room == 999
        and unique_room_numbers == 899
        and room_code_total == unique_room_codes
        and bed_code_total == unique_bed_codes
        and invalid_capacity == 0
        and non_available_beds == 0
        and not department_failure
    )

    if passed:
        print("FINAL STATUS: PASSED")
    else:
        print("FINAL STATUS: FAILED")

    print("=" * 70)

    return passed


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("STEP 56A - HOSPITAL ROOMS & BEDS MASTER DATA")
    print("=" * 70)
    print()

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ----------------------------------------------------
        # 1. Load departments
        # ----------------------------------------------------

        departments = load_departments(cursor)

        if len(departments) != 25:
            raise RuntimeError(
                f"Expected 25 departments, found {len(departments)}."
            )

        # ----------------------------------------------------
        # 2. Clear existing room/bed data
        # ----------------------------------------------------

        clear_existing_data(cursor, connection)

        # ----------------------------------------------------
        # 3. Generate rooms
        # ----------------------------------------------------

        print()
        print("Generating hospital rooms...")
        print("Expected rooms: 25 × 899 = 22,475")
        print()

        expected_rooms = len(DEPARTMENT_CONFIG) * 899

        rooms_inserted = insert_rooms(
            cursor,
            connection,
            departments
        )

        if rooms_inserted != expected_rooms:
            raise RuntimeError(
                f"Expected {expected_rooms} rooms, "
                f"but inserted {rooms_inserted}."
            )

        # ----------------------------------------------------
        # 4. Load rooms
        # ----------------------------------------------------

        rooms = load_rooms(cursor)

        # ----------------------------------------------------
        # 5. Generate beds
        # ----------------------------------------------------

        print()
        print("Generating beds...")

        expected_beds = sum(
            config["capacity"] * 899
            for config in DEPARTMENT_CONFIG.values()
        )

        beds_inserted = insert_beds(
            cursor,
            connection,
            rooms
        )

        if beds_inserted != expected_beds:
            raise RuntimeError(
                f"Expected {expected_beds} beds, "
                f"but inserted {beds_inserted}."
            )

        # ----------------------------------------------------
        # 6. Validation
        # ----------------------------------------------------

        success = validate(
            cursor,
            expected_rooms,
            expected_beds
        )

        if not success:
            sys.exit(1)

    except Exception as e:

        connection.rollback()

        print()
        print("=" * 70)
        print("ERROR")
        print("=" * 70)
        print(e)
        print("=" * 70)

        sys.exit(1)

    finally:

        cursor.close()
        connection.close()

        print()
        print("Database connection closed.")


if __name__ == "__main__":
    main()