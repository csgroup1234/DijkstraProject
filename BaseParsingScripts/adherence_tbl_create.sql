CREATE TABLE ADHERENCE_TBL (
    tbl_pk SERIAL PRIMARY KEY,
    service_date VARCHAR(9),
    routes INT,
    block VARCHAR(7),
    route_direction_name VARCHAR(12),
    stop_number VARCHAR(5),
    location VARCHAR(47),
    lat INT,
    long INT,
    scheduled_time INT,
    scheduled_time_str VARCHAR(8),
    arrival_time INT,
    arrival_time_str VARCHAR(8),
    depart_time INT,
    depart_time_str VARCHAR(8),
    odometer FLOAT,
    vehicle_number INT
);