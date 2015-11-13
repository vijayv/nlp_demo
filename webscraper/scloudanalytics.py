import soundcloud
import datetime
import time
import csv
import pymongo
import threading
import time
from getTrackInfo import trackSnapshot, getAllSnapshots, easy_parallize


class trackSnapshotThread(threading.Thread):

	def __init__(self,threadId, url):
		threading.Thread.__init__(self)
		self.threadId = threadId
		self.url = url

	def start(self):

		trackSnapshot(self.url)



# create client object with app and user credentials
client = soundcloud.Client(client_id='41d3aaf4c515a5fd20d87d7b21f0dd42',
                           client_secret='9d66914136406bfb53ce452cc85392d9',
                           username='peoplemademusic',
                           password='At0mic49')

# print authenticated user's username
print 'Client Username:', client.get('/me').username
print

# initialize db
mongoClient = pymongo.MongoClient('ds031883.mongolab.com',
								 port=31883,
			                     connectTimeoutMS=30000,
			                     socketTimeoutMS=None,
			                     socketKeepAlive=True)
db = mongoClient.soundcloudanalytics
db.authenticate('soundcloudninjas',
				password='gunners123',
				mechanism='SCRAM-SHA-1')

# post frequency test db
uploadRate = db.uploadRate

# tracks directory db
activeTrackDirectory = db.activeTrackDirectory


def startPostFrequencyTest(cycles=1):

	counter = 0

	timestamp = datetime.datetime.now()

	numCycles = cycles

	postInfo = []
	postInfoDb = []

	while counter < numCycles:

		print
		print "------Cycle", counter+1, "of", numCycles, "------"

		postId = postFrequencyTest()

		timestamp = datetime.datetime.now()
		print "Current Time:", timestamp

		timestamp2 = time.time()

		tempPostInfo = []
		tempPostInfo.append(timestamp2)
		tempPostInfo.append(postId)
		postInfo.append(tempPostInfo)

		tempPostInfoDb = {}
		tempPostInfoDb['timestamp'] = timestamp2
		tempPostInfoDb['trackId'] = postId
		postInfoDb.append(tempPostInfoDb)

		counter += 1

		time.sleep(8)

	print postInfo

	with open('postFrequencyTest.csv', 'w') as output_file:
		dw = csv.writer(output_file, postInfo, delimiter=',')
		dw.writerow(['timestamp', 'postId'])
		dw.writerows(postInfo)


	for post in postInfoDb:
		uploadRate.insert(post)

def postFrequencyTest():

	pageSize = 200
	offset = 0
	trackId = 0

	for i in range(1):

		tracks = client.get('/tracks', id='700000000', limit=pageSize, offset=offset)

		first_track = 0

		for track in tracks:

			try:

				trackId = int(track.id)
				print "Track ID:", track.id
				return trackId

			except:

				print "Track ID error!"
				return

		offset += (i * pageSize)


