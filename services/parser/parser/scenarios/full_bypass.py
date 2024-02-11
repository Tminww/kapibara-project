from services.parser.parser.outgoing_requests.request import api


def main():
    print(api.publication.subblocks()["response"].json())


if __name__ == "__main__":
    main()
