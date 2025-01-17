

import pandas as pd
import logging

def load_data(data):
    try:
        df = pd.read_json(data)

    except FileNotFoundError as e:
        logging.basicConfig

    return df