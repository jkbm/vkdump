#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Module to fetch images(or other types of attachments)
from VK dialog and download them to local drive.
"""
from time import time
from sys import stdout

import urllib.request
import requests
import json


def get_photos(folder, **kwargs):
    """
    Fetching API request results
    """
    base = "https://api.vk.com/method/messages.getHistoryAttachments"
    params = {}
    for key, value in kwargs.items():
        params[key] = str(value)
        print(key, value)
    jsons = []
    time_then = time()
    response = requests.get(base, params=params)
    jresponse = response.json()
    jsons.append(jresponse)
    with open('{0}.json'.format(jresponse['response']["next_from"]), 'w') as outfile:
        json.dump(jresponse, outfile)
    while "next_from" in jresponse['response']:
        start_from = jresponse['response']["next_from"]
        params['start_from'] = start_from
        response = requests.get(base, params=params)
        jresponse = response.json()
        jsons.append(jresponse)
        with open('{0}.json'.format(jresponse['response']["next_from"]), 'w') as outfile:
            json.dump(jresponse, outfile)

    print("Data created in %ds" % round(time()-time_then, 3))
    return jsons

def download(data):
    """
    Downloading, naming and saving photos locally
    """
    time_then = time()
    count = 0
    for part in data:
        for item in part['response']:
            if part['response'] != [0] and item != "next_from" and item != '0':
                link = data[0]['response'][str(item)]['photo']["src_big"]
                count += 1
                urllib.request.urlretrieve(link, '{0}/{1}.jpg'.format(folder, count))
                stdout.write("\r%d done" % int(count))
                stdout.flush()
    stdout.write("\r  \r\n")
    print("Files downloaded in %ds" % round(time()-time_then, 3))

if __name__ == "__main__":    
    access_token = "<GENERATED APP ACCESS TOKEN HERE>"
    peer_id = input("Enter dialog id: ") #Enter dialog id from prompt
    # peer_id = "<DIALOG ID HERE>" or directly in code
    folder = input("Enter folder name to save files into: ")
    data = get_photos(folder=folder,
                      peer_id=peer_id,
                      access_token=access_token,
                      count=200,
                      media_type="photo"
                     )
    download(data)
