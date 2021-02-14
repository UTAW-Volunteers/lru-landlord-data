"""
Hackney host a PDF of their property licenses on google drive, linked from a page on their webite.
The PDF contains tabular data that we can parse out and convert to a CSV.

Note: requires a Java runtime
"""

from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests
import tabula

START_URL = "https://hackney.gov.uk/hmo"
DRIVE_DOWNLOAD_URL = "https://drive.google.com/uc?export=download&id={}"

# Some magic numbers to help Tabula find the columns, without which it can't
# cope with all the whitespace.
COLUMNS = [
    79,
    164,
    220,
    294.525,
    325.215,
    340.065,
    354.915,
    369,
    402,
    423.225,
    451.935,
    478.665,
    504.405,
    534.105,
    553.905,
    574,
    610,
    632.115,
    652.905,
    675.675,
    695.475,
    714.285,
]

def dump():
    # Get the latest google drive link from hackney.gov.uk in case it changes when they update
    response = requests.get(START_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find(class_="typepdf")["href"]
    path = urlparse(link).path
    drive_token = path.split("/")[3]
    drive_url = DRIVE_DOWNLOAD_URL.format(drive_token)

    tabula.convert_into(drive_url, "hackney.csv", output_format="csv", pages="all", guess=False, stream=True, columns=COLUMNS)


if __name__ == "__main__":
    dump()
