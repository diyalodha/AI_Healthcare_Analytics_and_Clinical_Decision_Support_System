/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 47_Create_Inventory_Table.sql

Purpose : Create Hospital Inventory Management Table

Description:
Stores medical supplies, equipment inventory,
stock availability, supplier details, expiry tracking,
and AI-enabled inventory management information.

Version : 2.2

Author  : Diya Lodha & Team
===========================================================
*/


USE healthcare_ai_db;



-- ==========================================================
-- Remove Existing Table
-- ==========================================================

DROP TABLE IF EXISTS Inventory;



-- ==========================================================
-- Table : Inventory
-- ==========================================================

CREATE TABLE Inventory (


    -- ======================================================
    -- Primary Key
    -- ======================================================

    Inventory_ID CHAR(36)
        NOT NULL PRIMARY KEY DEFAULT (UUID()),



    -- ======================================================
    -- Department Reference
    -- ======================================================

    Department_ID CHAR(36),



    -- ======================================================
    -- Inventory Information
    -- ======================================================

    Item_Name VARCHAR(200)
        NOT NULL,


    Item_Code VARCHAR(100)
        NOT NULL UNIQUE,


    Item_Category ENUM(

        'Medical Equipment',

        'Surgical Supplies',

        'Consumables',

        'Laboratory',

        'Pharmacy',

        'PPE',

        'General'

    )
    NOT NULL,


    Manufacturer VARCHAR(150),


    Batch_Number VARCHAR(100),



    -- ======================================================
    -- Stock Details
    -- ======================================================

    Quantity_Available INT
        DEFAULT 0,


    Minimum_Required_Quantity INT
        DEFAULT 0,


    Reorder_Level INT
        DEFAULT 10,


    Maximum_Stock_Level INT
        DEFAULT 1000,


    Unit_Type VARCHAR(50),



    -- ======================================================
    -- Supplier & Storage
    -- ======================================================

    Supplier_Name VARCHAR(150),


    Supplier_Contact VARCHAR(100),


    Storage_Location VARCHAR(150),


    Purchase_Date DATE,


    Expiry_Date DATE,


    Last_Used_Date DATE,


    Cost_Per_Unit DECIMAL(10,2),



    -- ======================================================
    -- Inventory Status
    -- ======================================================

    Inventory_Status ENUM(

        'Available',

        'Low Stock',

        'Out of Stock',

        'Expired',

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


    Last_Stock_Update DATETIME
        DEFAULT CURRENT_TIMESTAMP,


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
    -- Constraints
    -- ======================================================

    CONSTRAINT CHK_Inventory_Quantity
        CHECK (Quantity_Available >= 0),


    CONSTRAINT CHK_Minimum_Quantity
        CHECK (Minimum_Required_Quantity >= 0),


    CONSTRAINT CHK_Reorder_Level
        CHECK (Reorder_Level >= 0),


    CONSTRAINT CHK_Maximum_Stock
        CHECK (Maximum_Stock_Level >= Reorder_Level),



    -- ======================================================
    -- Foreign Key
    -- ======================================================

    CONSTRAINT FK_Inventory_Department

        FOREIGN KEY (Department_ID)

        REFERENCES Departments(Department_ID)

        ON UPDATE CASCADE

        ON DELETE SET NULL

);



-- ==========================================================
-- Indexes
-- ==========================================================

CREATE INDEX IDX_Inventory_Department
ON Inventory(Department_ID);


CREATE INDEX IDX_Inventory_Item_Name
ON Inventory(Item_Name);


CREATE INDEX IDX_Inventory_Item_Code
ON Inventory(Item_Code);


CREATE INDEX IDX_Inventory_Category
ON Inventory(Item_Category);


CREATE INDEX IDX_Inventory_Status
ON Inventory(Inventory_Status);


CREATE INDEX IDX_Inventory_Reorder
ON Inventory(Reorder_Status);


CREATE INDEX IDX_Inventory_Expiry
ON Inventory(Expiry_Date);


CREATE INDEX IDX_Inventory_Stock
ON Inventory(Quantity_Available);



SHOW TABLES;

DESCRIBE Inventory;