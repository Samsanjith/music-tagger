import os
import requests
from requests.auth import HTTPBasicAuth
import csv
import json

api_key = input("Enter API Key")
audio_directory = input("Enter directory with your music files")

upload_url = "https://api-us.musiio.com/api/v1/upload/file"
extract_url = "https://api-us.musiio.com/api/v1/extract/tags"

useful_tags = ["USE CASE", "GENRE", "GENRE V2", "GENRE V3", "MOOD", "MOOD V2", "MOOD V3", "ENERGY", "AUTOTUNE PRESENCE"]

# Function to upload audio file and return track ID
def upload_audio_file(audio_file):
    opened_audio_file = [('audio', open(audio_file, 'rb'))]
    response = requests.post(upload_url, auth = HTTPBasicAuth(api_key, ''), files = opened_audio_file)
    return response.json()['id']

# Function to extract tags using track ID
def extract_tags(track_id):
    payload = {"id": track_id, "tags": useful_tags}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(extract_url, auth = HTTPBasicAuth(api_key, ''), headers = headers, data = json.dumps(payload))
    return response.json()

csv_file_name = "music_tag_info.csv"
csv_file_columns = ["FILE NAME"] + useful_tags

with open(csv_file_name, 'w', newline = '') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames = csv_file_columns)
    csv_writer.writeheader()

    for audio_file_name in os.listdir(audio_directory):    
        audio_file_path = os.path.join(audio_directory, audio_file_name)

        track_id = upload_audio_file(audio_file_path)
        
        tags = extract_tags(track_id)

        # Update CSV file
        row_data = {"File Name": audio_file_name}
        row_data.update(tags)
        csv_writer.writerow(row_data)