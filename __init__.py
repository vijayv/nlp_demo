from flask import Flask, render_template
import pymongo
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


@app.route("/ajax")
def ajax():
    l = db.activeTrackDirectory.find_one()
    return render_template('index.html', collections=l)


if __name__ == "__main__":
    app.run(debug=True)