def getNewTracksOld():

	returnedTracks = []
	tracks = ''
	pageSize = 200
	offset = 0
	page = 1

	for i in range(10):

		print
		print "---------Getting page", page, "of results from SoundCloud..."

		page += 1

		#tracks = client.get('/tracks', genres='nudisco', limit=pageSize, offset=offset)

		try:
			tracks = client.get('/tracks', id='300000000', limit=pageSize, offset=offset)

		except Exception as e:
			print "Error making API call! ---", e
			pass

		for track in tracks:

			tempTrack = {}

			print
			print "Track:", track
			print

			timeStamp = time.time()

			tempTrack['timeStamp'] = timeStamp
			print "Time Stamp:", timeStamp

			try:
				tempTrack['trackTitle'] = track.title
				print "Title:", track.title
			except:
				print "Title error!"

			try:
				tempTrack['trackId'] = int(track.id)
				print "Track ID:", track.id
			except:
				print "Track ID error!"

			try:
				tempTrack['trackUrl'] = track.permalink_url
				print "Track URL:", track.permalink_url
			except:
				print "Track URL error!"

			try:
				tempTrack['trackCreatedAt'] = track.created_at
				print "Track created at:", track.created_at
			except:
				print "Track Created At error!"

			try:
				tempTrack['trackDuration'] = track.duration
			except:
				print "Track Duration error!"

			try:
				tempTrack['trackGenre'] = track.genre
				print "Genre:", track.genre
			except:
				print "Genre error!"

			try:
				tempTrack['trackTagList'] = track.tag_list
				print "Track Tags:", track.tag_list
			except:
				print "Track Tags error!"

			try:
				tempTrack['commentable'] = track.commentable
			except:
				print "Track Commentable error!"

			try:
				tempTrack['trackUserId'] = track.user_id
				print "Poster User ID:", track.user_id
			except:
				print "Poster User ID error!"

			try:
				tempTrack['trackUsername'] = track.user['username']
				print "Poster User Name:", track.user['username']
			except:
				print "Poster User Name error!"

			returnedTracks.append(tempTrack)

		offset += (i * pageSize)

	writeTracksToDb(returnedTracks)

	print
	print "Found", len(returnedTracks), "tracks!"

def writeTracksToDb(tracks):

	print
	print
	print "-----------------------------------"
	print "Writing tracks to db..."

	thread = ''

	for track in tracks:
		comparison = activeTrackDirectory.find({'trackId': track['trackId']})

		if comparison.count() == 0:
			# print
			# print "-------------------------------"
			# print "New track! Updating db..."
			activeTrackDirectory.insert(track)

		else:
			# print
			# print "------------------------------"
			# print "Track already in db!"
			continue

	return


def halfHourIntervals(startTime, endTime):

	startHour = startTime.hour
	endHour = endTime.hour

	try:
		formattedYear = str(startTime.year)
	except:
		print "Incorrectly formatted year - please enter an INT or STR after 1971 in YYYY format"

	try:
		formattedMonth = str(startTime.month)
	except:
		print "Incorrectly formatted month - please enter an INT or STR between 1 & 12"

	try:
		formattedDay = str(startTime.day)
	except:
		print "Incorrectly formatted day - please enter an INT or STR between 1 & 31"


	for i in range(startHour, endHour + 2):
		hour = i

		for i2 in range(2):
			halfHour = i2
			print "i2 =", halfHour
			getNewTracks(formattedYear, formattedMonth, formattedDay, hour, halfHour)


