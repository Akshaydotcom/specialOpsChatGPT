# from sanic import Sanic
# from sanic_cors import CORS
# from sanic.response import json
# from motor.motor_asyncio import AsyncIOMotorClient
#
# app = Sanic(__name__)
# CORS(app)
# client = AsyncIOMotorClient('mongodb://localhost:27017')
# # Replace with your MongoDB connection URL
# db = client['nutrition']  # Replace with your database name
# collection = db['nutrition_health&population']
# collection2=db['nutrition_nutrientsOfMeals']
# # Define your routes and database operations here...
#
# @app.route('/home', methods=['GET'])
# async def login(request):
#     data = await collection['login_collection'].find().to_list(None)
#     for members in data:
#         members['_id'] = str(members['_id'])
#     return json(data)
#
# @app.route('/users/client', methods=['GET'])
# async def get_all_users(request):
#     limit = request.args.get('limit', default=10)  # Get the 'limit' query parameter, defaulting to 10 if not provided
#     limit = int(limit)
#     skip = int(request.args.get('skip', default=0))  # Get the 'skip' query parameter, defaulting to 0 if not provided
#
#     data = await collection.find().skip(skip).limit(limit).to_list(None)
#     for document in data:
#         document['_id'] = str(document['_id'])
#     return json(data)
#
# def get_all_nutrients():
#     data=collection2.find().to_list(None)
#     for document in data:
#         document['_id'] = str(document['_id'])
#     return json(data)
# if __name__ == '__main__':
#     app.run()

from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import json

app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://localhost:27017')
# Replace with your MongoDB connection URL
db = client['nutrition']  # Replace with your database name
collection = db['nutrition_health&population']
collection2 = db['nutrition_nutrientsOfMeals']
# Define your routes and database operations here...
from flask import jsonify


@app.route('/home', methods=['GET'])
def login():
    data = list(db['login_collection'].find())
    for members in data:
        members['_id'] = str(members['_id'])
    return jsonify(data)


@app.route('/users/client', methods=['GET'])
def get_all_users():
    data = list(collection.find())
    for document in data:
        document['_id'] = str(document['_id'])
    return jsonify(data)


def get_recipe(name):
    data = list(collection2.find(name))
    return data[0].get("recipe")

def get_nutrients(name):
    data = list(collection2.find(name))
    return data[0].get("nutrients")

def get_and_compare_nutrients(meal1,meal2):
    data1 = list(collection2.find(meal1))
    data2= list(collection2.find(meal2))
    return [data1[0].get("nutrients"),data2[0].get("nutrients")]


if __name__ == '__main__':
    app.run()
