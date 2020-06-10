import functools
import copy


def get_highest_bid(bids):
    return max([x['amount'] for x in bids.values()])


def get_winning_bid(bids):
    winning_bid_amount = get_highest_bid(bids)
    winning_bid = functools.reduce(
        lambda x, y: x if x['timestamp'] > y['timestamp'] and x['amount'] == winning_bid_amount else y, bids.values())
    del bids[winning_bid['user_id']]
    winning_bid['price_paid'] = get_highest_bid(
        bids) if bids != {} else winning_bid['amount']
    return winning_bid


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
    winning_bid = get_winning_bid(bids)
    if winning_bid['price_paid'] > sale['reserve_price']:
        winner['status'] = 'SOLD'
        winner['user_id'] = winning_bid['user_id']
        winner['price_paid'] = winning_bid['price_paid'] if len(
            bids.values()) == 1 else sale['reserve_price']

    return winner
