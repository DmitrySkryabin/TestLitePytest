import pytest 
from enum import Enum
from dataclasses import dataclass

def id(TestLite_id):

    def decorator(func):
        if getattr(func, '__pytest_wrapped__', None):
            function = func.__pytest_wrapped__.obj
        else:
            function = func
        function.__TestLite_id__ = TestLite_id
        return func
    
    return decorator


def TestLite_id(item):
    return getattr(
        getattr(item, "obj", None),
        "__TestLite_id__",
        None
    )


def get_step_number_with_error(longreprtext: str) -> int|None:
    print('<<<<<<<<<<<<<<<<<<<<<<<get_error_line_number>>>>>>>>>>>>>>>>>>>>>>>')
    step_number = 0
    for i, line in enumerate(longreprtext.split('\n')):
        print(f'{i}: {line}')
        if '#TestLiteStep' in line:
            step_number += 1
    print(f'STEP NUMBER: {step_number} {type(step_number)}')
    print('>>>>>>>>>>>>>>>>>>>>>>>get_error_line_number<<<<<<<<<<<<<<<<<<<<<<<')
    return step_number if step_number !=0 else None
    


class STATUS(Enum):
    SKIP = 'skip'
    PASSED = 'passed'
    FAIL = 'fail'
    ERROR = 'error'


@dataclass
class TestLiteTestReport:
    nodeid: str
    testcase_uuid: str = None
    status: str = None
    startime: str = None
    stoptime: str = None
    duration: str = None
    report: str = None
    log: str = None
    skipreason: str = None
    precondition_status: str = None
    postcondition_status: str = None
    step_number_with_error: int = None

    def add_standart_data(self, report: pytest.TestReport):
        self.startime = report.start
        self.stoptime = report.stop
        self.duration = report.duration
        self.log = report.caplog



class TestLiteTestReportsMetaClass(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
 

class TestLiteTestReports:
    __metaclass__ = TestLiteTestReportsMetaClass

    # TestReports:list[TestLiteTestReport] = []
    TestReports:dict[str, TestLiteTestReport] = {}

    @classmethod    
    def get_test_report(cls, nodeid: str):
        test_report = cls.TestReports.get(nodeid)
        if test_report is None:
            return TestLiteTestReport(nodeid)
        return test_report
    
    @classmethod
    def save_test_report(cls, TestReport: TestLiteTestReport):
        cls.TestReports.update({
            TestReport.nodeid: TestReport
        })
        
        

class TestLiteFinalReport:

    pass


