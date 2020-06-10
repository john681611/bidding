import database
import pytest

@pytest.fixture(autouse=True)
def run_around_tests():
    database.clear()
    yield

def test_add_item_to_db():
    txt = 'join the darkside'
    database.add('key', txt)
    assert database.get('key') == txt

def test_update_item_in_db():
    txt = 'NOOOOOOOOO? *sobs*'
    database.add('key2', 'Luke I am your Father')
    database.add('key2', txt)
    assert database.get('key2') == txt

def test_local_modify_doest_affect_db():
    txt = {'txt': 'For GONDOOOOOR'}
    database.add('key3', txt)
    data = database.get('key3')
    data['txt'] = 'For ROHAAAAAN'
    assert data['txt'] != database.get('key3')['txt']


def test_record_not_found():
    assert database.get('key4') == None

def test_clear_db():
    txt = '5G burns cookies!'
    database.add('key5', txt)
    database.clear()
    assert database.get('key5') == None