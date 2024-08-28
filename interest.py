#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from reader import InterestRateReader
from plotter import Plotter

if __name__ == "__main__":

    print("Start")
    key = None
    try:
        key = os.environ['RIKSBANK_API_KEY']
    except:
        print("Unable to find API Key needed for Riksbanken.")
        sys.exit(-1)
    
    r = InterestRateReader(key=key)
    json_data = r.retrieve_prime_rate_data()

    p = Plotter()
    p.plot_both(json_data)

    print("Bye!")

    sys.exit(0)

