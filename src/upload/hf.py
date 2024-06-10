import os
import pandas as pd
from datasets import Dataset, Features, Value, Image
from huggingface_hub import login
from dotenv import load_dotenv

load_dotenv()

hf_api_key = os.getenv('HUGGING_FACE_API_KEY')

login(token=hf_api_key)


def load_metadata(metadata_path):
    return pd.read_csv(metadata_path)


def create_hf_dataset(df, images_base_path):
    features = Features({
        'image': Image(),
        'text': Value('string'),
        'image_url': Value('string')
    })

    def correct_image_path(image_path):
        if image_path.startswith('.data/images'):
            return os.path.join(images_base_path, image_path[len('.data/images/'):])
        return os.path.join(images_base_path, image_path)

    df['image'] = df['image'].apply(correct_image_path)

    dataset = Dataset.from_pandas(df, features=features)
    return dataset


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    print(base_dir)
    metadata_path = os.path.join(base_dir, ".data", "metadata.csv")
    images_base_path = os.path.join(base_dir, ".data", "images")

    df = load_metadata(metadata_path)

    dataset = create_hf_dataset(df, images_base_path)

    dataset.push_to_hub("bunyaminergen/Food102")


if __name__ == "__main__":
    main()
