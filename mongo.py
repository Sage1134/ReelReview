import pymongo, asyncio


def get_database():
    Cluster = pymongo.MongoClient("mongodb+srv://ReelReview12345:ReelReview12345@reelreview.im8higz.mongodb.net/?retryWrites=true&w=majority")
    Collection = Cluster["ReelReview"]
    return Collection['Movies']


def updateDatabase(MovieName, field, value):
    db = get_database()
    if db.find_one({'_id':MovieName}) is not None:
        movieData = db.find_one({'_id':MovieName})
        movieData['_id'] = MovieName
        movieData[field] = value
        db.find_one_and_replace({'_id':MovieName}, movieData)
    else:
        movieData = {}
        movieData['_id'] = MovieName
        movieData[field] = value
        db.insert_one(movieData)
        return

def databaseGet(MovieName, field, defaultVal):
    db = get_database()
    if db.find_one({'_id':MovieName}) is not None:
        movieData = db.find_one({'_id':MovieName})
        if not field in movieData.keys():
            movieData['_id'] = MovieName
            movieData[field] = defaultVal
            db.find_one_and_replace({'_id':MovieName}, movieData)
    else:
        movieData = {}
        movieData['_id'] = MovieName
        movieData[field] = defaultVal
        db.insert_one(movieData)
    return movieData[field]

async def updateMovieInfo(movieName, field, default):
    current = databaseGet(movieName, field, default)
    updateDatabase(movieName, field, current + 1)

def searchDatabase(movieName, default):
    return [databaseGet(movieName, "Good", default), databaseGet(movieName, "Bad", default)]
