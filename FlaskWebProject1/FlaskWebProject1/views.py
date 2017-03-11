"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject1 import app
from flask import request
from flask import session
import conf
import excel 
import JsonLoader

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

LIST_OF_COLS = ["Name", "Date", "Payment Type", "Amount Payed", "Hours", "Debt", "Receipt"]

all_excel_data = excel.read_excel_data()

@app.route('/')
def index():
    """Renders the home page."""
    session['UserName'] = None

    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        error_message=''
    )

@app.route('/home2', methods=['GET','POST'])
def home2():
    
    if session['UserName']:
        if request.method == 'POST':
            if 'Name' in request.form.keys():
                name = request.form['Name']
                return render_template(
                        'Home.html',
                        title='Home Page',
                        payment_data = excel.read_excel_data(Name=name),
                        all_excel_data = all_excel_data
                        )
        return render_template(
                    'Home.html',
                    title='Home Page',
                    payment_data = all_excel_data,
                    all_excel_data = all_excel_data
                    )
    if request.method == 'POST':
        if request.form['UserName'] == conf.USER_NAME  and request.form['Password'] == conf.PASSWORD:
            session['UserName'] = request.form['UserName']
            return render_template(
                'Home.html',
                title='Home Page',
                payment_data = all_excel_data,
                all_excel_data = all_excel_data
                )
    return render_template(
    'index.html',
    title='Home Page',
    year=datetime.now().year,
    error_message='Invalid User or Password'
    )

@app.route('/home', methods=['GET','POST'])
def home():
    json_data = JsonLoader.get_json_data()
    if session['UserName']:
        if request.method == 'POST':
            if 'Name' in request.form.keys():
                name = request.form['Name']
                return render_template(
                        'Home2.html',
                        payment_data = JsonLoader.get_json_data(Name=name), #change to filter by name
                        all_json_data = json_data,
                        payment_keys = json_data[0]["Keys"]
                        )
        return render_template(
                    'Home2.html',
                    payment_data = json_data,
                    all_json_data = json_data,
                    payment_keys = json_data[0]["Keys"]
                    )
    if request.method == 'POST':
        if request.form['UserName'] == conf.USER_NAME  and request.form['Password'] == conf.PASSWORD:
            session['UserName'] = request.form['UserName']
            return render_template(
                'Home2.html',
                payment_data = json_data,
                all_json_data = json_data,
                payment_keys = json_data[0]["Keys"]
                )
    return render_template(
    'index.html',
    title='Home Page',
    year=datetime.now().year,
    error_message='Invalid User or Password'
    )

@app.route('/AddPayment', methods=['GET','POST'])
def add_payment():
    date = datetime.today()
    day = date.day
    month = date.month
    year = date.year

    if request.method == 'POST':
        if JsonLoader.is_user_exist(request.form["Name"]):
            json_data = JsonLoader.get_json_data()
            return render_template('Home2.html',
                    payment_data = json_data,
                    all_json_data = json_data,
                    payment_keys = json_data[0]["Keys"],
                    error_message = True
                    )
        JsonLoader.add_payment(request.form)
        json_data = JsonLoader.get_json_data()

        return render_template('Home2.html',
                    payment_data = json_data,
                    all_json_data = json_data,
                    payment_keys = json_data[0]["Keys"]
                    )

    return render_template('AddPayment.html',
                           year=year,
                           month=month,
                           day=day
                           )

@app.route('/edit/', methods=["GET"])
def edit():
    
    json_data = JsonLoader.get_json_data()

    date = datetime.today()
    day = date.day
    month = date.month
    year = date.year

    if len(request.args.get('name')):
        return render_template(
                        "EditPayment.html", 
                        name=request.args.get('name'),
                        year=year,
                        month=month,
                        day=day

                        )
    json_data = JsonLoader.get_json_data()

    return render_template('Home2.html',
                    payment_data = json_data,
                    all_json_data = json_data,
                    payment_keys = json_data[0]["Keys"],
                    reload=True
                    )

@app.route('/edit_details', methods=["POST"])
def edit_details():
    
    if request.method == "POST":
        JsonLoader.edit_user(request.form)
        print 1
        
    
    json_data = JsonLoader.get_json_data()
    return render_template('Home2.html',
                    payment_data = json_data,
                    all_json_data = json_data,
                    payment_keys = json_data[0]["Keys"],  
                    )

@app.route('/delete/', methods=["GET"])
def delete():

    json_data = JsonLoader.get_json_data()
    if len(request.args.get('name')):
        JsonLoader.delete_user(request.args.get('name'))

    return render_template('Home2.html',
                    payment_data = json_data,
                    all_json_data = json_data,
                    payment_keys = json_data[0]["Keys"],
                    reload=True
                    )
   