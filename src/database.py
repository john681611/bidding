import copy
DB = {}


def add(key, item):
    DB[key] = item


def get(key):
    return copy.deepcopy(DB[key]) if key in DB else None


def clear():
    global DB
    DB = {}


def get_closed(timestamp):
    return list(filter(lambda x: x['close_time'] == timestamp, DB.values()))
