import requests
import soundcloud
import datetime
import re
import urllib
import pymongo
import threading
import time
from multiprocessing import Process, Queue, Pool
from bs4 import BeautifulSoup

mongoClient = pymongo.MongoClient()
db = mongoClient.scAnalytics

#trackSnapshotsDb = db.trackSnapshots
activeTrackDirectory = db.activeTrackDirectory

numTracks = 0
counter = 0

def trackSnapshot(url=None):
	global counter

	if url != None:
		tempSnapshot = {}
		counter += 1

		print
		print "-----Processing track", counter, "of", numTracks, "total tracks..."

		try:
			scResponse = requests.get(url, timeout=2.0)
			timeStamp = time.time()
			tempSnapshot['timeStamp'] = timeStamp
			#print "Time Stamp:", timeStamp

			html = scResponse.text
			soup = BeautifulSoup(html)

			# get track id
			try:
				for i in soup.find_all('meta', {'property': 'twitter:player'}):
					if i != None:
						link = i.get('content')
						href = str(urllib.unquote(link).decode('utf8'))
						#print '----full src href=', href

						trackNumberSearch = re.compile('[0-9]+')
						result = re.findall(trackNumberSearch, href)

						trackId = int(result[0])
						tempSnapshot['trackId'] = int(trackId)
						#print "Track ID:", trackId

					else:
						tempSnapshot['trackId'] = None

			except Exception as e:
				print "Error getting trackId! ---", e
				tempSnapshot['trackId'] = None
				

			# get play count
			try:
				for count in soup.find_all('meta', {'property': 'soundcloud:play_count'}):
					if count != None:
						playCount = str(count.get('content'))
						tempSnapshot['trackPlayCount'] = int(playCount)
						#print "Play Count:", playCount

					else:
						tempSnapshot['trackPlayCount'] = None

			except Exception as e:
				print "Error getting play count! ---", e
				tempSnapshot['trackPlayCount'] = None
				

			# get likes count
			try:
				for fav in soup.find_all('meta', {'property': 'soundcloud:like_count'}):
					if fav != None:
						likeCount = str(fav.get('content'))
						tempSnapshot['trackLikeCount'] = int(likeCount)
						#print "Like Count:", likeCount

					else:
						tempSnapshot['trackLikeCount'] = None

			except Exception as e:
				print "Error getting like count! ---", e
				tempSnapshot['trackLikeCount'] = None
				

			# get comments Count
			try:
				for comment in soup.find_all('meta', {'property': 'soundcloud:comments_count'}):
					if comment != None:
						commentCount = str(comment.get('content'))
						tempSnapshot['trackCommentCount'] = int(commentCount)
						#print "Comment Count:", commentCount

					else:
						tempSnapshot['trackCommentCount'] = None

			except Exception as e:
				print "Error getting comment count! ---", e
				tempSnapshot['trackCommentCount'] = None
				

			# get download count
			try:
				for dl in soup.find_all('meta', {'property': 'soundcloud:download_count'}):
					if dl != None:
						downloadCount = str(dl.get('content'))
						tempSnapshot['trackDownloadCount'] = int(downloadCount)
						#print "Download Count:", downloadCount

					else:
						tempSnapshot['trackDownloadCount'] = None

			except Exception as e:
				print "Error getting download count! ---", e
				tempSnapshot['trackDownloadCount'] = None
				

			# get repost count
			try:
				for script in soup.find_all('script'):
					if script != None:
						testText = ''.join(script.find_all(text=True))

						if 'reposts_count' in testText:
							#text = 'webpackJsonp([],{0:function(e,t,a){var c,n,i={"87":[{"id":138025346,"kind":"user","permalink":"ollin-kan","username":"Ollin Kan","last_modified":"2015/03/30 21:32:21 +0000","uri":"https://api.soundcloud.com/users/138025346","permalink_url":"http://soundcloud.com/ollin-kan","avatar_url":"https://i1.sndcdn.com/avatars-000130462076-94xlb1-large.jpg","country":"Belgium","first_name":null,"last_name":null,"full_name":"","description":"Mexican/Belgian producer based in Brussels \nBooking: booking@nudiscoyourdisco.com\nIf you love melodies this is the perfect place for you!","city":"Brussels","discogs_name":null,"myspace_name":null,"website":null,"website_title":null,"online":false,"track_count":2,"playlist_count":0,"plan":"Pro Plus","public_favorites_count":1,"followers_count":111,"followings_count":15,"subscriptions":[{"product":{"id":"creator-pro-unlimited","name":"Pro Unlimited"}}],"likes_count":1,"reposts_count":0,"comments_count":23,"url":"/ollin-kan"}],"90":[{"kind":"track","id":198436422,"created_at":"2015/03/30 17:41:19 +0000","user_id":138025346,"duration":271410,"commentable":true,"state":"finished","original_content_size":11059446,"last_modified":"2015/04/04 20:15:07 +0000","sharing":"public","tag_list":"\"Ollin Kan\" \"Down Under\" Remake \"Melodic House\"","permalink":"ollin-kan-down-under","streamable":true,"embeddable_by":"all","downloadable":false,"purchase_url":"http://www.unlockthis.net/Ollinkan/ollin-kan-down-under","label_id":null,"purchase_title":"Free Download","genre":"House","title":"Ollin Kan - Down Under","description":"My remake of the 80s classic of Men At Work. ","label_name":null,"release":null,"track_type":null,"key_signature":null,"isrc":null,"video_url":null,"bpm":null,"release_year":2015,"release_month":3,"release_day":30,"original_format":"mp3","license":"cc-by-nc-sa","uri":"https://api.soundcloud.com/tracks/198436422","user":{"id":138025346,"kind":"user","permalink":"ollin-kan","username":"Ollin Kan","last_modified":"2015/03/30 21:32:21 +0000","uri":"https://api.soundcloud.com/users/138025346","permalink_url":"http://soundcloud.com/ollin-kan","avatar_url":"https://i1.sndcdn.com/avatars-000130462076-94xlb1-large.jpg"},"permalink_url":"http://soundcloud.com/ollin-kan/ollin-kan-down-under","artwork_url":"https://i1.sndcdn.com/artworks-000111773495-6js59c-large.jpg","waveform_url":"https://w1.sndcdn.com/UArXnKlsoXfZ_m.png","stream_url":"https://api.soundcloud.com/tracks/198436422/stream","playback_count":3374,"download_count":0,"favoritings_count":160,"comment_count":15,"likes_count":160,"reposts_count":48,"attachments_uri":"https:'
							filter1 = re.compile('reposts\\_count\\"\\:\d+')
							results = re.findall(filter1, testText)
							results2 = re.search('\d+', results[1])

							repostsCount = results2.group(0)
							tempSnapshot['repostsCount'] = int(repostsCount)
							#print "Reposts Count:", repostsCount

						else:
							tempSnapshot['repostsCount'] = None

			except Exception as e:
				print "Error getting reposts count! ---", e
				tempSnapshot['repostsCount'] = None
				

		except Exception as e:
			print "Error getting track info! ---", e
		#trackSnapshots.insert(tempSnapshot)

		try:
			if len(tempSnapshot.keys()) > 0:
				return tempSnapshot

			else:
				return

		except Exception as e:
			print "Error! ---", e

	else:
		print "URL given is None!"
		return


