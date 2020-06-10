import write_file


def test_format_data():
    data = {
        'close_time': 20,
        'item': 'toaster_1',
        'user_id': 8,
        'status': 'SOLD',
        'price_paid': 12.5,
        'total_bid_count': 3,
        'highest_bid': 20,
        'lowest_bid': 7.5
    }
    assert write_file.format_data(
        data) == '20|toaster_1|8|SOLD|12.50|3|20.00|7.50\n'
