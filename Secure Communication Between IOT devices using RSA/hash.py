import os
import hashlib
from pymongo import MongoClient
def add_user(username, password):
    client = MongoClient("mongodb://localhost:27017/")
    print("CONNECTION ESTABLISHED -")
    db = client.IOT_ISM
    #TODO:sanitize data
    #check to see if that username is already used
    if db.login_info.find_one({"username": username}) is None:
        #hash password
        m = hashlib.sha256()
        m.update(password.encode('utf-8'))
        db.login_info.insert_one({"username": username, "password": m.hexdigest()})
    else:
        print ("Error: Username \""+username+"\" is already in use.")
username = input("username : ")
password = input("password : ")
add_user(username, password)