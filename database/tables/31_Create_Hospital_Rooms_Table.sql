/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 31_Create_Hospital_Rooms_Table.sql

Purpose : Create Hospital Rooms Master Table

Version : 3.0

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

-- ==========================================================
-- Create Hospital Rooms Table
-- ==========================================================

CREATE TABLE IF NOT EXISTS Hospital_Rooms (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Room_ID CHAR(36)
        NOT NULL
        PRIMARY KEY
        DEFAULT (UUID()),


    -- ======================================================
    -- Foreign Key
    -- ======================================================

    Department_ID CHAR(36)
        NOT NULL,


    -- ======================================================
    -- Room Information
    -- ======================================================

    Room_Code VARCHAR(50)
        NOT NULL
        UNIQUE,

    Room_Number VARCHAR(20)
        NOT NULL
        UNIQUE,

    Room_Type ENUM(
        'General',
        'Semi-Private',
        'Private',
        'Deluxe',
        'ICU',
        'NICU',
        'PICU',
        'Operation Theater',
        'Emergency',
        'Isolation'
    )
    NOT NULL,

    Floor_Number INT,

    Capacity INT
        NOT NULL,

    Current_Occupancy INT
        DEFAULT 0,

    Daily_Charges DECIMAL(10,2)
        DEFAULT 0.00,

    Room_Status ENUM(
        'Available',
        'Occupied',
        'Reserved',
        'Cleaning',
        'Maintenance'
    )
    DEFAULT 'Available',

    Description TEXT,


    -- ======================================================
    -- Status Information
    -- ======================================================

    Is_Active BOOLEAN
        DEFAULT TRUE,

    Record_Version INT
        DEFAULT 1,


    -- ======================================================
    -- Audit Information
    -- ======================================================

    Created_By VARCHAR(50),

    Updated_By VARCHAR(50),

    Created_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    Updated_At TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,


    -- ======================================================
    -- Foreign Keys
    -- ======================================================

    CONSTRAINT fk_room_department
        FOREIGN KEY (Department_ID)
        REFERENCES Departments(Department_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,


    -- ======================================================
    -- Check Constraints
    -- ======================================================

    CONSTRAINT chk_room_capacity
        CHECK (Capacity > 0),

    CONSTRAINT chk_room_occupancy
        CHECK (
            Current_Occupancy >= 0
            AND Current_Occupancy <= Capacity
        ),

    CONSTRAINT chk_room_charges
        CHECK (Daily_Charges >= 0)

);

-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX idx_room_department
ON Hospital_Rooms(Department_ID);

CREATE INDEX idx_room_type
ON Hospital_Rooms(Room_Type);

CREATE INDEX idx_room_status
ON Hospital_Rooms(Room_Status);

CREATE INDEX idx_room_floor
ON Hospital_Rooms(Floor_Number);

CREATE INDEX idx_room_active
ON Hospital_Rooms(Is_Active);

-- ==========================================================
-- Verification
-- ==========================================================

SHOW TABLES;

DESCRIBE Hospital_Rooms;