from src.crawl.download import Download


def main():
    config_path = 'config/data.yaml'
    count = 10
    check = True
    sources = 'all'
    downloader = Download(config_path, count, check, sources)
    downloader.run()


if __name__ == "__main__":
    main()
