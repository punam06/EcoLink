-- Initialize MySQL database for EcoLink
-- This script is executed during container startup

-- Ensure the database exists
CREATE DATABASE IF NOT EXISTS ecolink;

-- Grant permissions to the ecolink_user
GRANT ALL PRIVILEGES ON ecolink.* TO 'ecolink_user'@'%';
FLUSH PRIVILEGES;