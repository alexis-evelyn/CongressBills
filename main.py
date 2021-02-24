#!/bin/python3
import os

import requests
import json

working_dir: str = "working"
files_dir: str = os.path.join(working_dir, "bills")
data_dir: str = os.path.join(working_dir, "json")

congress_api_base: str = "https://www.govinfo.gov/bulkdata/json/BILLS"


def download_response(url: str) -> dict:
    headers: dict = {
        "Accept": "application/json"
    }

    response: requests.Response = requests.get(url=url, headers=headers)
    response_dict: dict = json.loads(response.text)

    return response_dict


def write_json(data: dict, filename: str):
    data_str: str = json.dumps(data)
    with open(file=filename, mode="w+") as f:
        f.writelines(data_str)
        f.close()


if __name__ == "__main__":
    if not os.path.exists(working_dir):
        os.mkdir(working_dir)

    if not os.path.exists(files_dir):
        os.mkdir(files_dir)

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    data = download_response(url=congress_api_base)
    write_json(data=data, filename=os.path.join(data_dir, "root.json"))

    # TODO: Figure Out How To Spider All URLs
    for file in data["files"]:
        if file['folder']:
            # TODO: Get Current Directory From API URL
            # https://www.govinfo.gov/bulkdata/json/BILLS/117/1/sconres/BILLS-117sconres1es.xml -> /117/1/sconres/BILLS-117sconres1es.xml
            bill_dir: str = os.path.join(files_dir, file['justFileName'])
            if not os.path.exists(bill_dir):
                os.mkdir(bill_dir)

            print(f"Folder: {file['justFileName']} - {file['link']}")
        else:
            print(f"File: {file['justFileName']} - {file['link']}")