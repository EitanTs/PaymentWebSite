import json
import conf
import os
import excel

KEYS = ["Name", "Date", "Payment Type", "Amount Payed", "Hours", "Debt", "Receipt"]

RECEIPT_KEY = "Receipt"

NOT_USEFUL_KEYS = [RECEIPT_KEY, "Day", "Month", "Year"]

EDITING_KEYS = ["AmountPayed", "Hours"]

def create_empty_json(json_path):
    data_list = [{"Keys" : KEYS}]
    with open(json_path, mode='wb') as json_file:
        json_file.write(json.dumps(data_list))

def is_user_exist(name):
    return len(get_json_data(Name=name)) > 1

def change_data_to_json_file(new_data, json_path, delete_flag=False):
    with open(json_path, mode='r') as json_file:
        json_data = json.loads(json_file.read())
        if delete_flag:
            json_data.remove(new_data)
        else:
            json_data.append(new_data)
        json_data = json.dumps(json_data)
    
    with open(json_path, mode='w') as json_file:
        json_file.write(json_data)

def create_empty_payment_dict():
    payment_dict = {}
    for key in KEYS:
        payment_dict[key] = ''
    return payment_dict


def get_json_data(Name=None):
    if not os.path.isfile(conf.JSON_PATH):
        create_empty_json(conf.JSON_PATH)
    f = open(conf.JSON_PATH, 'rb')
    json_data = f.read()
    f.close()
    
    if not Name:
        return json.loads(json_data)

    json_data = json.loads(json_data)
    filtered_data = [json_data[0]]
    
    for i in range(1, len(json_data)):
        if Name in json_data[i]["Name"]:
            filtered_data.append(json_data[i])

    return filtered_data

def join_parts_to_date(day, month, year):
    return "{0}-{1}-{2}".format(day, month, year)


def set_receipt(request):
    payment_dict = {}
    if RECEIPT_KEY in request.keys():
        payment_dict[RECEIPT_KEY] = "V"
    else:
        payment_dict[RECEIPT_KEY] = "X"
    
    return payment_dict

def create_payment_dict(request):
    payment_dict = set_receipt(request)
    
    for key in request.keys():
        if key not in NOT_USEFUL_KEYS:
            payment_dict[key] = request[key]

    return payment_dict


def add_payment(request):
    json_data = get_json_data()
    date = join_parts_to_date(request["Day"], request["Month"], request["Year"])
    payment_dict = create_payment_dict(request)
    payment_dict["Date"] = date
    excel.write_data_to_csv(payment_dict)
    change_data_to_json_file(payment_dict, conf.JSON_PATH)

def delete_user(name):
    json_data = get_json_data()
    for i in range(1, len(json_data)):
        if name == json_data[i]["Name"]:
            change_data_to_json_file(json_data[i], conf.JSON_PATH, delete_flag=True)

def add_value_to_exist_data(json_data, request, key):
    return str(int(json_data[key]) + int(request[key]))

def add_to_exist_data(request):
    json_data = get_json_data(Name=request["Name"])[1]
    json_data["Date"] = join_parts_to_date(request["Day"], request["Month"], request["Year"])
    json_data["Receipt"] = request["Receipt"]
    json_data["PaymentType"] = request["PaymentType"]
    json_data["Debt"] = request["Debt"]

    for key in EDITING_KEYS:
        json_data[key] = add_value_to_exist_data(json_data, request, key)
    delete_user(request["Name"])
    change_data_to_json_file(json_data, conf.JSON_PATH)
    
def convert_immmutable_dict_to_dict(request):
    dict = {}
    for key in request.keys():
        dict[key] = request[key]
    return dict

def clear_and_update_data(request):
    
    request["Date"] = join_parts_to_date(request["Day"], request["Month"], request["Year"])
    request.pop("Day")
    request.pop("Month")
    request.pop("Year")
    delete_user(request["Name"])
    change_data_to_json_file(request, conf.JSON_PATH)

def calc_debt(request):
    json_data = get_json_data(Name=request["Name"])[1]
    old_debt = float(json_data["Debt"])
    new_debt = float(request["AmountPayed"]) - conf.LESSON_COST * float(request["Hours"])
    return int(old_debt + new_debt)

def edit_user(request):
    request = convert_immmutable_dict_to_dict(request)
    if not "Receipt" in request.keys():
        request["Receipt"] = "off"
    print request
    request["Debt"] = calc_debt(request)
    if is_receipt(request["Name"]):
        clear_and_update_data(request)
    else:
        add_to_exist_data(request)
    excel.write_data_to_csv(request)

def is_receipt(name):
    json_data = get_json_data(Name=name)[1]
    return json_data["Receipt"] == "on"

def send_receipt(name):
    json_data = get_json_data(Name=name)[1]
    json_data["Receipt"] = "on"
    delete_user(name)
    change_data_to_json_file(json_data, conf.JSON_PATH)
