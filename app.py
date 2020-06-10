import database
import operator

def get_max_bid(bids): 
    return max([x['amount'] for x in bids])

def process_sell(sell):
    database.add(sell['item'], sell)


def proccess_bid(bid):
    item = database.get(bid['item'])
    if item == None:
        print(f"No item {bid['item']} found for sale")
        return
    elif item['close_time'] < bid['timestamp']:
        print(f"Bid too late closed at {item['close_time']}")
        return
    elif len(item['bids']) > 0 and get_max_bid(item['bids']) > bid['bid_amount']:
        print(f"Bid too low max is {get_max_bid(item['bids'])}")
        return
    
    bid_details = {
        'user_id': bid['user_id'],
        'amount': bid['bid_amount'],
        'timestamp': bid['timestamp']
    }
    item['bids'].append(bid_details)
    database.add(item['item'],item)
    return bid_details