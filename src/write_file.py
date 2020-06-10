
def write(data, location):
    with open(location, 'a+') as text_file:
        text_file.write(data)


def format_data(data):
    return f"{data['close_time']}|{data['item']}|{data['user_id']}|{data['status']}|{data['price_paid']:.2f}|{data['total_bid_count']}|{data['highest_bid']:.2f}|{data['lowest_bid']:.2f}\n"
