import pytest 
import time
import lite
from logger import Logger

log = Logger(__name__).get_logger()

class Test1:

    @pytest.mark.skip('А чо на')
    @lite.test_key('CRM-TC-1')
    def test_1(self):
        #TestLiteStep
        log.info('start test_1')
        #TestLiteStep
        time.sleep(3)
        #TestLiteStep
        log.info('end test_1')
        #TestLiteStep
        log.info('last step')


    @lite.test_key('CRM-TC-2')
    def test_2(self):
        #TestLiteStep
        log.info('start test_2')
        #TestLiteStep
        time.sleep(3)
        #TestLiteStep
        a = 5/0
        log.info('end test_2')

    
    @lite.test_key('CRM-TC-3')
    def test_3(self):
        #TestLiteStep
        log.info('start test_3')
        #TestLiteStep
        time.sleep(3)
        #TestLiteStep
        log.info('end test_3')


    @pytest.fixture
    def fixture_pass(self):
        return 10 / 2


    @lite.test_key('CRM-TC-4')
    def test_4(self, fixture_pass):
        #TestLiteStep
        log.info('start test_4')
        #TestLiteStep
        time.sleep(3)
        #TestLiteStep
        log.info('end test_4')


    @pytest.fixture
    def fixture_error(self):
        return 10 / 0


    @lite.test_key('CRM-TC-5')
    def test_5(self, fixture_error):
        #TestLiteStep
        log.info('start test_5')
        #TestLiteStep
        time.sleep(3)
        #TestLiteStep
        log.info('end test_5')