def getNewTracks(year=0, month=0, day=0, hour=0, halfHour=0):

	returnedTracks = []
	tracks = ''
	pageSize = 200
	offset = 0
	page = 1

	year = year

	if month < 10:
		formattedMonth = '0' + str(month)
	else:
		formattedMonth = str(month)

	if day < 10:
		formattedDay = '0' + str(day)
	else:
		formattedDay = str(day)

	if hour < 10:
		formattedHour = '0' + str(hour)
	else:
		formattedHour = str(hour)

	if halfHour == 0:
		firstHalfHour = '00:00'
		secondHalfHour = '30:00'
	elif halfHour == 1:
		firstHalfHour = '30:00'
		secondHalfHour = '59:59'

	startTimestamp = str(year) + '-' + formattedMonth + '-' + formattedDay + ' ' + formattedHour + ':' + firstHalfHour
	endTimestamp = str(year) + '-' + formattedMonth + '-' + formattedDay + ' ' + formattedHour + ':' + secondHalfHour

	print 'Start Timestamp = ', startTimestamp
	print 'End Timestamp = ', endTimestamp

	for i in range(10):

		print
		print "---------Getting page", page, "of results from SoundCloud..."

		page += 1

		#tracks = client.get('/tracks', genres='nudisco', limit=pageSize, offset=offset)

		try:
			if year != 0:
				tracks = client.get('/tracks', created_at={'from': startTimestamp, 'to': endTimestamp}, limit=pageSize, offset=offset)

			else:
				tracks = client.get('/tracks', id='300000000', limit=pageSize, offset=offset)

		except Exception as e:
			print "Error making API call! ---", e
			pass

		for track in tracks:

			tempTrack = {}

			# print
			# print "Track:", track
			# print

			timeStamp = time.time()

			tempTrack['timeStamp'] = timeStamp
			# print "Time Stamp:", timeStamp

			try:
				tempTrack['trackTitle'] = track.title
				# print "Title:", track.title
			except:
				print "Title error!"


			try:
				tempTrack['trackId'] = int(track.id)
				# print "Track ID:", track.id
			except:
				print "Track ID error!"

			try:
				tempTrack['trackUrl'] = track.permalink_url
				# print "Track URL:", track.permalink_url
			except:
				print "Track URL error!"

			try:
				tempTrack['trackCreatedAt'] = track.created_at
				# print "Track created at:", track.created_at
			except:
				print "Track Created At error!"

			try:
				tempTrack['trackDuration'] = track.duration
				# print "Track duration:", track.duration
			except:
				print "Track Duration error!"

			try:
				tempTrack['trackGenre'] = track.genre
				# print "Genre:", track.genre
			except:
				print "Genre error!"

			try:
				tempTrack['trackTagList'] = track.tag_list
				# print "Track Tags:", track.tag_list
			except:
				print "Track Tags error!"

			try:
				tempTrack['commentable'] = track.commentable
				# print "Track commentable:", track.commentable
			except:
				print "Track Commentable error!"

			try:
				tempTrack['trackUserId'] = track.user_id
				# print "Poster User ID:", track.user_id
			except:
				print "Poster User ID error!"

			try:
				tempTrack['trackUsername'] = track.user['username']
				# print "Poster User Name:", track.user['username']
			except:
				print "Poster User Name error!"

			tempTrack['snapshots'] = []
			tempTrack['dailyAggregatePlays'] = []

			returnedTracks.append(tempTrack)

		offset += (i * pageSize)

	writeTracksToDb(returnedTracks)

	print
	print "Found", len(returnedTracks), "tracks!"


