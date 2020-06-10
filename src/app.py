import copy
import database
import write_file
import parse_file
import winning_bid


def process_sell(sell):
    database.add(sell['item'], sell)


def proccess_bid(bid):
    item = database.get(bid['item'])
    if (item is None or
            item['timestamp'] > bid['timestamp'] or
            item['close_time'] < bid['timestamp'] or
            bid['user_id'] in item['bids'] and
            item['bids'][bid['user_id']]['amount'] > bid['bid_amount']):
        return None

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
    database.add(item['item'], item)
    return bid_details


def process_commands(commands, output):
    for command in commands:
        if 'bid_amount' in command:
            proccess_bid(command)
        elif 'close_time' in command:
            process_sell(command)
        else:
            closed = database.get_closed(command['timestamp'])
            for sale in closed:

                winner = winning_bid.determin_winner(sale)
                write_file.write(
                    write_file.format_data(
                        copy.deepcopy(winner)), output)


def run(input_file, output):
    commands = list(map(parse_file.parse_message,
                        parse_file.read_file(input_file)))
    process_commands(commands, output)
