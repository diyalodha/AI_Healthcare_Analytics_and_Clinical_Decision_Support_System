/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 48_Create_Medicine_Stock_Table.sql

Purpose : Create Medicine Stock Management Table

Description:
Tracks medicine batches, expiry dates, stock levels,
supplier information and inventory management.

Version : 2.3

Author  : Diya Lodha & Team
===========================================================
*/

USE healthcare_ai_db;

-- ==========================================================
-- Remove Existing Table
-- ==========================================================

DROP TABLE IF EXISTS Medicine_Stock;

-- ==========================================================
-- Create Table
-- ==========================================================

CREATE TABLE Medicine_Stock (

    -- ======================================================
    -- Primary Key
    -- ======================================================

    Medicine_Stock_ID CHAR(36)
        NOT NULL PRIMARY KEY
        DEFAULT (UUID()),

    -- ======================================================
    -- Foreign Key
    -- ======================================================

    Medication_ID CHAR(36)
        NOT NULL,

    -- ======================================================
    -- Batch Information
    -- ======================================================

    Batch_Number VARCHAR(100)
        NOT NULL,

    Manufacturing_Date DATE,

    Expiry_Date DATE
        NOT NULL,

    -- ======================================================
    -- Stock Information
    -- ======================================================

    Quantity_Available INT
        DEFAULT 0,

    Minimum_Stock_Level INT
        DEFAULT 10,

    Maximum_Stock_Level INT
        DEFAULT 1000,

    Reorder_Level INT
        DEFAULT 20,

    Purchase_Price DECIMAL(10,2),

    Selling_Price DECIMAL(10,2),

    -- ======================================================
    -- Supplier Information
    -- ======================================================

    Supplier_Name VARCHAR(150),

    Supplier_Contact VARCHAR(100),

    Storage_Location VARCHAR(150),

    Storage_Temperature VARCHAR(50),

    -- ======================================================
    -- Stock Status
    -- ======================================================

    Stock_Status ENUM(
        'Available',
        'Low Stock',
        'Expired',
        'Unavailable',
        'Reserved'
    )
    DEFAULT 'Available',

    Reorder_Status ENUM(
        'Not Required',
        'Pending',
        'Ordered',
        'Received'
    )
    DEFAULT 'Not Required',

    Last_Restock_Date DATE,

    Last_Stock_Update DATETIME
        DEFAULT CURRENT_TIMESTAMP,

    Last_Dispensed_Date DATE,

    Notes TEXT,

    -- ======================================================
    -- Dataset Tracking
    -- ======================================================

    Data_Source ENUM(
        'Hospital_Records',
        'Synthetic'
    )
    DEFAULT 'Hospital_Records',

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
    -- Foreign Key
    -- ======================================================

    CONSTRAINT FK_MedicineStock_Medication
        FOREIGN KEY (Medication_ID)
        REFERENCES Medications(Medication_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    -- ======================================================
    -- Unique Constraint
    -- ======================================================

    CONSTRAINT UK_MedicineStock_Medication_Batch
        UNIQUE (Medication_ID, Batch_Number)

);

-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX IDX_MedicineStock_Medication
ON Medicine_Stock(Medication_ID);

CREATE INDEX IDX_MedicineStock_Batch
ON Medicine_Stock(Batch_Number);

CREATE INDEX IDX_MedicineStock_Expiry
ON Medicine_Stock(Expiry_Date);

CREATE INDEX IDX_MedicineStock_Status
ON Medicine_Stock(Stock_Status);

CREATE INDEX IDX_MedicineStock_Reorder
ON Medicine_Stock(Reorder_Status);

CREATE INDEX IDX_MedicineStock_Quantity
ON Medicine_Stock(Quantity_Available);

CREATE INDEX IDX_MedicineStock_LastRestock
ON Medicine_Stock(Last_Restock_Date);

SHOW TABLES;

DESCRIBE Medicine_Stock;