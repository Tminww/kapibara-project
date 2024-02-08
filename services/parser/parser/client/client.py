from parser.api.api import api


def main():
    print(api.publication.subjects()["response"].json())


if __name__ == "__main__":
    main()
