CREATE TABLE IF NOT EXISTS policy_transactions (
    policy_id VARCHAR(50) PRIMARY KEY,
    annual_premium_usd DECIMAL(12, 2) NOT NULL,
    status_code VARCHAR(5) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed metadata records
INSERT INTO policy_transactions (policy_id, annual_premium_usd, status_code) VALUES 
('POL-99421', 1450.00, 'A'),
('POL-10245', 2100.50, 'A'),
('POL-44192', 890.00, 'C'),
('POL-77213', 3200.00, 'A'),
('POL-30912', 1125.75, 'C');
