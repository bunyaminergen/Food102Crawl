import os
import requests
import yaml
import json
import csv
from dotenv import load_dotenv

load_dotenv()


def download_image(url, folder, image_name):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(os.path.join(folder, image_name), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {image_name}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Folder created: {folder}")
    else:
        print(f"Folder already exists: {folder}")


def unsplash_download(folder, query, base_url, client_id, count, metadata_list):
    url = f"{base_url}?query={query}&client_id={client_id}&per_page={count}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for idx, image in enumerate(data['results']):
            img_url = image['urls']['regular']
            image_name = f'{query}_{idx + 1}.jpg'
            download_image(img_url, folder, image_name)
            metadata = {
                "image": os.path.join(folder, image_name),
                "text": f"photo of {query}",
                "image_url": img_url
            }
            metadata_list.append(metadata)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def main():
    with open('config/data.yaml', 'r') as file:
        config = yaml.safe_load(file)

    base_url = config['unsplash']['base_url']
    count = config['unsplash']['count']
    client_id = os.getenv('UNSPLASH_API_KEY')
    image_base_path = config['unsplash']['image_base_path']
    metadata_path = config['unsplash']['metadata_path']

    queries = config['queries']

    metadata_list = []

    for query in queries:
        folder = os.path.join(image_base_path, query)
        create_folder(folder)
        unsplash_download(folder, query, base_url, client_id, count, metadata_list)

    with open(os.path.join(metadata_path, 'metadata.json'), 'w') as json_file:
        json.dump(metadata_list, json_file, indent=4)

    with open(os.path.join(metadata_path, 'metadata.csv'), 'w', newline='') as csvfile:
        fieldnames = ['image', 'text', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in metadata_list:
            writer.writerow(data)


if __name__ == "__main__":
    main()
