#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
import io
import os

class InterestRateReader:

    CONST_MAX_AGE_OF_DATA_FILE_IN_MINUTES = 60
    TEMP_FILENAME = "temp.json"

    def __init__(self, key):
        self.key = key

    def _save_to_file(self, content):
        f = open(self.TEMP_FILENAME, "w", encoding="utf-8")
        f.write(content)
        f.close()

    def _read_from_file(self):
        text = None
        with io.open(self.TEMP_FILENAME, "r", encoding="utf8") as f:
            text = f.read()
        return text

    def _get_interest_rates(self):
        #url = "https://api.riksbank.se/swestr/v1/SWESTR?fromDate={}".format(
        #    "2024-01-01T15:00:00Z"
        #)

        #url = "https://api.riksbank.se/swestr/v1/index/{}?fromDate={}".format(
        #    "SWESTRINDEX",
        #    "2024-01-01T15:00:00Z"
        #)

        #url = "https://api.riksbank.se/swestr/v1/{}?fromDate={}".format(
        #    "SWESTR",
        #    "2024-01-01T15:00:00Z"
        #)

        #url = "https://api.riksbank.se/monetary_policy_data/v1/forecasts"

        #url = "https://api.riksbank.se/monetary_policy_data/v1/forecasts/policy_rounds"

        #url = "https://api.riksbank.se/swea/v1/Series"

        url = "https://api.riksbank.se/swea/v1/Observations/{}/{}".format(
            "SECBREPOEFF",
            "1994-06-01"
        )

        the_headers = {"Authorization" : "Bearer {self.key}"}
        response = requests.get(
            url=url, 
            headers=the_headers)
        
        if response.status_code == 200:
            print ('OK!')
            response_dict = response.json()
            self._save_to_file(json.dumps(response_dict, indent=4, sort_keys=True))
        else:
            print ('Fail!')

    def _get_plot_data(self):
        data = self._read_from_file()
        print(data)

    def retrieve_prime_rate_data(self):
        data = None
        read_from_remote = True

        if os.path.exists(self.TEMP_FILENAME):
            fileLastUpdatedTime = os.stat(self.TEMP_FILENAME).st_mtime
            ageOfFileInMinutes = (time.time() - fileLastUpdatedTime) / 240
            if ageOfFileInMinutes < self.CONST_MAX_AGE_OF_DATA_FILE_IN_MINUTES:
                read_from_remote = False

        if read_from_remote:
            self._get_interest_rates()

        data = self._read_from_file()

        return data
        