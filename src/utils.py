
import functools


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
