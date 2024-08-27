#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from reader import InterestRateReader
from plotter import Plotter

key = "a1f1b291064b43dab2a0aa18a07ea0d4"

if __name__ == "__main__":
    r = InterestRateReader(key=key)
    json_data = r.retrieve_prime_rate_data()

    p = Plotter()
    #p.plot_prime_interest_rate(json_data)
    p.plot_both(json_data)

    sys.exit(0)

