from pymongo import MongoClient

mongo_con = MongoClient()
mongo_db = mongo_con['flask-app']
