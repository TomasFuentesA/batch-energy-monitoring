CREATE TABLE IF NOT EXISTS energy_data_cleaned (
    timestamp TIMESTAMP NOT NULL,
    house_id VARCHAR(50) NOT NULL,
    consumption_kWh FLOAT,
    temperature FLOAT,
    voltage FLOAT,
    PRIMARY KEY (timestamp, house_id)
);

CREATE TABLE IF NOT EXISTS energy_data_raw (
    timestamp TIMESTAMP NOT NULL,
    house_id VARCHAR(50) NOT NULL,
    consumption_kWh FLOAT,
    temperature FLOAT,
    voltage FLOAT,
    PRIMARY KEY (timestamp, house_id)
);