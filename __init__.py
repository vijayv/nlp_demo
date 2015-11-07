from flask import Flask, render_template, Response
from bson import json_util
import pymongo
import datetime
app = Flask(__name__)

mongoClient = pymongo.MongoClient('ds031883.mongolab.com',
    					         port=31883,
			                     connectTimeoutMS=30000,
			                     socketTimeoutMS=None,
			                     socketKeepAlive=True)
db = mongoClient.soundcloudanalytics
db.authenticate('soundcloudninjas',
				password='gunners123',
				mechanism='SCRAM-SHA-1')


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/api/v1/tracks")
def apiv1tracks():
    start_date = datetime.datetime(2015, 11, 4, 2, 00, 0, 000)
    l = [each for each in db.activeTrackDirectory.find({"trackGenre": "Hard"}).limit(10)]
    return Response(
        json_util.dumps(l),
        mimetype="application/json")

@app.route("/api/v1/genres")
def apiv1genres():
    l = [each for each in db.activeTrackDirectory.find().distinct("trackGenre")]
    return Response(
        json_util.dumps(l),
        mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
