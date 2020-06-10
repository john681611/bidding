import parse_file
import pytest


#Reading
def test_read_file_line_by_line():
    assert parse_file.read_file('input.txt') == [
        '10|1|SELL|toaster_1|10.00|20',
        '12|8|BID|toaster_1|7.50',
        '13|5|BID|toaster_1|12.50',
        '15|8|SELL|tv_1|250.00|20',
        '16',
        '17|8|BID|toaster_1|20.00',
        '18|1|BID|tv_1|150.00',
        '19|3|BID|tv_1|200.00',
        '20',
        '21|3|BID|tv_1|300.00']

def test_read_file_no_file():
    file_name = 'none.txt'
    with pytest.raises(FileNotFoundError) as excinfo:
        parse_file.read_file(file_name)
    assert file_name in str(excinfo.value)


# Parsing
def test_parse_sell():
    sell = '10|1|SELL|toaster_1|10.00|20'
    assert parse_file.parse_message(sell) == {
        'timestamp': 10,
        'user_id': 1,
        'item': 'toaster_1',
        'reserve_price': 10.00,
        'close_time': 20
    }

def test_parse_bid():
    bid = '12|8|BID|toaster_1|7.50'
    assert parse_file.parse_message(bid) == {
        'timestamp': 12,
        'user_id': 8,
        'item': 'toaster_1',
        'bid_amount': 7.50,
    }

def test_ignore_heart_beat():
    heart_beat = '20'
    assert parse_file.parse_message(heart_beat) == None


# parse everything
def test_parse_file():
    assert parse_file.parse_file('input.txt') == [
        {'close_time': 20,'item': 'toaster_1','reserve_price': 10.0,'timestamp': 10, 'user_id': 1},
        {'bid_amount': 7.5, 'item': 'toaster_1', 'timestamp': 12, 'user_id': 8},
        {'bid_amount': 12.5, 'item': 'toaster_1', 'timestamp': 13, 'user_id': 5},
        {'close_time': 20,'item': 'tv_1','reserve_price': 250.0,'timestamp': 15,'user_id': 8},
        {'bid_amount': 20.0, 'item': 'toaster_1', 'timestamp': 17, 'user_id': 8},
        {'bid_amount': 150.0, 'item': 'toaster_1', 'timestamp': 18, 'user_id': 1},
        {'bid_amount': 200.0, 'item': 'toaster_1', 'timestamp': 19, 'user_id': 3},
        {'bid_amount': 300.0, 'item': 'toaster_1', 'timestamp': 21, 'user_id': 3}
        ]
