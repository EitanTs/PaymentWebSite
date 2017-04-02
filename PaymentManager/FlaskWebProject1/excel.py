# -*- coding: utf-8 -*-

import conf
import csv
import os
EXCEL_PATH = conf.EXCEL_PATH

def write_data_to_csv(payment_dict):
    keys = payment_dict.keys()
    values = payment_dict.values()
    
    keys.remove('submit')
    values.remove('')
    
    if not os.path.isfile(conf.CSV_PATH):
        with open(conf.CSV_PATH, 'wb') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(keys)

    with open(conf.CSV_PATH, 'ab') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(values)