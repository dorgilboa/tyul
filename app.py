from flask import Flask, g , current_app, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import gunicorn
import sqlite3, hashlib


app = Flask(__name__)
cors = CORS(app)
api = Api(app)
app.config['CROSS_HEADERS'] = 'Content-Type'
web = gunicorn.SERVER

@app.route('/')
def hello_world():
    return 'Hello, World!'

DATABASE_PATH = 'database.db'

def connect_db():
    with app.app_context():
        ### data
        print("trying to connect to db")
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE_PATH)
            print(f"connected to db {db}")
        return db

def create_tables():
    cur = connect_db().cursor()
    try:
        # cur.execute('CREATE TABLE Users (username,password,email)')
        # cur.execute('CREATE TABLE Tracks (track_num INTEGER PRIMARY KEY, coords, track_name, username)')
        pass
    except Exception as err:
        print(err)
        raise err

def get_tracks():
    cur = connect_db().cursor()
    tracks = cur.execute('SELECT * FROM Tracks')
    return tracks

class RegisterSystem(Resource):
    def get(self):
        cur = connect_db().cursor()
        try:
            cur.execute("SELECT * from Users")
            users = cur.fetchall()
            print(users)
            return {'success': True, 'data': users}
        except Exception as err:
            error_msg = f"error while trying to get data : {err=}"
            print(error_msg)
            return {'success': False, 'error_msg': error_msg}
        return {'hello': 'world'}


    def post(self):
        username = request.form['username']
        password = request.form['password']
        try:
            hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest() #securing pw in db
        except Exception as err:
            error_msg = f"error while trying to encrypt password : {err=}"
            print(error_msg)
            return {'success': False, 'error_msg': error_msg}

        email = request.form['email']
        print(f"{username=}, {hashed_password=} , {email=}")
        db = connect_db()
        cur = db.cursor()
        try:
            sqlite_insert_with_params = """
            INSERT into Users (username, password, email) VALUES(?, ?, ?);
            """
            cur.execute(sqlite_insert_with_params, (username, hashed_password, email))
            db.commit()
            return {'success': True, 'data': 'Username created '}
        except Exception as err:
            error_msg = f"error while trying to add username : {err=}"
            print(error_msg)
            return {'success': False, 'error_msg': error_msg}

class LoginSystem(Resource):
    def get(self):
        cur = connect_db().cursor()
        try:
            cur.execute("SELECT * from Users")
            users = cur.fetchall()
            print(users)
            return {'success': True, 'data': users}
        except Exception as err:
            error_msg = f"error while trying to get data : {err=}"
            print(error_msg)
            return {'success': False, 'error_msg': error_msg}
        return {'hello': 'world'}


    def post(self):
        # gets information by: "username=***&password=***"
        # make username/email insert option
        username = request.form['username']
        password = request.form['password']
        try:
            hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        except Exception as err:
            error_msg = f"error while trying to encrypt password : {err=}"
            print(error_msg)
            return {'success': False, 'error_msg': error_msg}

        print(f"{username=}, {hashed_password=}")
        db = connect_db()
        cur = db.cursor()
        try:
            sqlite_insert_with_params = """
            SELECT * FROM Users Where username=? and password=?
            """
            cur.execute(sqlite_insert_with_params, (username, hashed_password))
            exists = cur.fetchall()
            print(exists)
            if exists:
                return {'success': True}
            else:
                return {'success': False}

            db.commit()
            return {'success': True, 'data': 'Username created '}
        except Exception as err:
            error_msg = f"error while trying to add username : {err=}"
            print(error_msg)
            return {'success': False, 'error_msg': error_msg}

class SaveTrackSystem(Resource):
    def get(self):
        cur = connect_db().cursor()
        try:
            cur.execute("SELECT * from Tracks")
            tracks = cur.fetchall()
            print(tracks)
            return {'success': True, 'data': tracks}
        except Exception as err:
            error_msg = f"error while trying to get data : {err=}"
            print(error_msg)
            return {'success': False, 'error_msg': error_msg}
        return {'hello': 'world'}


    def post(self):
        content = request.get_json()#['name']
        name= content['name']
        coordinates = content['coordinates']
        username = content['username']
        db = connect_db()
        cur = db.cursor()
        print(name, coordinates)
        try:
            coordinates = str(coordinates)
            sqlite_insert_with_params = """
            INSERT into Tracks (coords, track_name, username) VALUES(?, ?, ?);
            """
            cur.execute(sqlite_insert_with_params, (coordinates, name, username))
            db.commit()
            return {'success': True, 'data': 'Track added successfully'}
        except Exception as err:
            error_msg = f"error while trying to add track : {err=}"
            print(error_msg)
            return {'success': False, 'error_msg': error_msg}

api.add_resource(RegisterSystem, '/register')
api.add_resource(LoginSystem, '/login')
api.add_resource(SaveTrackSystem, '/home')


if __name__ == '__main__':
    app.run(debug=True)
