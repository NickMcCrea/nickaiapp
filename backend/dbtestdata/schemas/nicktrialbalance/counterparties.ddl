CREATE TABLE counterparties (
    counterparty_id VARCHAR(255) PRIMARY KEY,
    counterparty_name VARCHAR(255),
    counterparty_type VARCHAR(255),
    gics_level_1 VARCHAR(255),
    gics_level_2 VARCHAR(255),
    gics_level_3 VARCHAR(255),
    gics_level_4 VARCHAR(255),
    country_of_organisation VARCHAR(255),
    country_of_jurisdiction VARCHAR(255),
    country_of_residence VARCHAR(255)
  
);