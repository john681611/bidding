import app
import database
import pytest

@pytest.fixture(autouse=True)
def run_around_tests():
    database.clear()
    yield

def test_process_sell():
    sell =  {'close_time': 20,'item': 'toaster_1','reserve_price': 10.0,'timestamp': 10, 'user_id': 1}
    app.process_sell(sell)
    assert database.get(sell['item']) == sell

def test_process_bid_first_bid():
    sell = {'close_time': 20,'item': 'toaster_2','reserve_price': 10.0,'timestamp': 10, 'user_id': 1, 'bids': {}}
    app.process_sell(sell)
    bid = {'bid_amount': 7.5, 'item': 'toaster_2', 'timestamp': 12, 'user_id': 8}
    assert app.proccess_bid(bid) == {'user_id': 8, 'amount': 7.5, 'timestamp': 12}
    assert database.get('toaster_2')['bids'] == {8:{
        'user_id': 8,
        'amount': 7.5,
        'timestamp': 12
    }}

def test_process_bid_second_bid():
    sell = {'close_time': 20,'item': 'toaster_3','reserve_price': 10.0,'timestamp': 10, 'user_id': 1, 'bids': {
        8: {'user_id': 8, 'amount': 7.5, 'timestamp': 12}
    }}
    app.process_sell(sell)
    bid = {'bid_amount': 8, 'item': 'toaster_3', 'timestamp': 13, 'user_id': 9}
    assert app.proccess_bid(bid) == {'user_id': 9, 'amount': 8, 'timestamp': 13}
    assert database.get('toaster_3')['bids'] == {
        8:{'user_id': 8, 'amount': 7.5, 'timestamp': 12},
        9:{'user_id': 9, 'amount': 8, 'timestamp': 13}
    }

def test_process_bid_second_bid_same_user():
    sell = {'close_time': 20,'item': 'toaster_3','reserve_price': 10.0,'timestamp': 10, 'user_id': 1, 'bids': {
        8:{'user_id': 8, 'amount': 7.5, 'timestamp': 12}
    }}
    app.process_sell(sell)
    bid = {'bid_amount': 8, 'item': 'toaster_3', 'timestamp': 13, 'user_id': 8}
    assert app.proccess_bid(bid) == {'user_id': 8, 'amount': 8, 'timestamp': 13}
    assert database.get('toaster_3')['bids'] == {
        8: {'user_id': 8, 'amount': 8, 'timestamp': 13}
    }

def test_process_bid_lower_second_bid():
    sell = {'close_time': 20,'item': 'toaster_4','reserve_price': 10.0,'timestamp': 10, 'user_id': 1, 'bids': {
        9: {'user_id': 9, 'amount': 8, 'timestamp': 13}
    }}
    app.process_sell(sell)
    bid = {'bid_amount': 7.5, 'item': 'toaster_4', 'timestamp': 14, 'user_id': 9}
    assert app.proccess_bid(bid) == None
    assert database.get('toaster_4')['bids'] == {
        9:{'user_id': 9, 'amount': 8, 'timestamp': 13}
    }

def test_process_bid_no_sell():
    bid = {'bid_amount': 7.5, 'item': 'toaster_4', 'timestamp': 14, 'user_id': 8}
    assert app.proccess_bid(bid) == None

def test_process_bid_closed_sell():
    sell = {'close_time': 20,'item': 'toaster_5','reserve_price': 10.0,'timestamp': 10, 'user_id': 1, 'bids': {}}
    app.process_sell(sell)
    bid = {'bid_amount': 7.5, 'item': 'toaster_5', 'timestamp': 21, 'user_id': 8}
    assert app.proccess_bid(bid) == None
    assert database.get('toaster_5')['bids'] == {}

def test_process_bid_earlier_sell():
    sell = {'close_time': 20,'item': 'toaster_5','reserve_price': 10.0,'timestamp': 10, 'user_id': 1, 'bids': {}}
    app.process_sell(sell)
    bid = {'bid_amount': 7.5, 'item': 'toaster_5', 'timestamp': 9, 'user_id': 8}
    assert app.proccess_bid(bid) == None
    assert database.get('toaster_5')['bids'] == {}

def test_determin_winner_unsold():
    sale = {'close_time': 20,'item': 'toaster_5','reserve_price': 10.0,'timestamp': 10, 'user_id': 1, 'bids': {}}
    assert app.determin_winner(sale) == {
    'close_time': sale['close_time'],
    'item': sale['item'],
    'user_id': '',
    'status': 'UNSOLD',
    'price_paid': '0.00',
    'total_bid_count': 0,
    'highest_bid': '0.00',
    'lowest_bid': '0.00'
    }

def test_determin_winner_one_bid():
    sale = {'close_time': 20,'item': 'toaster_5','reserve_price': 10.0,'timestamp': 10, 'user_id': 1, 'bids': [
        {'user_id': 9, 'amount': 11, 'timestamp': 13}
    ]}
    assert app.determin_winner(sale) == {
    'close_time': sale['close_time'],
    'item': sale['item'],
    'user_id': 9,
    'status': 'SOLD',
    'price_paid': '11.00',
    'total_bid_count': 1,
    'highest_bid': '11.00',
    'lowest_bid': '11.00'
    }

def test_process_commands():
    commands = [
        {'close_time': 20,'item': 'toaster_1','reserve_price': 10.0,'timestamp': 10, 'user_id': 1, 'bids': {}},
        {'bid_amount': 7.5, 'item': 'toaster_1', 'timestamp': 12, 'user_id': 8},
        {'bid_amount': 12.5, 'item': 'toaster_1', 'timestamp': 13, 'user_id': 5},
        {'close_time': 20,'item': 'tv_1','reserve_price': 250.0,'timestamp': 15,'user_id': 8, 'bids': {}}
    ]
    app.process_commands(commands)
    assert database.get('toaster_1') == {'close_time': 20,'item': 'toaster_1','reserve_price': 10.0,'timestamp': 10, 'user_id': 1, 'bids': {
        8:{'user_id': 8, 'amount': 7.5, 'timestamp': 12},
        5:{'user_id': 5, 'amount': 12.5, 'timestamp': 13}
    }}
    assert database.get('tv_1') == {'close_time': 20,'item': 'tv_1','reserve_price': 250.0,'timestamp': 15,'user_id': 8, 'bids': {}}
