import app
import database
import pytest

@pytest.fixture(autouse=True)
def run_around_tests():
    database.clear()

    yield
def test_E2E():
    with open('src/test/E2E_output.txt', 'w+') as text_file:
        text_file.write('')
    app.run('src/test/E2E_input.txt', 'src/test/E2E_output.txt')
    with open('src/test/E2E_output.txt', 'r') as text_file:
        contents = text_file.read()
    assert contents == '20|toaster_1|8|SOLD|12.50|3|20.00|7.50\n20|tv_1||UNSOLD|0.00|2|200.00|150.00\n'