CREATE TABLE IF NOT EXISTS countries(
	country_id TINYINT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS  group_technology(
	group_technology_id TINYINT   PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    renewable BOOLEAN NOT NULL
    );
CREATE TABLE IF NOT EXISTS  technology(
	technology_id TINYINT PRIMARY KEY   NOT NULL,
    name VARCHAR(50) NOT NULL,
    group_technology_id TINYINT NOT NULL,
    FOREIGN KEY (group_technology_id) REFERENCES group_technology(group_technology_id)
    );
CREATE TABLE IF NOT EXISTS  sub_technology(
	sub_technology_id TINYINT PRIMARY KEY  ,
    name VARCHAR(50) NOT NULL,
    technology_id TINYINT NOT NULL,
    FOREIGN KEY (technology_id) REFERENCES technology(technology_id)
    );
CREATE TABLE IF NOT EXISTS producer_type(
    producer_type_id TINYINT PRIMARY KEY,
    type TEXT NOT NULL CHECK(type IN ('Off-grid electricity', 'On-grid electricity', 'All types'))
);
CREATE TABLE IF NOT EXISTS  energy_data (
    id SMALLINT NOT NULL PRIMARY KEY,
	country_id TINYINT NOT NULL,
    sub_tech_id TINYINT NOT NULL,
    producer_type_id TINYINT NOT NULL,
    year INTEGER NOT NULL,
    electricity_generation_gwh FLOAT,
    electricity_installed_mw FLOAT,
    public_flows_2022_usdm FLOAT,
    international_public_flows_7a1 FLOAT,
    renewable_installed_per_capita_whab FLOAT,
    FOREIGN KEY (country_id) REFERENCES countries(country_id),
    FOREIGN KEY (sub_tech_id) REFERENCES sub_technology(sub_technology_id),
    FOREIGN KEY (producer_type_id) REFERENCES producer_type(producer_type_id)
);

    
