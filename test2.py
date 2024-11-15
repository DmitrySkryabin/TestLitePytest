import pytest
import lite
from logger import Logger

log = Logger(__name__).get_logger()


class Test1:


    @lite.test_key('CRM-TC-1')
    def test_first(self):
        #TestLiteStep
        log.info('first step')
        #TestLiteStep
        log.info('second step')
        a = 4/0
        #TestLiteStep
        log.info('third step')
        #TestLiteStep
        log.info('fourth step')


    @lite.test_key('CRM-TC-2')
    def test_second(self):
        #TestLiteStep
        log.info('first step')
        #TestLiteStep
        log.info('second step')


    @lite.test_key('CRM-TC-4')
    def test_third(self):
        #TestLiteStep
        log.info('first step')
