import database
import operator
import utils
import write_file
import parse_file
import copy

def process_sell(sell):
    database.add(sell['item'], sell)


def proccess_bid(bid):
    item = database.get(bid['item'])
    if (item == None or
        item['timestamp'] > bid['timestamp'] or
        item['close_time'] < bid['timestamp'] or
        bid['user_id'] in item['bids'] and item['bids'][bid['user_id']]['amount'] > bid['bid_amount']):
        return
    
    bid_details = {
        'user_id': bid['user_id'],
        'amount': bid['bid_amount'],
        'timestamp': bid['timestamp']
    }

    item['bids'][bid['user_id']] = bid_details
    item['bid_count'] += 1
    if bid['bid_amount'] > item['highest_bid']:
        item['highest_bid'] = bid['bid_amount']
    if bid['bid_amount'] < item['lowest_bid']:
        item['lowest_bid'] = bid['bid_amount']
    database.add(item['item'],item)
    return bid_details

def determin_winner(sale):
    sale = copy.deepcopy(sale)
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
    winner['highest_bid'] = sale['highest_bid']
    winner['lowest_bid'] = sale['lowest_bid']
    winning_bid = utils.get_winning_bid(bids)
    if winning_bid['price_paid'] > sale['reserve_price']:
        winner['status'] = 'SOLD'
        winner['user_id'] = winning_bid['user_id']
        winner['price_paid'] =  winning_bid['price_paid'] if len(bids.values()) == 1 else sale['reserve_price']


    return winner

def process_commands(commands, output):
    for command in commands:
        if 'bid_amount' in command:
            proccess_bid(command)
        elif 'close_time' in command:
            process_sell(command)
        else:
            closed = database.get_closed(command['timestamp'])
            for sale in closed:

                winner = determin_winner(sale)
                write_file.write(write_file.format_data(copy.deepcopy(winner)), output)

def run(input, output):
   commands = list(map(parse_file.parse_message,parse_file.read_file(input)))
   process_commands(commands, output)