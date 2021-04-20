BEGIN TRANSACTION;

CREATE TABLE providers (
    id              integer PRIMARY KEY,
    code            char(3),
    logo_url        varchar,
    name            varchar,
    summary         varchar,    
    is_active       boolean
);

CREATE TABLE verticals (
    id              integer PRIMARY KEY,
    code            char(2),
    name            varchar
);

CREATE TABLE products (
    id              integer PRIMARY KEY,
    vertical_id     integer,
    provider_id     integer,
    is_sponsored    boolean,
    data            json,
    CONSTRAINT fk_vertical FOREIGN KEY(vertical_id) REFERENCES verticals(id),
    CONSTRAINT fk_provider FOREIGN KEY(provider_id) REFERENCES providers(id)
);


CREATE VIEW active_broadband_products AS
SELECT 
    pd.id,
    pd.is_sponsored,
    vt.code as vertical_code,
    pv.name as provider_name,
    pv.logo_url as provider_logo_url,
    (pd.data->>'p')::int as p,
    (pd.data->>'internet_download_speed_in_mbs')::int as internet_download_speed_in_mbs,
    (pd.data->>'tv_channels')::int as tv_channels,
    (pd.data->>'mobile_phone_count')::int as mobile_phone_count,
    (pd.data->>'mobile_phone_data_in_gbps')::int as mobile_phone_data_in_gbps,
    (pd.data->>'price')::FLOAT as price
FROM products pd
JOIN providers pv on pv.id=pd.provider_id
JOIN verticals vt on vt.id=pd.vertical_id
WHERE vt.code='BB' AND pv.is_active;


COPY providers(id,code,logo_url,name,summary,is_active)
FROM '/docker-entrypoint-initdb.d/providers.csv'
DELIMITER ','
CSV HEADER;

COPY verticals(id,code,name)
FROM '/docker-entrypoint-initdb.d/verticals.csv'
DELIMITER ','
CSV HEADER;

COPY products(id,vertical_id,provider_id,is_sponsored,data)
FROM '/docker-entrypoint-initdb.d/products.csv'
DELIMITER ','
CSV HEADER;

COMMIT;
