import pandas, os

WD = os.path.dirname(os.path.realpath(__file__))

CSV_DIR = WD + '/../Provided Content/'

CSV_LIST = [
    'Adherence',
    'BusFareBoxActivity',
    'BusOnTimePerformance',
    'MasterBusStopList',
    # 'Logged_Messages_6.00amTo9.00AM_10052017'
]

STR_COLS = [
    'ServiceDate',
    'Block',
    'RouteDirectionName',
    'StopNumber',
    'Location',
    'ScheduledTime(HHMMSS)',
    'ArrivalTime(HHMMSS)',
    'DepartureTime(HHMMSS)',
    'RouteName',
    'RouteName',
    'Location',
    'Corner',
    'Accessibility',
    'Shelter',
    'RoutesServed',
    'Branch',
    'Direction',
    'CBD',
]

INT_COLS = [
    'StopNumber',
    'Routes',
    'Sequence',
    'Routes',
    'EarlyDeparture',
    'OnTime',
    'LateArrival',
    'Missing',
    'TimePointCount',
    'Routes',
    'Ridership',
    'TockenCount',
    'TicketCount',
    'PassCount',
    'BillCount',
    'DumpCount',
    'Routes',
    'ScheduledTime(s)',
    'ArrivalTime(s)',
    'DepartureTime(s)',
    'VehicleNumber',
]

FLT_COLS = [
    'AverageDwellTime',
    'CurrentRevenue',
    'UnclassifiedRevenue',
    'Latitude',
    'Longitude',
    'Odometer',
]

for file in CSV_LIST:
    # Usually Encoding is UTF-8, I dont know why, but UTF-8 is throwing 
    # a byte read error for MasterBusStopList, so I am using ISO-8859-1...
    df = pandas.read_csv(CSV_DIR + file + '.csv', header=0, encoding = "ISO-8859-1", quotechar='"', skipinitialspace=True)
    uniq_cols = []
    lens = []
    # For each column in the working file
    # Get the unique values and put them in a jagged array
    for col in list(df.columns.values):
        uniq_cols.append([col] + list(df[col].unique()))
        lens.append(len(uniq_cols[-1]))
    # Open a new csv, and write the unique values
    with open(WD + '/' + file + '_uniq.csv', 'w+') as f:
        # Use row major to write out the contents to the file
        for i in range(0, max(lens)):
            row_str = ''
            for j in range(0, len(uniq_cols)):
                if i < len(uniq_cols[j]):
                    row_str += str(uniq_cols[j][i]) + ','
                else:
                    row_str += ','
            f.write(row_str + '\n')

    with open(WD + '/' + file + '_DT.txt', 'w+') as g:
        for col in df.columns.values:
            if col in STR_COLS:
                g.write('{},{},{}\n'.format(col, 'STRING', df[col].astype(str).map(len).max()))
            elif col in INT_COLS:
                g.write('{},{},1\n'.format(col,'INT'))
            elif col in FLT_COLS:
                g.write('{},{},1\n'.format(col,'FLT'))
    print(file)
