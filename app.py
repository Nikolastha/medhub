"""
backend simple server for the pharmacy app med-hub
"""

import os
from flask import redirect
from flask import url_for
from flask import flash
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_cors import CORS
from bcrypt import hashpw
from bcrypt import gensalt
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_api import status

load_dotenv()
app = Flask(__name__)
CORS(app)
app.config['MONGO_DBNAME'] = 'mongo'
client = MongoClient(os.getenv('MC'))
mydb = client["pharmacy"]
diesease = mydb["diesease"]
specalist = mydb["specalist"]
medicine = mydb["medicine"]
users = mydb["users"]
app.secret_key = "blah"


@app.route('/', methods=['GET'])
def index():
    """ Index page

    :return: index page
    :rtype: flask rendertemplate
    """
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    """ Simple post request to register a new user using json"""
    return_json = {}
    if request.method == 'POST':
        post_data = request.json
        return_json["post_data"] = post_data

        pass1 = post_data["password_1"].encode('utf-8')
        # pass2 = post_data["password_2"].encode('utf-8')
        license_agreement = post_data["license_agreement"]
        _id = post_data["phone"]
        existing_user = users.find_one({'_id': _id})

        first = post_data["first_name"]
        last = post_data["last_name"]
        gender = post_data["gender"]
        dob = post_data['dob']

        if existing_user is None:
            if len(pass1) >= 6:
                # if pass1 == pass2:
                if license_agreement:
                    hashpass = hashpw(pass1, gensalt())
                    users.insert({
                        '_id': _id,
                        'password': hashpass,
                        'first': first,
                        'last': last,
                        'gender': gender,
                        'dob': dob
                    })
                    return jsonify({"result": 'User added!'})
                return jsonify({"result": 'Error 5: Please agree the license agreement'}), status.HTTP_400_BAD_REQUEST
                # return jsonify({"result": 'Error 4: passwords do not match'}), status.HTTP_400_BAD_REQUEST
            return jsonify({"result": 'Error 3: Set stronger password with atleast 6 characters'}), status.HTTP_400_BAD_REQUEST
        return jsonify({"result": 'Error 2: That _id already exists!'})
    return jsonify({"result": "Error 1: post registration details"}), status.HTTP_400_BAD_REQUEST


@app.route('/login', methods=['POST'])
def login():
    """ simple post request to login using json """

    return_json = {}
    if request.method == 'POST':
        post_data = request.json
        return_json = {"post_data": post_data}
        phone = post_data["phone"]
        password = post_data["password"]
        login_user = users.find_one({'_id': phone})
        if login_user and password != "":
            user_pass = login_user['password']
            if hashpw(password.encode('utf-8'), user_pass) == user_pass:
                return_json["success"] = True
                return_json["message"] = "Authentication success!"
                return jsonify({"result": return_json})
            else:
                return_json["success"] = False
                return_json["errors"] = "Error! Invalid Credintials! "
        else:
            return_json["success"] = False
            return_json["errors"] = "Error! Invalid Credintials! "
    else:
        return_json["success"] = False
        return_json["errors"] = "Error! use post requests and send json! "
    return jsonify({"result": return_json}), status.HTTP_400_BAD_REQUEST


@app.route('/specalists', methods=['GET'])
def get_all_specalist():
    """ get all specalists """
    return jsonify({"result": list(specalist.find())})


@app.route('/dieseases', methods=['GET'])
def get_all_diesease():
    """ get all dieseases """
    return jsonify({"result": list(diesease.find())})


@app.route('/meds', methods=['GET'])
def get_all_medicine():
    """ get all medicines """
    return jsonify({"result": list(medicine.find())})


@app.route('/vendor_login', methods=['POST'])
def vendor_login():
    """ get all medicines """
    if request.method == 'POST':
        if request.form['username'] == 'admin':
            if request.form['password'] == 'admin':
                return redirect(url_for('dashboard'))

    flash('Login error! please check you credintials.')
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/med', methods=['GET', 'POST'])
def get_one_med():
    "get a single medicine"
    common_name = request.args.get('common_name')
    search_medicine = medicine.find_one({'common_name': common_name})
    if search_medicine:
        output = search_medicine
    else:
        output = "No such name Err1" + str(common_name)
        flash(output)
    render_template('dashboard.html')


@app.route('/addspecalist')
def addspecalist():
    """ add a new specalist using a webform """
    return render_template('specalist.html')


@app.route('/adddiesease')
def adddiesease():
    """ add a new specalist using a webform """
    return render_template('diesease.html')


@app.route('/addmedicine')
def addmedicine():
    """ add a new medicine using a webform """
    return render_template('medicine.html')


@app.route('/adddiesease_post', methods=['POST', 'GET'])
def adddiesease_post():
    """ post requst which will add the posted json to diesease collection"""
    if request.method == 'POST':
        diesease_dict = {
            '_id': request.form['id'],
            'name': request.form['name'],
            'doctor': request.form['doctor'],
            'summary': request.form['summary'],
            'causes': request.form['causes'],
            'symptoms': request.form['symptoms']
        }
        diesease.insert_one(diesease_dict)
        output = "Diesease added!"
        flash(output)
        return render_template('dashboard.html')

    else:
        output = "Some error"
        flash(output)
        return render_template('dashboard.html')


@app.route('/addspecalist_post', methods=['POST', 'GET'])
def addspecalist_post():
    """ post requst which will add the posted json to specalist collection"""
    if request.method == 'POST':
        specalist_dict = {
            '_id': request.form['id'],
            'name': request.form['name'],
            'specalization': request.form['specalization'],
            'phone': request.form['phone'],
            'designation': request.form['designation']
        }
        specalist.insert_one(specalist_dict)
        output = "Specalist added!"
        flash(output)
        return render_template('dashboard.html')

    else:
        output = "Some error"
        flash(output)
        return render_template('dashboard.html')


@app.route('/addmedicine_post', methods=['POST', 'GET'])
def addmedicine_post():
    """ post requst which will add the posted json to medicine collection"""
    if request.method == 'POST':
        medicine_dict = {
            'technical_name': request.form['technical_name'],
            'common_name': request.form['common_name'],
            'price': request.form['price'],
            'schedule': request.form['schedule'],
            'description': request.form['description'],
            'prescription': request.form['prescription'],
            'company': request.form['company'],
            '_id': request.form['id'],
            'image_url': request.form['image_url']
        }
        medicine.insert_one(medicine_dict)
        output = "Medicine added!"
        flash(output)
        return render_template('dashboard.html')

    else:
        output = "Some error"
        flash(output)
        return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=bool(os.getenv('DEBUG')))
