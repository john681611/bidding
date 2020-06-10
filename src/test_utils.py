import utils


def test_get_winning_bid():
    bids = {
        8: {'user_id': 8, 'amount': 7.5, 'timestamp': 12},
        5: {'user_id': 5, 'amount': 12.5, 'timestamp': 13}
    }
    assert utils.get_winning_bid(
        bids) == {'user_id': 5, 'amount': 12.5, 'timestamp': 13, 'price_paid': 7.5}


def test_get_winning_bid_same_ammount():
    bids = {
        8: {'user_id': 8, 'amount': 12.5, 'timestamp': 12},
        5: {'user_id': 5, 'amount': 12.5, 'timestamp': 13}
    }
    assert utils.get_winning_bid(
        bids) == {'user_id': 5, 'amount': 12.5, 'price_paid': 12.5, 'timestamp': 13}


def test_get_winning_bid_single_bid():
    bids = {
        5: {'user_id': 5, 'amount': 12.5, 'timestamp': 13}
    }
    assert utils.get_winning_bid(
        bids) == {'user_id': 5, 'amount': 12.5, 'price_paid': 12.5, 'timestamp': 13}


def test_get_highest_bid():
    bids = {
        8: {'user_id': 8, 'amount': 7.5, 'timestamp': 12},
        5: {'user_id': 5, 'amount': 12.5, 'timestamp': 13}
    }

    assert utils.get_highest_bid(bids) == 12.5
