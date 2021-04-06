import requests


ENDPOINT_URL = 'https://opendata.camden.gov.uk/api/views/x43g-c2rf/rows.csv?accessType=DOWNLOAD'


def dump():
    response = requests.get(ENDPOINT_URL)
    with open("data/camden.csv", "wb") as csvfile:
        csvfile.write(response.content)


if __name__ == "__main__":
    dump()
