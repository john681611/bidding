import database
import operator

def process_sell(sell):
    database.add(sell['item'], sell)


def proccess_bid(bid):
    item = database.get(bid['item'])
    if item == None:
        print(f"No item {bid['item']} found for sale")
        return
    elif item['timestamp'] > bid['timestamp']:
        print(f"Bid too early opens at {item['timestamp']}")
        return 
    elif item['close_time'] < bid['timestamp']:
        print(f"Bid too late closed at {item['close_time']}")
        return
    elif bid['user_id'] in item['bids'] and item['bids'][bid['user_id']]['amount'] > bid['bid_amount']:
        print(f"Bid too low max is {item['bids'][bid['user_id']]['amount']}")
        return
    
    bid_details = {
        'user_id': bid['user_id'],
        'amount': bid['bid_amount'],
        'timestamp': bid['timestamp']
    }
    item['bids'][bid['user_id']] = bid_details
    database.add(item['item'],item)
    return bid_details

def determin_winner(sale):
    winner = {
    'close_time': sale['close_time'],
    'item': sale['item'],
    'user_id': '',
    'status': 'UNSOLD',
    'price_paid': '0.00',
    'total_bid_count': 0,
    'highest_bid': '0.00',
    'lowest_bid': '0.00'
    }
    if len(sale['bids']):
        pass
    return winner

def process_commands(commands):
    for command in commands:
        if 'bid_amount' in command:
            proccess_bid(command)
        elif 'close_time' in command:
            process_sell(command)
