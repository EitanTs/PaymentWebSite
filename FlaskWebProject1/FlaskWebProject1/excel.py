# -*- coding: utf-8 -*-

import conf

from xlrd import open_workbook
from xlutils.copy import copy

EXCEL_PATH = conf.EXCEL_PATH
FIRST_ROW = 0
NAME_COL = 1

FIRST_SHEET_INDEX = 0

COLUMNS_DICTIONARY = { "Name": 1, "Date": 2, "Payment Type": 3, 
                       "Amount Payed": 4, "Hours": 5, "Debt": 6,
                       "Receipt": 7 }


def read_excel_data(Name=None):
    wb = open_workbook(EXCEL_PATH)
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols

        rows = []
        values = {}

        for row in range(1, number_of_rows):
            name = sheet.cell(row, NAME_COL).value
            if Name:
                if Name.lower() == name.lower():
                    values[name] = []
                else:
                    if Name.lower() in name.lower():
                        values[name] = []
                    else:
                        continue
            else:
                values[name] = []

            for col in range(NAME_COL + 1, number_of_columns):
                values[name].append(str(sheet.cell(row, col).value))                         
        return values

def update_excel_by_name(student_name, col_name, value):
    
    rb = open_workbook(EXCEL_PATH)
    wb = copy(rb)
    s = wb.get_sheet(FIRST_SHEET_INDEX)
    main_sheet = rb.sheets()[FIRST_SHEET_INDEX]

    for row in range(0, main_sheet.nrows):
        
        is_change = student_name == main_sheet.cell(row, COLUMNS_DICTIONARY["Name"]).value    

        for col in range(0, main_sheet.ncols):
            
            cell_value = main_sheet.cell(row, col).value
            if is_change and col == COLUMNS_DICTIONARY[col_name]:
                s.write(row, col, value)
            else:
                s.write(row, col, cell_value)
    wb.save(EXCEL_PATH)

def delete_excel_line_by_name(student_name):
    rb = open_workbook(EXCEL_PATH)
    wb = copy(rb)
    s = wb.get_sheet(FIRST_SHEET_INDEX)
    main_sheet = rb.sheets()[FIRST_SHEET_INDEX]

    for row in range(0, main_sheet.nrows):
        
        is_delete = student_name == main_sheet.cell(row, COLUMNS_DICTIONARY["Name"]).value    

        for col in range(0, main_sheet.ncols):
            cell_value = main_sheet.cell(row, col).value
            if is_delete:
                s.write(row, col, '')
            else:
                s.write(row, col, cell_value)
    wb.save(EXCEL_PATH)