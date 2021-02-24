#!/bin/python3
import os
from typing import List

import requests
import json

working_dir: str = "working"
files_dir: str = os.path.join(working_dir, "data")
data_dir: str = os.path.join(working_dir, "json")

congress_api_base: str = "https://www.govinfo.gov/bulkdata/json/"


def download_response(url: str) -> dict:
    headers: dict = {
        "Accept": "application/json"
    }

    response: requests.Response = requests.get(url=url, headers=headers)
    response_dict: dict = json.loads(response.text)

    return response_dict


def download_file(url: str) -> bytes:
    headers: dict = {
        "Accept": "*"
    }

    response: requests.Response = requests.get(url=url, headers=headers)
    response_bytes: bytes = response.content

    return response_bytes


def write_json(data: dict, filename: str):
    data_str: str = json.dumps(data)
    with open(file=filename, mode="w+") as f:
        f.writelines(data_str)
        f.close()


def write_file(body: bytes, filename: str):
    with open(file=filename, mode="w+b") as f:
        f.write(body)
        f.close()


if __name__ == "__main__":
    if not os.path.exists(working_dir):
        os.mkdir(working_dir)

    if not os.path.exists(files_dir):
        os.mkdir(files_dir)

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    data = download_response(url=congress_api_base)
    urls: List[str] = [congress_api_base]

    for url in urls:
        if url == congress_api_base:
            write_json(data=data, filename=os.path.join(data_dir, "index.json"))
        else:
            folder_path: str = os.path.join(data_dir, url[len(congress_api_base):])
            json_path: str = f"{folder_path}/index.json"

            if os.path.exists(json_path):
                data = json.load(open(json_path, mode="r"))
            else:
                data = download_response(url=url)

            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

            write_json(data=data, filename=json_path)

        for file in data["files"]:
            filename: str = os.path.join(files_dir, url[len(congress_api_base):], file['justFileName'])

            if file['folder']:
                if not os.path.exists(filename):
                    print(f"Making Directory: {filename} - URL: {url}")
                    os.mkdir(filename)
                else:
                    print(f"Already Made Directory: {filename}")

                if file['link'] not in urls:
                    urls.append(file['link'])

                # print(f"Folder: {filename} - {file['link']}")
            else:
                # print(f"File: {filename} - {file['link']}")

                if not os.path.exists(filename):
                    print(f'Downloading File "{filename}" From "{file["link"]}"')
                    contents: bytes = download_file(url=file['link'])
                    write_file(body=contents, filename=filename)
                else:
                    print(f'Skipping File "{filename}" Due To Already Existing')

        # Note: NEVER Modify List Will Looping Through It!!!
        # urls.remove(url)
