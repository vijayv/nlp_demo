from flask import Flask, render_template, Response, request
from bson import json_util
from bson.son import SON
from APIv1 import APIv1, APIFieldConstants
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

sca_api = APIv1()

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/api/v1/tracks")
def apiv1tracks():
    '''
    will return all tracks from db that match the given criteria

    can filter on specific fields by using:


    fields = ";" delimited list of fields to return.
    limit = number of results to return.
    sort = ";" delimited list of fields to sort by descending.

    examples:
    http://localhost:5000/api/v1/tracks?fields=track_user_name;current_plays;current_comments
    http://localhost:5000/api/v1/tracks?fields=track_user_name;current_plays;current_comments&limit=10&sort=current_comments;current_plays
    '''

    find_params = {}
    field_params = {}
    sort_params = [("_id", -1)]
    limit = 100

    find_params = {"currentPlays": {"$gte": 100}}
    if "fields" in request.args:
        field_params = sca_api.to_field_params(request.args.get("fields").split(";"))

    if "sort" in request.args:
        sort_params = sca_api.to_sort_params(request.args.get("sort").split(";"))

    if "limit" in request.args:
        limit = int(request.args.get("limit"))

    l = [each for each in db.activeTrackDirectory.find(
        find_params,
        field_params,
        ).sort(sort_params).limit(limit)]
    return Response(
        json_util.dumps(l),
        mimetype="application/json",
        )


@app.route("/api/v1/track")
def apiv1track():
    '''
    will return entire track collection for a given trackId
    example: http://localhost:5000/api/v1/track?track_id=226658780
    '''
    try:
        track_id = int(request.args.get("track_id"))
    except:
        # TODO: add an error handler when track_id is not passed
        pass

    l = db.activeTrackDirectory.find_one({"trackId": track_id})
    return Response(
        json_util.dumps(l),
        mimetype="application/json")


@app.route("/api/v1/genres")
def apiv1genres():
    '''
    return the n most common genres from the db
    '''
    l = [each for each in db.activeTrackDirectory.aggregate(
        [
            {"$group": {"_id": "$trackGenre", "count": {"$sum": 1}}},
            {"$sort": SON([("count", -1)])},
            {"$limit": 20 }
        ]
    )["result"]]

    return Response(
        json_util.dumps(l),
        mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
