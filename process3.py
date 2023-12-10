import json
import os
import pandas as pd

def extract_toll_info(json_folder, output_dir):
    output_file_path = os.path.join(output_dir, 'transformed_data.csv')

    df = pd.DataFrame(columns=['unit', 'trip_id', 'toll_loc_id_start', 'toll_loc_id_end',
        'toll_loc_name_start', 'toll_loc_name_end', 'toll_system_type',
        'entry_time', 'exit_time', 'tag_cost', 'cash_cost', 'license_plate_cost'])

    data_list = []

    for json_file in os.listdir(json_folder):
        unit = json_file.split('_')[0]
        trip_id = json_file.split('.')[0]
        file_path = os.path.join(json_folder, json_file)

        with open(file_path, 'r') as file:
            data = json.load(file)

            try:
                for i in data["route"]["tolls"]:
                    toll_loc_start = i["start"]["id"]
                    toll_loc_end = i["end"]["id"]
                    toll_system_type = i.get("type")
                    entry_time = i["start"]["arrival"]["time"]
                    exit_time = i["end"]["arrival"]["time"]
                    tag_cost = i.get("tagPriCost")
                    cash_cost = i.get("cashCost")
                    license_plate_cost = i.get("licensePlateCost")

                    data_list.append({'unit': unit, 'trip_id': trip_id,
                                      'toll_loc_id_start': toll_loc_start, 'toll_loc_id_end': toll_loc_end,
                                      'toll_loc_name_start': i["start"]["name"], 'toll_loc_name_end': i["end"]["name"],
                                      'toll_system_type': toll_system_type, 'entry_time': entry_time,
                                      'exit_time': exit_time, 'tag_cost': tag_cost,
                                      'cash_cost': cash_cost, 'license_plate_cost': license_plate_cost})

            except KeyError as e:
                print(f"KeyError: {e} not present in dictionary")

    df = pd.DataFrame(data_list)
    df.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    json_folder = "/home/lnv85/Documents/assignmentmapui/MapUp-Data-Assessment-E/evaluation_data/output/process2"
    output_dir = "/home/lnv85/Documents/assignmentmapui/MapUp-Data-Assessment-E/evaluation_data/output/process3"
    extract_toll_info(json_folder, output_dir)
