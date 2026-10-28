/*
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : 01_Create_Database.sql
Purpose : Create Database
Version : 3.0
Author  : Diya Lodha & Team
===========================================================
*/

-- ===========================================================
-- Drop Existing Database
-- ===========================================================

DROP DATABASE IF EXISTS healthcare_ai_db;

-- ===========================================================
-- Create Database
-- ===========================================================

CREATE DATABASE healthcare_ai_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE healthcare_ai_db;

-- ===========================================================
-- Verify Database
-- ===========================================================

SELECT DATABASE();