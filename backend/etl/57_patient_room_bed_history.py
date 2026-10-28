import os
import sys
import uuid
import heapq
from datetime import datetime, time
from collections import defaultdict

import mysql.connector


# ============================================================
# STEP 57
# PATIENT ROOM / BED HISTORY
# ============================================================

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_NAME = "healthcare_ai_db"

BATCH_SIZE = 5000
SCRIPT_NAME = "57_patient_room_bed_history.py"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    password = os.getenv("MYSQL_PASSWORD")

    if not password:
        raise RuntimeError(
            "MYSQL_PASSWORD environment variable is not set."
        )

    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=password,
        database=DB_NAME,
        autocommit=False
    )


# ============================================================
# HELPERS
# ============================================================

def normalize_end_date(discharge_date):

    if discharge_date is None:
        return None

    return datetime.combine(
        discharge_date,
        time(23, 59, 59)
    )


def care_unit_from_room_type(room_type):

    mapping = {
        "General": "General Ward",
        "Semi-Private": "Semi-Private",
        "Private": "Private Room",
        "Deluxe": "Deluxe Room",
        "ICU": "ICU",
        "NICU": "NICU",
        "PICU": "PICU",
        "Emergency": "Emergency Bay",
        "Isolation": "Isolation Ward",
        "Operation Theater": "Post-Op Recovery"
    }

    return mapping.get(room_type, "Other")


def allocation_status(current_status):

    if current_status == "Discharged":
        return "Discharged"

    if current_status == "Transferred":
        return "Transferred"

    return "Active"


def calculate_hours(start_dt, end_dt):

    if end_dt <= start_dt:
        return 0.0

    seconds = (end_dt - start_dt).total_seconds()

    return round(seconds / 3600.0, 2)


# ============================================================
# LOAD BEDS
# ============================================================

def load_beds(cursor):

    cursor.execute("""
        SELECT
            Bed_ID,
            Room_ID,
            Bed_Number
        FROM beds
        ORDER BY Room_ID, Bed_Number
    """)

    beds_by_room = defaultdict(list)

    for bed_id, room_id, bed_number in cursor.fetchall():

        beds_by_room[room_id].append({
            "Bed_ID": bed_id,
            "Bed_Number": bed_number
        })

    return beds_by_room


# ============================================================
# LOAD ADMISSIONS
# ============================================================

def load_admissions(cursor):

    cursor.execute("""
        SELECT
            a.Admission_ID,
            a.Patient_ID,
            a.Department_ID,
            a.Admission_Date,
            a.Actual_Discharge_Date,
            a.Length_of_Stay,
            a.Current_Status,
            a.Room_Number,

            hr.Room_ID,
            hr.Room_Type,
            hr.Floor_Number,
            hr.Capacity,
            hr.Daily_Charges,

            d.Department_Name

        FROM admissions a

        INNER JOIN hospital_rooms hr
            ON a.Department_ID = hr.Department_ID
           AND a.Room_Number = hr.Room_Number

        INNER JOIN departments d
            ON a.Department_ID = d.Department_ID

        ORDER BY
            a.Department_ID,
            CAST(a.Room_Number AS UNSIGNED),
            a.Admission_Date,
            a.Admission_ID
    """)

    return cursor.fetchall()


# ============================================================
# HISTORICAL BED ALLOCATION
# ============================================================

