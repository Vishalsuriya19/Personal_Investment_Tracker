-- Investment Tracker Database Schema
-- Drop existing tables if they exist
DROP TABLE IF EXISTS reports;
DROP TABLE IF EXISTS predictions;
DROP TABLE IF EXISTS investments;
DROP TABLE IF EXISTS users;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Investments table
CREATE TABLE investments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    stock_name VARCHAR(100) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    quantity DECIMAL(10, 4) NOT NULL DEFAULT 1,
    purchase_price DECIMAL(15, 2) NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_date (date)
);

-- Predictions table
CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    stock_name VARCHAR(100) NOT NULL,
    current_price DECIMAL(15, 2) NOT NULL,
    predicted_price DECIMAL(15, 2) NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    profit_probability DECIMAL(5, 2) NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_stock_name (stock_name)
);

-- Reports table
CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    report_text LONGTEXT NOT NULL,
    risk_assessment VARCHAR(50) NOT NULL,
    recommendations LONGTEXT,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_date (date)
);

-- Create indexes for better query performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_investments_stock ON investments(stock_name);
CREATE INDEX idx_predictions_stock ON predictions(stock_name);