def deleteBottomXPercent(now, deletionPercentage, numDaysBack, removeStartDate=False):

	dividend = 100 / deletionPercentage
	daysBack = numDaysBack
	now = now

	createdAtEnd = now - datetime.timedelta(days=daysBack)
	createdAtStart = now - datetime.timedelta(days=daysBack+1)

	startYear = str(createdAtStart.year)
	startMonth = createdAtStart.month
	if startMonth < 10:
		startMonth = '0' + str(startMonth)

	startDay = createdAtStart.day
	if startDay < 10:
		startDay = '0' + str(startDay)

	startHour = createdAtStart.hour
	if startHour < 10:
		startHour = '0' + str(startHour)

	startMin = createdAtStart.minute
	if startMin < 10:
		startMin = '0' + str(startMin)

	formattedStart = str(startYear) + '/' + str(startMonth) + '/' + str(startDay) + ' ' + str(startHour) + ':' + str(startMin) + ':00 +0000'

	endYear = str(createdAtEnd.year)
	endMonth = createdAtEnd.month
	if endMonth < 10:
		endMonth = '0' + str(endMonth)

	endDay = createdAtEnd.day
	if endDay < 10:
		endDay = '0' + str(endDay)

	endHour = createdAtEnd.hour
	if endHour < 10:
		endHour = '0' + str(endHour)

	endMin = createdAtEnd.minute
	if endMin < 10:
		endMin = '0' + str(endMin)

	formattedEnd = str(endYear) + '/' + str(endMonth) + '/' + str(endDay) + ' ' + str(endHour) + ':' + str(endMin) + ':00 +0000'

	removalSet = []
	print
	print "--------- Deleting bottom", deletionPercentage, "percent of tracks from",
	print formattedStart,

	if removeStartDate:
		queriedTracks = activeTrackDirectory.find({'trackCreatedAt': {'$lte': formattedEnd}})

		numResults = queriedTracks.count()
		print "Queries matched before removal:", numResults

		removalNumber = numResults / dividend
		print "Removing", removalNumber, "tracks..."

		last7DaysPlays = []

		for track in queriedTracks:
			plays7DaysAgo = track['dailyAggregatePlays'][-7]
			playsYesterday = track['dailyAggregatePlays'][-1]

			last7DaysPlays.append([playsYesterday - plays7DaysAgo, track])

		last7DaysPlaysSorted = sorted(last7DaysPlays)

		counter = 0

		for track in last7DaysPlaysSorted:
			if counter < removalNumber:
				counter += 1
				removalSet.append(track[1])

		easy_parallize(deleteDocument, removalSet)


	else:
		print "to",
		print formattedEnd
		queriedTracks = activeTrackDirectory.find({'trackCreatedAt': {'$gt': formattedStart, '$lte': formattedEnd}}).sort("currentPlays", pymongo.ASCENDING)

		numResults = queriedTracks.count()
		print "Queries matched before removal:", numResults

		removalNumber = numResults / dividend
		print "Removing", removalNumber, "tracks..."

		counter = 0

		for track in queriedTracks:
			if counter < removalNumber:
				counter += 1
				removalSet.append(track)

		easy_parallize(deleteDocument, removalSet)

		queriedTracks2 = activeTrackDirectory.find({'trackCreatedAt': {'$gt': formattedStart, '$lte': formattedEnd}}).sort("currentPlays", pymongo.ASCENDING)
		numResults2 = queriedTracks.count()
		print "Queries matched after removal:", numResults2

def deleteDocument(track):

	try:
		result = activeTrackDirectory.remove({'trackId': track['trackId']})

	except Exception as e:
		print "---Error deleting from db! ---", e


def masterProcess():
	global client

	sleepTimeMins = 15
	gracePeriod = 0 # counted in days
	deletionPercentage = 50
	longTermDeletionPercentage = 1 # percent to be deleted after grace period

	while True:

		now = datetime.datetime.now()

		getSnapshotsStartTime = ''
		getSnapshotsEndTime = ''

		print "Current Hour:", now.hour
		print "Current Minute:", now.minute
		print

		if now.hour == 0 and now.minute >= 30:
		# if now.hour == 22 and now.minute >= 30:
			getSnapshotsStartTime = datetime.datetime.now()
			getAllSnapshots()

			client = soundcloud.Client(client_id='41d3aaf4c515a5fd20d87d7b21f0dd42',
                           client_secret='9d66914136406bfb53ce452cc85392d9',
                           username='peoplemademusic',
                           password='At0mic49')

			for i in range(1, gracePeriod + 1):
				# NEED TO FIGURE OUT IF THE FIRST PARAMETER BELOW SHOULD BE now (ABOVE) INSTEAD OF THE EXACT MOMENT AT THIS POINT
				deleteBottomXPercent(datetime.datetime.now(), deletionPercentage, i)

			# COME BACK TO THIS - FOR DELETING BOTTOM 1%
			# deleteBottomXPercent(datetime.datetime.now(), longTermDeletionPercentage, gracePeriod, True)

			getSnapshotsEndTime = datetime.datetime.now()
			halfHourIntervals(getSnapshotsStartTime, getSnapshotsEndTime)

		else:

			beforeSize = activeTrackDirectory.count()
			getNewTracks()
			print
			print "Track Directory size before:", beforeSize
			print "Track Directory size after:", activeTrackDirectory.count()
			print activeTrackDirectory.count() - beforeSize, "new tracks added!"
			print "Sleeping for", sleepTimeMins, "mins before next API call..."
			print

			time.sleep(sleepTimeMins * 60)

if __name__ == '__main__':


	masterProcess()
