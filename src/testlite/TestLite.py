import requests
from testlite._config import CONFIG


def test_key(TestLite_id: str):
    '''
    :param TestLite_id (str): TestCase key from TestLite

    Set key for TestCase to upload report in TestLite
    '''
    def decorator(func):
        if getattr(func, '__pytest_wrapped__', None):
            function = func.__pytest_wrapped__.obj
        else:
            function = func
        function.__TestLite_testcase_key__ = TestLite_id
        return func
    
    return decorator


def get_parameters_from_TestLite(testcase_key: str) -> dict:
    '''
    :param testcase_key (str): TestCase key from TestLite

    Return parameters for TestCase from TestLite
    '''
    response = requests.get(
        url=f'{CONFIG().TESTLITEURL}/api/v1/testcase/{testcase_key}/get/parameters'
    )
    return response.json()
