import pytest 
import datetime
import json
import dataclasses
import queue
from enum import Enum


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
    


class STATUS(str, Enum):
    SKIP = 'skip'
    PASSED = 'passed'
    FAIL = 'fail'
    ERROR = 'error'


@dataclasses.dataclass
class TestLiteTestReport:
    nodeid: str
    testcase_uuid: str = None
    status: str = None
    startime_timestamp: float = None
    stoptime_timestamp: float = None
    duration: float = None
    report: str = None
    log: str = None
    skipreason: str = None
    precondition_status: str = None
    postcondition_status: str = None
    step_number_with_error: int = None

    @property    
    def startime_readable(self):
        return datetime.datetime.fromtimestamp(self.startime_timestamp)
    @property
    def stoptime_readable(self):
        return datetime.datetime.fromtimestamp(self.stoptime_timestamp)

    def add_standart_data(self, report: pytest.TestReport):
        self.startime_timestamp = report.start
        self.stoptime_timestamp = report.stop
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
    queue = queue.Queue()

    def __init__(self):
        print('TestLiteTestReports INISIALIZING!!!!!!!!!!!!!!')
        

    # @classmethod    
    # def get_test_report(cls, nodeid: str):
    #     test_report = cls.TestReports.get(nodeid)
    #     if test_report is None:
    #         return TestLiteTestReport(nodeid)
    #     return test_report
    
    # @classmethod
    # def save_test_report(cls, TestReport: TestLiteTestReport):
    #     cls.TestReports.update({
    #         TestReport.nodeid: TestReport
    #     })

    @classmethod    
    def get_test_report(cls, nodeid: str):
        test_report = cls.TestReports.get(nodeid)
        if test_report is None:
            return TestLiteTestReport(nodeid)
        return test_report
    
    @classmethod
    def save_test_report(cls, TestReport: TestLiteTestReport):
        data = []
        # while TestReport != cls.queue.get():
        #     TestReport
        while cls.queue.empty():
            data.append(cls.queue.get())
        print(f'DATA: {data}')
        cls.TestReports.update({
            TestReport.nodeid: TestReport
        })
        


class TestReportJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, TestLiteTestReport):
            item = dataclasses.asdict(o)
            item.update({
                'startime_readable': str(o.startime_readable),
                'stoptime_readable': str(o.stoptime_readable), 
            })
            return item
        return super().default(o)

        

class TestLiteFinalReport:

    @classmethod
    def get_finall_report(cls):
        return [TestLiteTestReports.TestReports[item] for item in TestLiteTestReports.TestReports]

    @classmethod
    def get_serialize_finall_report(cls):
        return TestReportJSONEncoder().encode(cls.get_finall_report())


