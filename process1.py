# unit: Unique identification of the vehicle.
# latitude: GPS latitude in degrees.
# longitude: GPS longitude in degrees.
# timestamp: Timestamp string in RFC 3301 format.

import os
import pandas as pd
from datetime import datetime

def extract_tripsCSV(input_file, output_dir):
    data = pd.read_parquet(input_file)
    # print(data["timestamp"])
    # print(data)
    print(data["unit"].unique())
    # dt_object = datetime.strptime(data["timestamp"], '%Y-%m-%d %H:%M:%S%z')
    # output_timestamp = dt_object.strftime('%Y-%m-%dT%H:%M:%SZ%z')
    # print(output_timestamp)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    df = data.groupby('unit')
    print(df.first())
    for unit, unit_df in df:
        unit_df = unit_df.sort_values(by='timestamp')
        unit_df['time_diff'] = unit_df['timestamp'].diff().dt.total_seconds().fillna(0)
        unit_df['trip_number'] = (unit_df['time_diff'] > 7 * 3600).cumsum()

        for trip_number, trip_df in unit_df.groupby('trip_number'):
            trip_df['timestamp'] = pd.to_datetime(trip_df['timestamp'], utc=True)
            trip_df['timestamp'] = trip_df['timestamp'].apply(lambda x: x.strftime('%Y-%m-%dT%H:%M:%S'))
            trip_df[['latitude', 'longitude', 'timestamp']].to_csv(
                os.path.join(output_dir, f'{unit}_{trip_number}.csv'),
                index=False
            )

if __name__ == "__main__":
    input_file = "/home/lnv85/Documents/assignmentmapui/MapUp-Data-Assessment-E/evaluation_data/input/raw_data.parquet"
    output_dir = "/home/lnv85/Documents/assignmentmapui/MapUp-Data-Assessment-E/evaluation_data/output/process1/"
    extract_tripsCSV(input_file, output_dir)

