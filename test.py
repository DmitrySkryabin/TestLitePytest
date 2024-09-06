import pytest
import lite
import allure
from logger import Logger

log = Logger(__name__).get_logger()


@pytest.fixture
def fix1():
    log.info('its fix1 log')
    return 1

@pytest.fixture
def fix2():
    log.info('its fix2 log')
    return 2

@pytest.fixture
def fix_error():
    log.info(f'NOW WE MAKE ERROR')
    a = 5 / 0
    return a


@pytest.fixture
def fix_error_teardown():
    a = 3
    yield a
    a = a / 0


class OtherClassForTest:

    def another_func(self):
        #TestLiteStep
        self.value = 5


class Test1(OtherClassForTest):

    # @lite.id('some-id-heh')
    # def test_with_steps(self):
    #     #TestLiteStep
    #     print('step: 1')
    #     #TestLiteStep
    #     print('step: 2')
    #     a = 5 / 0
    #     #TestLiteStep
    #     print('step: 3')
    #     #TestLiteStep
    #     assert 1 == 1
    
    # @lite.id('a6666ac6-af09-4cdf-8835-5befd9c9f919')
    # def test_passed(self, fix1):
    #     '''Описание тут ону маны суруябын'''
    #     log.info('its test_passed info 1 log')
    #     print('!!!!!!PRINTING test_1!!!!!!!')
    #     log.info('its test_passed info 2 log')
    #     assert 1==fix1


    def test_from_another_class(self):
        #TestLiteStep
        print('TEST FROM ANOTHER CLASS')
        #TestLiteStep
        super().another_func()
        assert self.value == 1

    
    # def other_func(self):
    #     #TestLiteStep
    #     print('OTHER FUNC')
    #     log.info('its other_func info 1 log')
    #     #TestLiteStep
    #     return 5


    # def test_with_logic_in_other_func(self):
    #     #TestLiteStep
    #     print('TEST WITH LOGIC IN OTHER FUNC')
    #     value = self.other_func()
    #     #TestLiteStep
    #     log.info('its test_with_logic_in_other_func info 1 log')
    #     #TestLiteStep
    #     assert value == 1
    

    # @pytest.mark.skip(reason='Just testing skip reason')
    # def test_skip(self, fix2):
    #     log.info('its test_skip info log')
    #     assert 1==fix2

    # def test_fail(self, fix2):
    #     log.info('its test_fail info log')
    #     assert 1==fix2

    # def test_error_in_setup(self, fix_error):
    #     log.info('its test_error_in_setup info log')
    #     assert 1==fix_error

    # def test_error_in_test(self):
    #     log.info('its test_error_in_test info log')
    #     a = 5 / 0
    #     assert 1==fix_error

    # @lite.id('some-id')
    # def test_error_in_teardown(self, fix_error_teardown):
    #     log.info('its fix_error_teardown info log')
    #     print(fix_error_teardown)
    #     assert 3==3