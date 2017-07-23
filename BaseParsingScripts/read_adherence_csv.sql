COPY adherence_tbl (
	service_date, 
	routes,
	block,
	route_direction_name,
	stop_number,
	location,
	lat,
	long,
	scheduled_time,
	scheduled_time_str,
	arrival_time,
	arrival_time_str,
	depart_time,
	depart_time_str, 
	odometer,
	vehicle_number
) FROM '/Users/cory/Desktop/Adherence.csv' HEADER NULL 'NULL' DELIMITER ',' CSV;