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

@app.route('/home', methods=['POST','POST'])
def home():
    
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

@app.route('/edit/', methods=["GET"])
def edit():
    excel.update_excel_by_name(request.args.get('name'), 'Date', '01/01/1996')
    return render_template(
                    'Home.html',
                    title='Home Page',
                    payment_data = all_excel_data,
                    all_excel_data = all_excel_data
                    )


@app.route('/delete/', methods=["GET"])
def delete():
    excel.delete_excel_line_by_name(request.args.get('name'))
    return render_template(
                    'Home.html',
                    title='Home Page',
                    payment_data = all_excel_data,
                    all_excel_data = all_excel_data
                    )