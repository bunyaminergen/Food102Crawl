from src.crawl.download import Download


def main():
    config_path = 'config/data.yaml'
    count = 4
    check = True
    sources = 'all'  # or 'unsplash', 'pexels', or a list like ['unsplash', 'pexels']

    downloader = Download(config_path, count, check, sources)
    downloader.run()


if __name__ == "__main__":
    main()
