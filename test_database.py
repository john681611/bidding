import database

def test_add_item_to_db():
    txt = 'join the darkside'
    database.add('key', txt)
    assert database.get('key') == txt

def test_update_item_in_db():
    txt = 'NOOOOOOOOO? *sobs*'
    database.add('key2', 'Luke I am your Father')
    database.add('key2', txt)
    assert database.get('key2') == txt

def test_record_not_found():
    assert database.get('key3') == None