import os
from datasets import load_dataset


def save_images(dataset, save_dir):
    os.makedirs(save_dir, exist_ok=True)

    for idx, example in enumerate(dataset['train']):
        image = example['image']
        text = example['text']
        image_url = example['image_url']

        image_path = os.path.join(save_dir, f"image_{idx}.jpg")
        image.save(image_path)
        print(f"Saved {image_path}")


def main():
    dataset = load_dataset("bunyaminergen/Food102")

    save_dir = "saved_images"
    save_images(dataset, save_dir)

    for example in dataset['train']:
        image = example['image']
        text = example['text']
        image_url = example['image_url']

        print(f"Text: {text}, Image URL: {image_url}")


if __name__ == "__main__":
    main()
