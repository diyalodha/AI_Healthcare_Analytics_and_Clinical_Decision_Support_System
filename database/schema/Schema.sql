/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : Schema.sql

Purpose :
Database Schema Configuration

Includes:
- Database Initialization
- Foreign Key Management
- Character Set Configuration
- SQL Mode Configuration
- Relationship Validation
- Database Metadata

Version : 2.1

Author : Diya Lodha & Team
===========================================================
*/


-- ==========================================================
-- Select Database
-- ==========================================================

USE healthcare_ai_db;



-- ==========================================================
-- Database Configuration
-- ==========================================================

SET SQL_MODE = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION';


SET NAMES utf8mb4;



-- ==========================================================
-- Disable Foreign Key Checks
-- Used during bulk loading / seed insertion
-- ==========================================================

SET FOREIGN_KEY_CHECKS = 0;



-- ==========================================================
-- Storage Engine Configuration
-- ==========================================================

ALTER DATABASE healthcare_ai_db

CHARACTER SET utf8mb4

COLLATE utf8mb4_unicode_ci;



-- ==========================================================
-- Enable Foreign Key Checks
-- ==========================================================

SET FOREIGN_KEY_CHECKS = 1;



-- ==========================================================
-- Database Verification Queries
-- ==========================================================


-- Check all created tables

SHOW TABLES;



-- Check Database Information

SELECT

    SCHEMA_NAME AS Database_Name,

    DEFAULT_CHARACTER_SET_NAME AS Character_Set,

    DEFAULT_COLLATION_NAME AS Collation

FROM information_schema.SCHEMATA

WHERE SCHEMA_NAME = 'healthcare_ai_db';



-- ==========================================================
-- Table Count Verification
-- ==========================================================

SELECT

COUNT(*) AS Total_Tables

FROM information_schema.TABLES

WHERE TABLE_SCHEMA = 'healthcare_ai_db';



-- ==========================================================
-- Foreign Key Relationship Verification
-- ==========================================================


SELECT

TABLE_NAME,

COLUMN_NAME,

CONSTRAINT_NAME,

REFERENCED_TABLE_NAME,

REFERENCED_COLUMN_NAME

FROM information_schema.KEY_COLUMN_USAGE

WHERE TABLE_SCHEMA = 'healthcare_ai_db'

AND REFERENCED_TABLE_NAME IS NOT NULL;



-- ==========================================================
-- End of Schema Configuration
-- ==========================================================