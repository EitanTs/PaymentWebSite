import json
import conf
import os

KEYS = ["Name", "Date", "Payment Type", "Amount Payed", "Hours", "Debt", "Receipt"]

RECEIPT_KEY = "Receipt"

NOT_USEFUL_KEYS = [RECEIPT_KEY, "Day", "Month", "Year"]

def create_empty_json(json_path):
    data_list = [{"Keys" : KEYS}]
    with open(json_path, mode='wb') as json_file:
        json_file.write(json.dumps(data_list))



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
    change_data_to_json_file(payment_dict, conf.JSON_PATH)

def delete_user(name):
    json_data = get_json_data()
    for i in range(1, len(json_data)):
        if name == json_data[i]["Name"]:
            change_data_to_json_file(json_data[i], conf.JSON_PATH, delete_flag=True)