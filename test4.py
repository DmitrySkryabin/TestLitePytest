import lite
import pytest
import time


def get_data():
    return [
        {
            'data1': 'value1',
            'data2': 'value2'
        },
        {
            'data3': 'value3',
            'data4': 'value4'
        },
        {
            'data5': 'value5',
            'data6': 'value6'
        }
    ]


class Test1:

    @pytest.fixture    
    def fixture_1(self):
        time.sleep(1)
        print('Start fixture_1')
        return 'fixture1'
    
    @pytest.fixture
    def fixture_2(self):
        print('Start fixture_2')
        # time.sleep(1)
        yield 'fixture2'
        # time.sleep(1)
        print('End fixture_2')
        a = 5/ 0

    @pytest.fixture
    def fixture_3(self):
        print('Start fixture_3')
        # time.sleep(1)
        yield 'fixture3'
        # time.sleep(2)
        print('End fixture_3')

    @pytest.fixture
    def fixture_error(self):
        print('Start fixture_error')
        return 1 / 0

    # @lite.test_key('CRM-1')
    # def test_1(self, fixture_1, fixture_2, fixture_error):
    #     print(True)

    @pytest.mark.parametrize('data', get_data())
    @lite.test_key('CRM-2')
    def test_2(self, fixture_1, fixture_2, data):
        print(True)
    
    # @pytest.mark.skip('BECOSE EBAT TEBYA NE DOLJNO')
    @pytest.mark.parametrize('data', ['param1', 'param2'])
    @lite.test_key('CRM-3')
    def test_3(self, fixture_1, data):
        print(True)