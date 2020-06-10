
import math
def read_file(location):
    with open(location, 'r') as text_file:
        contents = text_file.read()
    return contents.strip().split('\n')

def parse_message(message):
    parts = message.split('|')
    if "SELL" in message:
        return {
        'timestamp': int(parts[0]),
        'user_id': int(parts[1]),
        'item': parts[3],
        'reserve_price': float(parts[4]),
        'close_time': int(parts[5]),
        'bids': {},
        'bid_count': 0 ,
        'lowest_bid': math.inf,
        'highest_bid': 0,
        }
    elif "BID" in message:
        return {
        'timestamp': int(parts[0]),
        'user_id': int(parts[1]),
        'item': parts[3],
        'bid_amount': float(parts[4]),
        }
    else:
        return {'timestamp': int(message)}

def parse_file(location): 
    return list(filter(lambda x: x is not None, map(parse_message, read_file(location))))