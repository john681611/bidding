import copy
db = {}

def add(key, item):
    db[key] = item

def get(key):
    return copy.deepcopy(db[key]) if key in db else None

def clear():
    global db
    db = {}

def get_closed(timestamp): 
    return list(filter(lambda x: x['close_time'] == timestamp, db.values()))