def allocate_beds(admissions, beds_by_room):

    admissions_by_room = defaultdict(list)

    for row in admissions:

        room_id = row[8]

        admissions_by_room[room_id].append(row)

    allocations = []

    total_conflicts = 0
    rooms_with_overflow = set()

    room_counter = 0

    for room_id, room_admissions in admissions_by_room.items():

        room_counter += 1

        room_admissions.sort(
            key=lambda x: (x[3], x[0])
        )

        physical_beds = beds_by_room.get(
            room_id,
            []
        )

        if not physical_beds:

            raise RuntimeError(
                f"Room {room_id} has no physical beds."
            )

        # ----------------------------------------------------
        # Heap:
        #
        # (previous_end_datetime, physical_bed_index)
        # ----------------------------------------------------

        occupied = []

        # Physical beds that haven't been used yet
        unused_indexes = list(
            range(len(physical_beds))
        )

        # Number of overflow beds created for this room
        overflow_counter = 0

        for row in room_admissions:

            (
                admission_id,
                patient_id,
                department_id,
                admission_dt,
                discharge_date,
                length_of_stay,
                current_status,
                room_number,
                db_room_id,
                room_type,
                floor_number,
                capacity,
                daily_charge,
                department_name
            ) = row

            end_dt = normalize_end_date(
                discharge_date
            )

            selected_bed = None
            selected_bed_number = None
            selected_bed_id = None

            # ------------------------------------------------
            # Reuse a physical bed if available
            # ------------------------------------------------

            if occupied:

                earliest_end, bed_index = occupied[0]

                if earliest_end <= admission_dt:

                    heapq.heappop(occupied)

                    selected_bed = physical_beds[
                        bed_index
                    ]

            # ------------------------------------------------
            # Otherwise use a never-used physical bed
            # ------------------------------------------------

            if selected_bed is None:

                if unused_indexes:

                    bed_index = unused_indexes.pop(0)

                    selected_bed = physical_beds[
                        bed_index
                    ]

            # ------------------------------------------------
            # If physical capacity is exhausted
            # ------------------------------------------------

            if selected_bed is None:

                overflow_counter += 1
                total_conflicts += 1

                rooms_with_overflow.add(room_id)

                selected_bed_id = None

                selected_bed_number = (
                    f"OVERFLOW-{overflow_counter:02d}"
                )

                # We intentionally DO NOT insert this
                # overflow bed into the beds table.

            else:

                selected_bed_id = selected_bed["Bed_ID"]
                selected_bed_number = selected_bed["Bed_Number"]

                # Find its index again
                bed_index = physical_beds.index(
                    selected_bed
                )

                heapq.heappush(
                    occupied,
                    (
                        end_dt,
                        bed_index
                    )
                )

            allocations.append({
                "Admission_ID": admission_id,
                "Patient_ID": patient_id,
                "Department_ID": department_id,
                "Room_ID": db_room_id,
                "Room_Number": room_number,
                "Room_Type": room_type,
                "Floor_Number": floor_number,
                "Bed_ID": selected_bed_id,
                "Bed_Number": selected_bed_number,
                "Department_Name": department_name,
                "Admission_Date": admission_dt,
                "Discharge_Date": discharge_date,
                "Length_of_Stay": length_of_stay,
                "Current_Status": current_status,
                "Daily_Charge": daily_charge
            })

        if room_counter % 1000 == 0:

            print(
                f"   Processed rooms: "
                f"{room_counter:,}"
            )

    print()
    print(
        f"Rooms processed       : {room_counter:,}"
    )

    print(
        f"Rooms with overflow   : "
        f"{len(rooms_with_overflow):,}"
    )

    print(
        f"Overflow allocations  : "
        f"{total_conflicts:,}"
    )

    return allocations


# ============================================================
# INSERT HISTORY
# ============================================================

