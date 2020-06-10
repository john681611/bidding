import database
import operator
import utils

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
    item['bid_count'] += 1
    database.add(item['item'],item)
    return bid_details

def determin_winner(sale):
    winner = {
    'close_time': sale['close_time'],
    'item': sale['item'],
    'user_id': '',
    'status': 'UNSOLD',
    'price_paid': 0,
    'total_bid_count': 0,
    'highest_bid': 0,
    'lowest_bid': 0
    }
    if sale['bids'] == {}:
        return winner
    bids = sale['bids']
    winner['total_bid_count'] = sale['bid_count']
    winner['highest_bid'] = utils.get_highest_bid(bids)
    winner['lowest_bid'] = utils.get_lowest_bid(bids)
    winning_bid = utils.get_winning_bid(bids)
    if winning_bid['price_paid'] > sale['reserve_price']:
        winner['status'] = 'SOLD'
        winner['user_id'] = winning_bid['user_id']
        winner['price_paid'] =  winning_bid['price_paid'] if len(bids.values()) == 1 else sale['reserve_price']


    return winner

def process_commands(commands):
    for command in commands:
        if 'bid_amount' in command:
            proccess_bid(command)
        elif 'close_time' in command:
            process_sell(command)
