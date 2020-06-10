import app
import database
import pytest
import math


@pytest.fixture(autouse=True)
def run_around_tests():
    database.clear()
    yield


def test_process_sell():
    sell = {'close_time': 20, 'item': 'toaster_1', 'reserve_price': 10.0, 'timestamp': 10,
            'user_id': 1, 'bids': {}, 'bid_count': 0, 'highest_bid': 0, 'lowest_bid': math.inf}
    app.process_sell(sell)
    assert database.get(sell['item']) == sell


def test_process_bid_first_bid():
    sell = {'close_time': 20, 'item': 'toaster_2', 'reserve_price': 10.0, 'timestamp': 10,
            'user_id': 1, 'bids': {}, 'bid_count': 0, 'highest_bid': 0, 'lowest_bid': math.inf}
    app.process_sell(sell)
    bid = {'bid_amount': 7.5, 'item': 'toaster_2',
           'timestamp': 12, 'user_id': 8}
    assert app.proccess_bid(
        bid) == {'user_id': 8, 'amount': 7.5, 'timestamp': 12}
    result = database.get('toaster_2')
    assert result['bids'] == {8: {
        'user_id': 8,
        'amount': 7.5,
        'timestamp': 12
    }}
    assert result['bid_count'] == 1
    assert result['highest_bid'] == 7.5
    assert result['lowest_bid'] == 7.5


def test_process_bid_second_bid():
    sell = {'close_time': 20, 'item': 'toaster_3', 'reserve_price': 10.0, 'timestamp': 10, 'user_id': 1, 'highest_bid': 7.5, 'lowest_bid': 7.5, 'bid_count': 1, 'bids': {
        8: {'user_id': 8, 'amount': 7.5, 'timestamp': 12}
    }}
    app.process_sell(sell)
    bid = {'bid_amount': 8, 'item': 'toaster_3', 'timestamp': 13, 'user_id': 9}
    assert app.proccess_bid(
        bid) == {'user_id': 9, 'amount': 8, 'timestamp': 13}
    assert database.get('toaster_3')['bids'] == {
        8: {'user_id': 8, 'amount': 7.5, 'timestamp': 12},
        9: {'user_id': 9, 'amount': 8, 'timestamp': 13}
    }
    assert database.get('toaster_3')['bid_count'] == 2


def test_process_bid_second_bid_same_user():
    sell = {'close_time': 20, 'item': 'toaster_3', 'reserve_price': 10.0, 'timestamp': 10, 'user_id': 1, 'bid_count': 1, 'highest_bid': 7.5, 'lowest_bid': 7.5, 'bids': {
        8: {'user_id': 8, 'amount': 7.5, 'timestamp': 12}
    }}
    app.process_sell(sell)
    bid = {'bid_amount': 8, 'item': 'toaster_3', 'timestamp': 13, 'user_id': 8}
    assert app.proccess_bid(
        bid) == {'user_id': 8, 'amount': 8, 'timestamp': 13}
    assert database.get('toaster_3')['bids'] == {
        8: {'user_id': 8, 'amount': 8, 'timestamp': 13}
    }
    assert database.get('toaster_3')['bid_count'] == 2


def test_process_bid_lower_second_bid():
    sell = {'close_time': 20, 'item': 'toaster_4', 'reserve_price': 10.0, 'timestamp': 10, 'user_id': 1, 'bid_count': 1, 'bids': {
        9: {'user_id': 9, 'amount': 8, 'timestamp': 13}
    }}
    app.process_sell(sell)
    bid = {'bid_amount': 7.5, 'item': 'toaster_4',
           'timestamp': 14, 'user_id': 9}
    assert app.proccess_bid(bid) is None
    assert database.get('toaster_4')['bids'] == {
        9: {'user_id': 9, 'amount': 8, 'timestamp': 13}
    }
    assert database.get('toaster_4')['bid_count'] == 1


def test_process_bid_no_sell():
    bid = {'bid_amount': 7.5, 'item': 'toaster_4',
           'timestamp': 14, 'user_id': 8}
    assert app.proccess_bid(bid) is None


def test_process_bid_closed_sell():
    sell = {'close_time': 20, 'item': 'toaster_5', 'reserve_price': 10.0,
            'timestamp': 10, 'user_id': 1, 'bids': {}, 'bid_count': 0}
    app.process_sell(sell)
    bid = {'bid_amount': 7.5, 'item': 'toaster_5',
           'timestamp': 21, 'user_id': 8}
    assert app.proccess_bid(bid) is None
    assert database.get('toaster_5')['bids'] == {}
    assert database.get('toaster_5')['bid_count'] == 0


def test_process_bid_earlier_sell():
    sell = {'close_time': 20, 'item': 'toaster_5', 'reserve_price': 10.0,
            'timestamp': 10, 'user_id': 1, 'bids': {}, 'bid_count': 0}
    app.process_sell(sell)
    bid = {
        'bid_amount': 7.5,
        'item': 'toaster_5',
        'timestamp': 9,
        'user_id': 8}
    assert app.proccess_bid(bid) is None
    assert database.get('toaster_5')['bids'] == {}
    assert database.get('toaster_5')['bid_count'] == 0


def test_process_commands():
    with open('src/test/test_output.txt', 'w+') as text_file:
        text_file.write('')
    commands = [
        {'close_time': 20, 'item': 'toaster_1', 'reserve_price': 10.0, 'timestamp': 10,
            'user_id': 1, 'bids': {}, 'bid_count': 0, 'highest_bid': 0, 'lowest_bid': math.inf},
        {'bid_amount': 7.5, 'item': 'toaster_1', 'timestamp': 12, 'user_id': 8},
        {'bid_amount': 12.5, 'item': 'toaster_1', 'timestamp': 13, 'user_id': 5},
        {'close_time': 20, 'item': 'tv_1', 'reserve_price': 250.0, 'timestamp': 15,
            'user_id': 8, 'bids': {}, 'bid_count': 0, 'highest_bid': 0, 'lowest_bid': math.inf},
        {'bid_amount': 20, 'item': 'toaster_1', 'timestamp': 17, 'user_id': 8},
        {'timestamp': 20}
    ]
    app.process_commands(commands, 'src/test/test_output.txt')
    assert database.get('toaster_1') == {'close_time': 20, 'item': 'toaster_1', 'reserve_price': 10.0, 'timestamp': 10, 'user_id': 1, 'bid_count': 3, 'highest_bid': 20, 'lowest_bid': 7.5, 'bids': {
        5: {'user_id': 5, 'amount': 12.5, 'timestamp': 13},
        8: {'user_id': 8, 'amount': 20, 'timestamp': 17}
    }}
    assert database.get('tv_1') == {'close_time': 20, 'item': 'tv_1', 'reserve_price': 250.0, 'timestamp': 15,
                                    'user_id': 8, 'bid_count': 0, 'bids': {}, 'highest_bid': 0, 'lowest_bid': math.inf}
    with open('src/test/test_output.txt', 'r') as text_file:
        contents = text_file.read()
        assert contents == '20|toaster_1|8|SOLD|12.50|3|20.00|7.50\n20|tv_1||UNSOLD|0.00|0|0.00|0.00\n'