def insert_history(cursor, allocations):

    sql = """
        INSERT INTO patient_room_bed_history (
            Allocation_ID,
            Patient_ID,
            Admission_ID,
            Department_ID,
            Care_Unit_Type,
            Ward_Name,
            Room_Number,
            Bed_Number,
            Floor_Number,
            Allocated_From,
            Allocated_To,
            Length_Of_Stay_Hours,
            Allocation_Status,
            Transfer_Reason,
            Daily_Bed_Charge,
            Total_Bed_Cost,
            Attending_Nurse_Notes,
            Clinical_Remarks,
            Data_Source,
            Created_By,
            Updated_By
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    batch = []
    inserted = 0

    total = len(allocations)

    for allocation in allocations:

        start_dt = allocation["Admission_Date"]

        end_dt = normalize_end_date(
            allocation["Discharge_Date"]
        )

        stay_hours = calculate_hours(
            start_dt,
            end_dt
        )

        daily_charge = float(
            allocation["Daily_Charge"] or 0
        )

        total_cost = round(
            daily_charge *
            (stay_hours / 24.0),
            2
        )

        care_unit = care_unit_from_room_type(
            allocation["Room_Type"]
        )

        status = allocation_status(
            allocation["Current_Status"]
        )

        row = (
            str(uuid.uuid4()),

            allocation["Patient_ID"],

            allocation["Admission_ID"],

            allocation["Department_ID"],

            care_unit,

            allocation["Department_Name"],

            allocation["Room_Number"],

            allocation["Bed_Number"],

            str(allocation["Floor_Number"])
            if allocation["Floor_Number"] is not None
            else None,

            start_dt,

            end_dt,

            stay_hours,

            status,

            "Initial Admission",

            daily_charge,

            total_cost,

            None,

            None,

            "Synthetic",

            SCRIPT_NAME,

            SCRIPT_NAME
        )

        batch.append(row)

        if len(batch) >= BATCH_SIZE:

            cursor.executemany(
                sql,
                batch
            )

            inserted += len(batch)

            batch.clear()

            print(
                f"   Inserted: "
                f"{inserted:,}/{total:,}"
            )

    if batch:

        cursor.executemany(
            sql,
            batch
        )

        inserted += len(batch)

    return inserted


# ============================================================
# VALIDATION
# ============================================================

def validate(cursor, expected):

    print()
    print("=" * 70)
    print("STEP 57 VALIDATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Total
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM patient_room_bed_history
    """)

    total = cursor.fetchone()[0]

    print(
        f"Expected records : {expected:,}"
    )

    print(
        f"Actual records   : {total:,}"
    )

    # --------------------------------------------------------
    # Unique admissions
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(DISTINCT Admission_ID)
        FROM patient_room_bed_history
    """)

    unique_admissions = cursor.fetchone()[0]

    print(
        f"Unique admissions: {unique_admissions:,}"
    )

    # --------------------------------------------------------
    # Unique patients
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(DISTINCT Patient_ID)
        FROM patient_room_bed_history
    """)

    unique_patients = cursor.fetchone()[0]

    print(
        f"Unique patients  : {unique_patients:,}"
    )

    # --------------------------------------------------------
    # NULL checks
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            SUM(Patient_ID IS NULL),
            SUM(Admission_ID IS NULL),
            SUM(Department_ID IS NULL),
            SUM(Room_Number IS NULL),
            SUM(Bed_Number IS NULL),
            SUM(Allocated_From IS NULL),
            SUM(Daily_Bed_Charge IS NULL),
            SUM(Data_Source IS NULL)
        FROM patient_room_bed_history
    """)

    nulls = cursor.fetchone()

    print()
    print("NULL CHECKS")

    labels = [
        "Patient_ID",
        "Admission_ID",
        "Department_ID",
        "Room_Number",
        "Bed_Number",
        "Allocated_From",
        "Daily_Bed_Charge",
        "Data_Source"
    ]

    for label, value in zip(labels, nulls):

        print(
            f"{label:<20}: {value:,}"
        )

    # --------------------------------------------------------
    # Orphans
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM patient_room_bed_history h
        LEFT JOIN patients p
            ON h.Patient_ID = p.Patient_ID
        WHERE p.Patient_ID IS NULL
    """)

    orphan_patients = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM patient_room_bed_history h
        LEFT JOIN admissions a
            ON h.Admission_ID = a.Admission_ID
        WHERE a.Admission_ID IS NULL
    """)

    orphan_admissions = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM patient_room_bed_history h
        LEFT JOIN departments d
            ON h.Department_ID = d.Department_ID
        WHERE d.Department_ID IS NULL
    """)

    orphan_departments = cursor.fetchone()[0]

    print()
    print("ORPHAN CHECKS")

    print(
        f"Orphan patients    : {orphan_patients:,}"
    )

    print(
        f"Orphan admissions   : {orphan_admissions:,}"
    )

    print(
        f"Orphan departments  : {orphan_departments:,}"
    )

    # --------------------------------------------------------
    # Date validation
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM patient_room_bed_history
        WHERE Allocated_To < Allocated_From
    """)

    invalid_dates = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM patient_room_bed_history
        WHERE Length_Of_Stay_Hours < 0
    """)

    invalid_hours = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM patient_room_bed_history
        WHERE Daily_Bed_Charge < 0
           OR Total_Bed_Cost < 0
    """)

    invalid_costs = cursor.fetchone()[0]

    print()
    print("VALUE VALIDATION")

    print(
        f"Invalid dates       : {invalid_dates:,}"
    )

    print(
        f"Invalid stay hours  : {invalid_hours:,}"
    )

    print(
        f"Invalid costs       : {invalid_costs:,}"
    )

    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            Allocation_Status,
            COUNT(*)
        FROM patient_room_bed_history
        GROUP BY Allocation_Status
        ORDER BY Allocation_Status
    """)

    print()
    print("ALLOCATION STATUS")

    for status, count in cursor.fetchall():

        print(
            f"{status:<15}: {count:,}"
        )

    # --------------------------------------------------------
    # Care unit
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            Care_Unit_Type,
            COUNT(*)
        FROM patient_room_bed_history
        GROUP BY Care_Unit_Type
        ORDER BY Care_Unit_Type
    """)

    print()
    print("CARE UNIT TYPE")

    for care_unit, count in cursor.fetchall():

        print(
            f"{care_unit:<25}: {count:,}"
        )

    # --------------------------------------------------------
    # Data source
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            Data_Source,
            COUNT(*)
        FROM patient_room_bed_history
        GROUP BY Data_Source
    """)

    print()
    print("DATA SOURCE")

    for source, count in cursor.fetchall():

        print(
            f"{source:<20}: {count:,}"
        )

    # --------------------------------------------------------
    # Overflow
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM patient_room_bed_history
        WHERE Bed_Number LIKE 'OVERFLOW-%'
    """)

    overflow_count = cursor.fetchone()[0]

    print()
    print("BED CAPACITY")

    print(
        f"Overflow allocations : "
        f"{overflow_count:,}"
    )

    # --------------------------------------------------------
    # Final status
    # --------------------------------------------------------

    passed = (
        total == expected
        and unique_admissions == expected
        and nulls[0] == 0
        and nulls[1] == 0
        and nulls[2] == 0
        and nulls[3] == 0
        and nulls[4] == 0
        and nulls[5] == 0
        and nulls[6] == 0
        and nulls[7] == 0
        and orphan_patients == 0
        and orphan_admissions == 0
        and orphan_departments == 0
        and invalid_dates == 0
        and invalid_hours == 0
        and invalid_costs == 0
    )

    print()
    print("=" * 70)

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
    print("STEP 57 - PATIENT ROOM/BED HISTORY")
    print("=" * 70)
    print()

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        print(
            "Connected to MySQL successfully."
        )

        print()

        # ----------------------------------------------------
        # Existing records
        # ----------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_room_bed_history
        """)

        existing = cursor.fetchone()[0]

        print(
            f"Existing history records: "
            f"{existing:,}"
        )

        if existing > 0:

            print(
                "Deleting existing Step 57 records..."
            )

            cursor.execute("""
                DELETE FROM patient_room_bed_history
            """)

            connection.commit()

            print("Existing records deleted.")

        print()

        # ----------------------------------------------------
        # Load beds
        # ----------------------------------------------------

        print("Loading physical beds...")

        beds_by_room = load_beds(cursor)

        total_beds = sum(
            len(v)
            for v in beds_by_room.values()
        )

        print(
            f"Physical beds loaded: "
            f"{total_beds:,}"
        )

        print()

        # ----------------------------------------------------
        # Load admissions
        # ----------------------------------------------------

        print(
            "Loading admissions with matching rooms..."
        )

        admissions = load_admissions(cursor)

        print(
            f"Admissions loaded: "
            f"{len(admissions):,}"
        )

        if not admissions:

            raise RuntimeError(
                "No admissions found."
            )

        # ----------------------------------------------------
        # Allocate beds
        # ----------------------------------------------------

        print()

        print("=" * 70)
        print("GENERATING HISTORICAL BED ALLOCATIONS")
        print("=" * 70)

        print()

        allocations = allocate_beds(
            admissions,
            beds_by_room
        )

        print()

        print(
            f"Allocations generated: "
            f"{len(allocations):,}"
        )

        # ----------------------------------------------------
        # Insert
        # ----------------------------------------------------

        print()

        print("=" * 70)
        print("INSERTING HISTORY")
        print("=" * 70)

        print()

        inserted = insert_history(
            cursor,
            allocations
        )

        connection.commit()

        print()

        print(
            f"Inserted records: "
            f"{inserted:,}"
        )

        # ----------------------------------------------------
        # Validate
        # ----------------------------------------------------

        validate(
            cursor,
            len(allocations)
        )

    except Exception as error:

        if connection:

            connection.rollback()

        print()

        print("=" * 70)
        print("ERROR")
        print("=" * 70)

        print(
            str(error)
        )

        print()

        print(
            "Transaction rolled back."
        )

        sys.exit(1)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

        print()
        print(
            "Database connection closed."
        )


if __name__ == "__main__":
    main()