def getAllSnapshots():
	global numTracks

	trackUrls = []
	dbTracks = activeTrackDirectory.find()
	count = 0

	for track in dbTracks:
		tempUrl = track['trackUrl']

		if count < activeTrackDirectory.count():
		#if count < 101:
			count += 1
			trackUrls.append(tempUrl)

		else:
			break

	actualNumTracks = len(trackUrls)
	numTracks = actualNumTracks / 4
	
	print
	print "----------------Tracking", actualNumTracks, "tracks..."
	print

	trackSnapshots = easy_parallize(trackSnapshot, trackUrls)
	numDbErrors = 0

	for track in trackSnapshots:

		#print track
		try:
			activeTrackDirectory.update({'trackId': track['trackId']},
			   {'$push': {'snapshots': track},
			   '$push': {'dailyAggregatePlays': track['trackPlayCount']},
			    '$set': {
			    	'currentPlays': track['trackPlayCount'],
			    	'currentReposts': track['repostsCount'],
			    	'currentLikes': track['trackLikeCount'],
			    	'currentComments': track['trackCommentCount'],
			    	'currentDownloads': track['trackDownloadCount']
			    }})

		except Exception as e:
			numDbErrors += 1
			print
			print "Error! ---", e
			print track

	print "Num DB errors =", numDbErrors
	# updatedTracks = activeTrackDirectory.find({})
	# count = 0
	# errorCount = 0

	# for track in updatedTracks:
	# 	try:
	# 		if len(track['snapshots']) > 1:
	# 			count += 1

	# 	except:
	# 		errorCount += 1
	# 		continue

	# print count, "tracks with more than 1 snapshot"
	# print errorCount, "tracks with a processing error"


def easy_parallize(function, sequence):

	startTime = time.time()
	pool = Pool()

	# f is given sequence. guaranteed to be in order
	result = pool.map(function, sequence)
	cleaned = [x for x in result if not x is None]
	#cleaned = asarray(cleaned)
	# not optimal but safe

	pool.close()
	pool.join()

	endTime = time.time()
	runTime = endTime - startTime

	print "--------Processing Run Time:", runTime

	return cleaned


def getTracksWithGteXPlays(numPlays):

	queriedTracks = activeTrackDirectory.find({'currentPlays': {'$gte': numPlays}}).sort('currentPlays', -1)

	for track in queriedTracks:

		print track['trackTitle']
		print track['currentPlays']
		print track['trackCreatedAt']
		print track['trackId']
		print

	print "There are", queriedTracks.count(), "tracks with at least", numPlays, "plays"


def getTrackPlayHistory(trackId):

	queriedTrack = activeTrackDirectory.find_one({'trackId': trackId})

	trackSnapshots = queriedTrack['snapshots']

	for snapshot in trackSnapshots:

		formattedTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(snapshot['timeStamp']))

		print formattedTime,
		print snapshot['trackPlayCount']

	#print trackSnapshots
	print
	print len(trackSnapshots)

if __name__ == '__main__':

	#getAllSnapshots()

	#getTracksWithGteXPlays(500)

	getTrackPlayHistory(225624884)

	#trackSnapshot('https://soundcloud.com/jaxjones/yeah-yeah-yeah')