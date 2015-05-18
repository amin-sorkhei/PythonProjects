__author__ = 'sorkhei'

from user import user

# Initializes the number of items, users and ratings

with open('u.info') as tmp:
    lines = tmp.readlines()
    num_of_users = int((lines[0].split(' '))[0])
    num_of_items = int((lines[1].split(' '))[0])
    num_of_ratings = int((lines[2].split(' '))[0])

# Initialize the dictionaries regarding the data
users_dict = {}
with open('u.user', 'r') as usr:
    lines = usr.readlines()
    for k in xrange(1, num_of_users + 1):
        id, age, sex, occupation, zipcode = lines[k - 1].strip().split('|')
        users_dict[k] = user(int(id), int(age), sex, occupation, zipcode)

with open('u.data', 'r') as data:
    lines = data.readlines()
    for line in lines:
        user_id, item_id, rating, time_stamp = map(int, line.split('\t'))
        users_dict[user_id].add_rating(item_id, rating, time_stamp)

print num_of_items

