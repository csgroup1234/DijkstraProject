import os, psycopg2, pandas
import numpy as np
from PIL import Image, ImageDraw

WD = os.path.dirname(os.path.realpath(__file__))

CSV_DIR = WD + '/../Provided Content/'
IMG_FLD = '/init_plots/'
TXT_FLD = '/init_bus_stops/'
BND_FLD = '/init_bounds/'


IMG_DIM = (500, 500)
CIR_RAD = 5
FILL = (255, 0, 0)
FILL_B = (0, 0, 0)



CSV_LIST = [
    'Adherence',
    # 'BusFareBoxActivity',
    # 'BusOnTimePerformance',
    # 'MasterBusStopList',
    # 'Logged_Messages_6.00amTo9.00AM_10052017'
]

SQLBASE = '''

	SELECT * FROM adherence_tbl;

'''

SQLBRKT = '''
	
	SELECT tbl_pk, b.vehicle_number, b.odometer, b.service_date, b.scheduled_time FROM
	(SELECT a.*, 
			lag(vehicle_number, -1) over () AS lg
			FROM adherence_tbl a
			WHERE a.arrival_time NOTNULL
			ORDER BY a.tbl_pk DESC) AS b
	WHERE b.vehicle_number <> coalesce(b.lg, -1)
	ORDER BY tbl_pk;

'''

SQLSECT = '''

	SELECT * 
	FROM adherence_tbl
	WHERE tbl_pk BETWEEN {} AND {}

'''

db_conn = psycopg2.connect("host='localhost' user='postgres' password='...'")

def new_img(size=IMG_DIM, color=(255, 255, 255)):
	img = Image.new('RGB', size=size, color=color)
	return img

def get_corr(lon, lat, pg_conv):
	x_corr = (lon - pg_conv[0]) / pg_conv[2] * IMG_DIM[0]
	y_corr = (lat - pg_conv[3]) / pg_conv[5] * IMG_DIM[1]
	return x_corr, y_corr, CIR_RAD

def calc_scale(axis_min, axis_max):
	return 4 / 3 * np.abs(axis_max - axis_min)

def stretched_screen(axis_min, axis_max, axis_scale):
	iMin = np.max(((axis_min + axis_max - axis_scale) / 2), 0)
	iMax = iMin + axis_scale
	return iMin, iMax

def save_unique_stops(vn, l):
	with open(WD + TXT_FLD + vn + '_STOPS.txt', 'w') as sf:
		for i, stop in enumerate(l):
			sf.write(str(i) + ',' + stop + '\n')

def save_bounds(pt_conv):
	with open(WD + BND_FLD + vn + '_BOUNDS.txt', 'w') as ib:
		ib.write('{},{},{},{}'.format(pt_conv[0], pt_conv[1], pt_conv[3], pt_conv[4]))


for file in CSV_LIST:
	df_breaks = pandas.read_sql(SQLBRKT, db_conn)
	for x in range(len(df_breaks['tbl_pk']) - 1):

		# So we can see progress
		vn = df_breaks['vehicle_number'][x].astype(str)
		print(vn, end=' ')
		print('{0:.2f}%'.format(x / (len(df_breaks['tbl_pk']) - 1) * 100), end='\r')

		vn_img = new_img()
		draw_img = ImageDraw.Draw(vn_img)

		a, b = df_breaks['tbl_pk'][x], df_breaks['tbl_pk'][x + 1] - 1
		df_veh = pandas.read_sql(SQLSECT.format(a, b), db_conn)

		# This should be done in postgres
		pow_one = np.ceil(np.log10(np.abs(df_veh['long']))) - 2
		pow_two = np.ceil(np.log10(np.abs(df_veh['long']))) - 2
		df_veh['corr_long'] = df_veh['long'] / (10 ** (pow_one))
		df_veh['corr_lat'] = df_veh['lat'] / (10 ** (pow_two))

		max_lat, min_lat = np.max(df_veh['corr_lat']), np.min(df_veh['corr_lat'])
		max_long, min_long = np.max(df_veh['corr_long']), np.min(df_veh['corr_long'])

		pg_x_scale = calc_scale(min_long, max_long)
		pg_y_scale = calc_scale(min_lat, max_lat)

		iMinLong, iMaxLong = stretched_screen(min_long, max_long, pg_x_scale)
		iMinLat, iMaxLat = stretched_screen(min_lat, max_lat, pg_y_scale)

		pt_conv = (iMinLong, iMaxLong, pg_x_scale, iMinLat, iMaxLat, pg_y_scale)

		for ind, row in df_veh.iterrows():
			i, j, r = get_corr(row['corr_long'], row['corr_lat'], pt_conv)
			draw_img.ellipse((i - r, j - r, i + r, j + r), fill=FILL)
			if (0 < ind and (0 <= i <= IMG_DIM[0] and 0 <= j <= IMG_DIM[1]) and
				(0 <= prev_i <= IMG_DIM[0] and 0 <= prev_j <= IMG_DIM[1])):
				draw_img.line((prev_i, prev_j, i, j), fill=FILL_B)
			# Debugging
			if (IMG_DIM[0] < i or IMG_DIM[1] < j):
				print(vn)
			prev_i, prev_j = i, j

		vn_img.save(WD + IMG_FLD + vn + '.jpg')
		save_unique_stops(vn, df_veh['stop_number'].unique())
		save_bounds(pt_conv)
