import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TOLLGURU_API_KEY")
API_URL = os.getenv("TOLLGURU_API_URL")

def upload_to_tollguru(csv_folder, output_dir):
    headers = {'x-api-key': API_KEY, 'Content-Type': 'text/csv'}

    for csv_file in os.listdir(csv_folder):
        file_path = os.path.join(csv_folder, csv_file)
        url = f'{API_URL}/gps-tracks-csv-upload?mapProvider=osrm&vehicleType=5AxlesTruck'

        with open(file_path, 'rb') as file:
            response = requests.post(url, data=file, headers=headers)

        json_output_file = os.path.join(output_dir, f'{csv_file.replace(".csv", ".json")}')
        
        with open(json_output_file, 'w') as json_file:
            


if __name__ == "__main__":
    csv_folder = "/home/lnv85/Documents/assignmentmapui/MapUp-Data-Assessment-E/evaluation_data/output/process1"
    output_dir = "/home/lnv85/Documents/assignmentmapui/MapUp-Data-Assessment-E/evaluation_data/output/process2"
    upload_to_tollguru(csv_folder,output_dir)
