CREATE TABLE counterparties (
    counterparty_id VARCHAR(255) PRIMARY KEY,
    counterparty_name VARCHAR(255),
    counterparty_type VARCHAR(255),
    gics_level_1 VARCHAR(255),
    gics_level_2 VARCHAR(255),
    gics_level_3 VARCHAR(255),
    gics_level_4 VARCHAR(255),
    country_of_residence VARCHAR(255)
  
);

CREATE TABLE nicktrialbalance (
    pnl_date DATE,
    company_code VARCHAR(255),
    account VARCHAR(255),
    cost_code VARCHAR(255),
    product_id VARCHAR(255),
    counterparty_id VARCHAR(255),
    balance REAL
);

CREATE TABLE products (
    product_id VARCHAR(255) PRIMARY KEY,
    product_type VARCHAR(255),
    instrument_type VARCHAR(255),
    market_type VARCHAR(255),
    contract_type VARCHAR(255),
    risk_type VARCHAR(255),
    maturity_date DATE,
    start_date DATE
   
);