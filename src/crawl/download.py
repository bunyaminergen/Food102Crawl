import os
import requests
import yaml
import json
import csv
import time
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()


class Download:
    def __init__(self, config_path, count, check=False, sources='all'):
        self.config = self.load_config(config_path)
        self.unsplash_client_id = os.getenv('UNSPLASH_API_KEY')
        self.pexels_client_id = os.getenv('PEXELS_API_KEY')
        self.pixabay_client_id = os.getenv('PIXABAY_API_KEY')
        self.flickr_client_id = os.getenv('FLICKR_API_KEY')
        self.metadata_list = []
        self.count = count
        self.queries = self.config['queries']
        self.check = check
        self.sources = self.parse_sources(sources)

    @staticmethod
    def load_config(config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
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

    @staticmethod
    def create_folder(folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Folder created: {folder}")
        else:
            print(f"Folder already exists: {folder}")

    def parse_sources(self, sources):
        if sources == 'all':
            return ['unsplash', 'pexels', 'pixabay', 'openverse', 'flickr']
        elif isinstance(sources, str):
            return [sources]
        elif isinstance(sources, list):
            return sources
        else:
            raise ValueError("Invalid sources type. Must be 'all', a string, or a list.")

    def unsplash_download(self, folder, query, per_source_count):
        base_url = self.config['unsplash']['base_url']
        page = 1
        downloaded = 0

        while downloaded < per_source_count:
            url = f"{base_url}?query={query}&client_id={self.unsplash_client_id}&per_page=30&page={page}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                for idx, image in enumerate(data['results']):
                    if downloaded >= per_source_count:
                        break
                    img_url = image['urls']['regular']
                    image_name = f'{query}_{len(self.metadata_list) + 1}.jpg'
                    description = image.get('description') or image.get('alt_description') or ''

                    if self.check and query.lower() not in (description or '').lower():
                        print(f"Skipping {image_name} as it does not contain the query term.")
                        continue

                    self.download_image(img_url, folder, image_name)
                    metadata = {
                        "image": os.path.join(folder, image_name),
                        "text": description,
                        "image_url": img_url
                    }
                    self.metadata_list.append(metadata)
                    downloaded += 1

                page += 1
                time.sleep(7)
            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 403:
                    print("Unsplash Rate Limit Exceeded. Waiting for 1 hour and 3 minutes...")
                    for _ in tqdm(range(3780), desc="Waiting"):
                        time.sleep(1)
                    continue
                else:
                    print(f"HTTP error occurred on Unsplash: {http_err}")
                    break
            except Exception as err:
                print(f"Other error occurred on Unsplash: {err}")
                break

    def pexels_download(self, folder, query, per_source_count):
        base_url = self.config['pexels']['base_url']
        headers = {
            'Authorization': self.pexels_client_id
        }
        page = 1
        downloaded = 0

        while downloaded < per_source_count:
            url = f"{base_url}?query={query}&per_page=30&page={page}"
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                for idx, image in enumerate(data['photos']):
                    if downloaded >= per_source_count:
                        break
                    img_url = image['src']['original']
                    image_name = f'{query}_{len(self.metadata_list) + 1}.jpg'
                    description = image.get('alt') or ''

                    if self.check and query.lower() not in (description or '').lower():
                        print(f"Skipping {image_name} as it does not contain the query term.")
                        continue

                    self.download_image(img_url, folder, image_name)
                    metadata = {
                        "image": os.path.join(folder, image_name),
                        "text": description,
                        "image_url": img_url
                    }
                    self.metadata_list.append(metadata)
                    downloaded += 1

                page += 1
                time.sleep(7)
            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 429:
                    print("Pexels Rate Limit Exceeded. Waiting for 5 minutes...")
                    for _ in tqdm(range(300), desc="Waiting"):
                        time.sleep(1)
                    continue
                else:
                    print(f"HTTP error occurred on Pexels: {http_err}")
                    break
            except Exception as err:
                print(f"Other error occurred on Pexels: {err}")
                break

    def pixabay_download(self, folder, query, per_source_count):
        base_url = self.config['pixabay']['base_url']
        page = 1
        downloaded = 0

        while downloaded < per_source_count:
            url = f"{base_url}?key={self.pixabay_client_id}&q={query}&image_type=photo&per_page=30&page={page}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                for idx, image in enumerate(data['hits']):
                    if downloaded >= per_source_count:
                        break
                    img_url = image['largeImageURL']
                    image_name = f'{query}_{len(self.metadata_list) + 1}.jpg'
                    description = image.get('tags') or ''

                    if self.check and query.lower() not in (description or '').lower():
                        print(f"Skipping {image_name} as it does not contain the query term.")
                        continue

                    self.download_image(img_url, folder, image_name)
                    metadata = {
                        "image": os.path.join(folder, image_name),
                        "text": description,
                        "image_url": img_url
                    }
                    self.metadata_list.append(metadata)
                    downloaded += 1

                page += 1
                time.sleep(7)
            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 429:
                    print("Pixabay Rate Limit Exceeded. Waiting for 5 minutes...")
                    for _ in tqdm(range(300), desc="Waiting"):
                        time.sleep(1)
                    continue
                else:
                    print(f"HTTP error occurred on Pixabay: {http_err}")
                    break
            except Exception as err:
                print(f"Other error occurred on Pixabay: {err}")
                break

    def openverse_download(self, folder, query, per_source_count):
        base_url = self.config['openverse']['base_url']
        page = 1
        downloaded = 0

        while downloaded < per_source_count:
            url = f"{base_url}?q={query}&format=json&per_page=30&page={page}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                for idx, image in enumerate(data['results']):
                    if downloaded >= per_source_count:
                        break
                    img_url = image['url']
                    image_name = f'{query}_{len(self.metadata_list) + 1}.jpg'
                    description = image.get('title') or ''

                    if self.check and query.lower() not in (description or '').lower():
                        print(f"Skipping {image_name} as it does not contain the query term.")
                        continue

                    self.download_image(img_url, folder, image_name)
                    metadata = {
                        "image": os.path.join(folder, image_name),
                        "text": description,
                        "image_url": img_url
                    }
                    self.metadata_list.append(metadata)
                    downloaded += 1

                page += 1
                time.sleep(7)
            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 429:
                    print("Openverse Rate Limit Exceeded. Waiting for 5 minutes...")
                    for _ in tqdm(range(300), desc="Waiting"):
                        time.sleep(1)
                    continue
                else:
                    print(f"HTTP error occurred on Openverse: {http_err}")
                    break
            except Exception as err:
                print(f"Other error occurred on Openverse: {err}")
                break

    def flickr_download(self, folder, query, per_source_count):
        base_url = self.config['flickr']['base_url']
        page = 1
        downloaded = 0

        while downloaded < per_source_count:
            url = f"{base_url}?method=flickr.photos.search&api_key={self.flickr_client_id}&text={query}&format=json&nojsoncallback=1&per_page=30&page={page}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                for idx, photo in enumerate(data['photos']['photo']):
                    if downloaded >= per_source_count:
                        break
                    img_url = f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}_b.jpg"
                    image_name = f'{query}_{len(self.metadata_list) + 1}.jpg'
                    description = photo.get('title') or ''

                    if self.check and query.lower() not in (description or '').lower():
                        print(f"Skipping {image_name} as it does not contain the query term.")
                        continue

                    self.download_image(img_url, folder, image_name)
                    metadata = {
                        "image": os.path.join(folder, image_name),
                        "text": description,
                        "image_url": img_url
                    }
                    self.metadata_list.append(metadata)
                    downloaded += 1

                page += 1
                time.sleep(7)
            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 429:
                    print("Flickr Rate Limit Exceeded. Waiting for 5 minutes...")
                    for _ in tqdm(range(300), desc="Waiting"):
                        time.sleep(1)
                    continue
                else:
                    print(f"HTTP error occurred on Flickr: {http_err}")
                    break
            except Exception as err:
                print(f"Other error occurred on Flickr: {err}")
                break

    def save_metadata(self):
        metadata_path = self.config['metadata_path']
        with open(os.path.join(metadata_path, 'metadata.json'), 'w', encoding='utf-8') as json_file:
            json.dump(self.metadata_list, json_file, indent=4)

        with open(os.path.join(metadata_path, 'metadata.csv'), 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['image', 'text', 'image_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for data in self.metadata_list:
                writer.writerow(data)

    def run(self):
        image_base_path = self.config['image_base_path']

        for query in self.queries:
            folder = os.path.join(image_base_path, query)
            self.create_folder(folder)
            per_source_count = self.count // len(self.sources)

            for source in self.sources:
                downloaded = 0
                while downloaded < per_source_count:
                    initial_count = len(self.metadata_list)
                    try:
                        if source == 'unsplash':
                            self.unsplash_download(folder, query, per_source_count - downloaded)
                        elif source == 'pexels':
                            self.pexels_download(folder, query, per_source_count - downloaded)
                        elif source == 'pixabay':
                            self.pixabay_download(folder, query, per_source_count - downloaded)
                        elif source == 'openverse':
                            self.openverse_download(folder, query, per_source_count - downloaded)
                        elif source == 'flickr':
                            self.flickr_download(folder, query, per_source_count - downloaded)
                    except Exception as e:
                        print(f"Error occurred for source {source} with query {query}: {e}")
                    downloaded += len(self.metadata_list) - initial_count

        self.save_metadata()


def main():
    config_path = 'config/data.yaml'
    count = 30
    check = True
    sources = 'all'

    downloader = Download(config_path, count, check, sources)
    downloader.run()


if __name__ == "__main__":
    main()
