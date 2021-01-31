# """
# Hackney's register is public but can only be searched by postcode:
# https://propertylicensing.hackney.gov.uk/public-register
# """

# from bs4 import BeautifulSoup
# import requests

# BASE_URL = "https://propertylicensing.hackney.gov.uk/public-register"


# def dump_search(postcode):
#     response = requests.get(BASE_URL)
#     soup = BeautifulSoup(response.text, "html.parser")
#     query_params = {}
#     search_field = soup.find(id="search_query")["name"]
#     query_params[search_field] = postcode
#     csrf_input = soup.find(id="search__token")
#     query_params[csrf_input["name"]] = csrf_input["value"]

#     response = requests.get(BASE_URL, params=query_params)
#     soup = BeautifulSoup(response.text, "html.parser")
#     print(response.text)



# def dump_all():
#     postcodes = (f"E{i}" for i in range(1, 16))
#     data = []
#     for postcode in postcodes:
#         data += dump_search(postcode)

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


def dump():
    # Get the latest google drive link from hackney.gov.uk in case it changes when they update
    response = requests.get(START_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find(class_="typepdf")["href"]
    path = urlparse(link).path
    drive_token = path.split("/")[3]
    drive_url = DRIVE_DOWNLOAD_URL.format(drive_token)

    dataframe = tabula.convert_into(drive_url, "hackney.csv", output_format="csv", pages="all")




if __name__ == "__main__":
    dump()
