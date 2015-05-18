__author__ = 'sorkhei'

class user:

    def __init__(self, id, age, gender, occupation, zipcode):
        self.id = id
        self.age = age
        self.gender = gender
        self.occupation = occupation
        self.zipcode = zipcode
        self.watched_movies = []
        self.score = {}

    def add_rating(self, movie_id, rating, time_stamp):
        self.watched_movies.append(movie_id)
        self.watched_movies.sort()
        self.score[movie_id] = (rating, time_stamp)