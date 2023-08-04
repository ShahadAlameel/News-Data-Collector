from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB configuration
MONGODB_URI = 'mongodb://localhost:27017/'
MONGODB_DATABASE = 'guardian_news_articles'
MONGODB_COLLECTION = 'news_articles'

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
collection = db[MONGODB_COLLECTION]

try:
    collection.create_index([("text", "text")])
except OperationFailure as e:
    if "already exists" not in str(e):
        raise



@app.route('/news_articles', methods=['GET'])
def search_articles():
    keyword = request.args.get('keyword')
    if keyword:
        query = {"$text": {"$search": keyword}}
        articles = collection.find(query, {"_id": 0})
    else:
        articles = collection.find({}, {"_id": 0})

    return jsonify(list(articles))

if __name__ == '__main__':
    app.run(debug=True)
