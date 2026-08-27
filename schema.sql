-- 1. Create a dedicated database for our logistics project
CREATE DATABASE IF NOT EXISTS logistics_analytics;

-- 2. Tell MySQL to use this database
USE logistics_analytics;

-- 3. Create a clean table to store our delivery records
DROP TABLE IF EXISTS logistics_delivery_logs;
CREATE TABLE logistics_delivery_logs (
    transaction_id VARCHAR(50) PRIMARY KEY,
    carrier_name VARCHAR(100),
    origin_city VARCHAR(100),
    destination_city VARCHAR(100),
    planned_transit_hours DECIMAL(6,2),
    actual_transit_hours DECIMAL(6,2),
    risk_classification VARCHAR(50),
    operational_status VARCHAR(50)
);

-- 4. Create an index so our analytics queries run faster later
CREATE INDEX idx_risk_tier ON logistics_delivery_logs(risk_classification);
