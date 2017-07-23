select tbl_pk, b.vehicle_number, b.odometer, b.service_date, b.scheduled_time from
(select a.*, 
		lag(vehicle_number, -1) over () as lg
		from adherence_tbl a
		where a.arrival_time NOTNULL
		order by a.tbl_pk desc) as b
where b.vehicle_number <> coalesce(b.lg, -1)
order by tbl_pk;