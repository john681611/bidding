import database
import operator

def process_sell(sell):
    database.add(sell['item'], sell)

def proccess_bid(bid):
    item = database.get(bid['item'])
    if item['bids'] != [] and max([x['amount'] for x in item['bids']]) > bid['bid_amount']:
        print('in')
        return
    bid_details = {
        'user_id': bid['user_id'],
        'amount': bid['bid_amount'],
        'timestamp': bid['timestamp']
    }
    item['bids'].append(bid_details)
    database.add(item['item'],item)