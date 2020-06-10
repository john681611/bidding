import winning_bid


def test_get_winning_bid():
    bids = {
        8: {'user_id': 8, 'amount': 7.5, 'timestamp': 12},
        5: {'user_id': 5, 'amount': 12.5, 'timestamp': 13}
    }
    assert winning_bid.get_winning_bid(
        bids) == {'user_id': 5, 'amount': 12.5, 'timestamp': 13, 'price_paid': 7.5}


def test_get_winning_bid_same_ammount():
    bids = {
        8: {'user_id': 8, 'amount': 12.5, 'timestamp': 12},
        5: {'user_id': 5, 'amount': 12.5, 'timestamp': 13}
    }
    assert winning_bid.get_winning_bid(
        bids) == {'user_id': 5, 'amount': 12.5, 'price_paid': 12.5, 'timestamp': 13}


def test_get_winning_bid_single_bid():
    bids = {
        5: {'user_id': 5, 'amount': 12.5, 'timestamp': 13}
    }
    assert winning_bid.get_winning_bid(
        bids) == {'user_id': 5, 'amount': 12.5, 'price_paid': 12.5, 'timestamp': 13}


def test_get_highest_bid():
    bids = {
        8: {'user_id': 8, 'amount': 7.5, 'timestamp': 12},
        5: {'user_id': 5, 'amount': 12.5, 'timestamp': 13}
    }

    assert winning_bid.get_highest_bid(bids) == 12.5


def test_determin_winner_unsold_no_bids():
    sale = {'close_time': 20, 'item': 'toaster_5', 'reserve_price': 10.0,
            'timestamp': 10, 'user_id': 1, 'bids': {}, 'bid_count': 0, }
    assert winning_bid.determin_winner(sale) == {
        'close_time': sale['close_time'],
        'item': sale['item'],
        'user_id': '',
        'status': 'UNSOLD',
        'price_paid': 0,
        'total_bid_count': 0,
        'highest_bid': 0,
        'lowest_bid': 0
    }


def test_determin_winner_unsold_one_bid():
    sale = {'close_time': 20, 'item': 'toaster_5', 'reserve_price': 10.0, 'timestamp': 10, 'user_id': 1, 'bid_count': 1, 'highest_bid': 5, 'lowest_bid': 5, 'bids': {
        9: {'user_id': 9, 'amount': 5, 'timestamp': 13}
    }}
    assert winning_bid.determin_winner(sale) == {
        'close_time': sale['close_time'],
        'item': sale['item'],
        'user_id': '',
        'status': 'UNSOLD',
        'price_paid': 0,
        'total_bid_count': 1,
        'highest_bid': 5,
        'lowest_bid': 5
    }


def test_determin_winner_one_bid():
    sale = {'close_time': 20, 'item': 'toaster_5', 'reserve_price': 10.0, 'timestamp': 10, 'user_id': 1, 'highest_bid': 11, 'lowest_bid': 11, 'bid_count': 1, 'bids': {
        9: {'user_id': 9, 'amount': 11, 'timestamp': 13}
    }}
    assert winning_bid.determin_winner(sale) == {
        'close_time': sale['close_time'],
        'item': sale['item'],
        'user_id': 9,
        'status': 'SOLD',
        'price_paid': 10,
        'total_bid_count': 1,
        'highest_bid': 11,
        'lowest_bid': 11
    }


def test_determin_winner_two_bids():
    sale = {'close_time': 20, 'item': 'toaster_1', 'reserve_price': 10.0, 'timestamp': 10, 'user_id': 1, 'bid_count': 2, 'highest_bid': 12.5, 'lowest_bid': 11, 'bids': {
        8: {'user_id': 8, 'amount': 11, 'timestamp': 12},
        5: {'user_id': 5, 'amount': 12.5, 'timestamp': 13}
    }}
    assert winning_bid.determin_winner(sale) == {
        'close_time': sale['close_time'],
        'item': sale['item'],
        'user_id': 5,
        'status': 'SOLD',
        'price_paid': 11,
        'total_bid_count': 2,
        'highest_bid': 12.5,
        'lowest_bid': 11
    }
