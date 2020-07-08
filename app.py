from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_cors import CORS
import bcrypt

from pymongo import MongoClient


client = MongoClient(
    "mongodb://root:root@localhost:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false")

app = Flask(__name__)
CORS(app)
app.config['MONGO_DBNAME'] = 'mongo'


mydb = client["pharmacy"]
medicine = mydb["medicine"]
users = mydb["users"]


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    return_json = {}
    if request.method == 'POST':
        post_data = request.json
        return_json["post_data"] = post_data

        pass1 = post_data["password_1"].encode('utf-8')
        pass2 = post_data["password_2"].encode('utf-8')
        license_agreement = post_data["license_agreement"]
        _id = post_data["phone"]
        existing_user = users.find_one({'_id': _id})

        first = post_data["first_name"]
        last = post_data["last_name"]
        gender = post_data["gender"]
        dob = post_data['dob']

        if existing_user is None:
            if len(pass1) >= 6:
                if pass1 == pass2:
                    if license_agreement:
                        hashpass = bcrypt.hashpw(pass1, bcrypt.gensalt())
                        users.insert({
                            '_id': _id,
                            'password': hashpass,
                            'first': first,
                            'last': last,
                            'gender': gender,
                            'dob': dob
                        })
                        return jsonify({"result": 'User added!'})
                    return jsonify({"result": 'Error 5: Please agree the license agreement'})
                return jsonify({"result": 'Error 4: passwords do not match'})
            return jsonify({"result": 'Error 3: Set stronger password with atleast 6 characters'})
        return jsonify({"result": 'Error 2: That _id already exists!'})
    return jsonify({"result": "Error 1: post registration details"})


@app.route('/login', methods=['POST'])
def login():
    return_json = {}
    if request.method == 'POST':
        post_data = request.json
        return_json = {"post_data": post_data}
        phone = post_data["phone"]
        password = post_data["password"]
        login_user = users.find_one({'_id': phone})
        if login_user and password != "":
            x = password.encode('utf-8')
            y = login_user['password']
            z = login_user['password']
            if bcrypt.hashpw(x, y) == z:
                return_json["success"] = True
                return_json["message"] = "Authentication success!"
            else:
                return_json["success"] = False
                return_json["errors"] = "Error! Invalid Credintials! "
        else:
            return_json["success"] = False
            return_json["errors"] = "Error! Invalid Credintials! "
    else:
        return_json["success"] = False
        return_json["errors"] = "Error! use post requests and send json! "
    return jsonify({"result": return_json})


@app.route('/meds', methods=['GET'])
def get_all_medicine():
    return jsonify({"result": list(medicine.find())})


@app.route('/med', methods=['GET', 'POST'])
def get_one_med():
    common_name = request.args.get('common_name')
    s = medicine.find_one({'common_name': common_name})
    if s:
        output = s
    else:
        output = "No such name Err1" + str(common_name)
    return jsonify({'result': output})


@app.route('/addmed', methods=['POST'])
def add_med():
    med_id = request.args.get('med_id')
    med = {
        "_id": med_id,
        "common_name": request.args.get('common_name'),
        "technical_name": request.args.get('technical_name'),
        "price": request.args.get('price'),
        "schedule": request.args.get('schedule'),
        "prescription": request.args.get('prescription'),
        "description": request.args.get('description'),
        "image_url": request.args.get('image_url')}

    output = medicine.insert_one(med)
    return jsonify({'result': str(output)})


@app.route('/addmedicine')
def addmedicine():
   return render_template('medicine.html')

@app.route('/addmedicine_post',methods = ['POST', 'GET'])
def addmedicine_post():
    if request.method == 'POST':
        medicine_dict = {
            'technical_name' : request.form['technical_name'],
            'common_name' : request.form['common_name'],
            'price' : request.form['price'],
            'schedule' : request.form['schedule'],
            'description' : request.form['description'],
            'prescription' : request.form['prescription'],
            'company' : request.form['company'],
            '_id' : request.form['id'],
            'image_url' : request.form['image_url']
        }
        medicine.insert_one(medicine_dict)
        output = "Medicine added!"

    else:
        output = "Some error"
    return jsonify({'result': str(output)})


if __name__ == '__main__':
    app.run(debug=True)
