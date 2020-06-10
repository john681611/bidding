db = {}

def add(key, item):
    db[key] = item

def get(key):
    return db[key] if key in db else None
