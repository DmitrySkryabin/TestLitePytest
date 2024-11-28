import pytest 
import datetime
import json
import dataclasses
import queue
import random
import pickle
import os
import shutil
import threading
import requests
from enum import Enum
from logger import Logger

log = Logger(__name__).get_logger()


class CONFIG:
    REPORTSDIRNAME = 'TestLiteReports'
    DELETEREPORTSDIR = True
    REPORTSSAVETYPE = 'BINARY'
    TESTLITEURL = 'http://127.0.0.1:8000'



def test_key(TestLite_id):

    def decorator(func):
        if getattr(func, '__pytest_wrapped__', None):
            function = func.__pytest_wrapped__.obj
        else:
            function = func
        function.__TestLite_testcase_key__ = TestLite_id
        return func
    
    return decorator


def TestLite_testcase_key(item):
    return getattr(
        getattr(item, "obj", None),
        "__TestLite_testcase_key__",
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
    testcase_key: str = None
    status: str = None
    startime_timestamp: float = None
    stoptime_timestamp: float = None
    # duration: float = None
    report: str = None
    log: str = None
    skipreason: str = None
    precondition_status: str = None
    postcondition_status: str = None
    step_number_with_error: int = None


    @property
    def duration(self):
        if self.stoptime_timestamp is not None:
            return round(self.stoptime_timestamp - self.startime_timestamp, 2)
            # return f'{(self.stoptime_timestamp - self.startime_timestamp):.2f}'
        else:
            return None


    @property    
    def startime_readable(self):
        if self.startime_timestamp is not None:
            return datetime.datetime.fromtimestamp(self.startime_timestamp)
        else:
            return None
        
    @property
    def stoptime_readable(self):
        if self.stoptime_timestamp is not None:
            return datetime.datetime.fromtimestamp(self.stoptime_timestamp)
        else:
            return None
    
    def add_log(self, log):
        self.log = self.log + log

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
    # Ебани сюда пикл и проверь, а потом еще добавь хуету чтобы вконце все потоки соединили свою хуету в одну хуету
    __metaclass__ = TestLiteTestReportsMetaClass

    # TestReports:list[TestLiteTestReport] = []
    TestReports:dict[str, TestLiteTestReport] = {}
    save_pickle_file = 'TestLiteTemp'
    TestReportsQueue = queue.Queue()
    counter = 1
    thread_list = []

    @property
    def thr_context(self) -> dict[str, TestLiteTestReport]|dict[None]:
        if self._thr == threading.current_thread():
            return self.TestReports
        else:
            return {}

    def __init__(self):
        self._thr = threading.current_thread()
        log.info(f'_thr: {self._thr}')
        

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
        


class TestReportJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, TestLiteTestReport):
            item = dataclasses.asdict(o)
            item.update({
                'startime_readable': str(o.startime_readable),
                'stoptime_readable': str(o.stoptime_readable), 
                'duration': float(o.duration)
            })
            return item
        return super().default(o)


class TestLiteFinalReport:

    def __init__(self, report):
        self.report = report
        self.json_report = None

    def __call__(self) -> list[TestLiteTestReport]:
        return self.report
    
    def __repr__(self):
        return str(self.report)
    
    def __iter__(self):
        yield self.report

    @property
    def json(self):
        if self.json_report is None:
            self.json_report = TestReportJSONEncoder().encode(self.report)
        return self.json_report
    
    def save_json_file(self, file_name):
        with open(file_name, 'w') as file:
            file.write(self.json)

    def send_json_in_TestLite(self, testsuite):
        response = requests.post(
            url=f'{CONFIG.TESTLITEURL}/api/v1/project/{testsuite.split("-")[0]}/testsuite/{testsuite}/save',
            data=self.json,
            headers={
                'Content-Type': 'application/json'
            }
        )
      

class TestLiteReportManager:

    def __init__(self):
        self.reports = TestLiteTestReports().thr_context
        if not os.path.exists(CONFIG.REPORTSDIRNAME):
            os.mkdir(CONFIG.REPORTSDIRNAME)


    def save_report(self):
        log.info('SAVING REPORT')
        match CONFIG.REPORTSSAVETYPE.upper():
            case 'TXT':
                self._save_report_as_txt_file()
            case 'BINARY':
                self._save_report_as_binary_file()


    def get_reports(self) -> TestLiteFinalReport:
        report = None
        match CONFIG.REPORTSSAVETYPE.upper():
            case 'TXT':
                report = self._read_reports_from_txt_files()
            case 'BINARY':
                report = self._read_reports_from_binary_files()
        
        if CONFIG.DELETEREPORTSDIR:
            shutil.rmtree(CONFIG.REPORTSDIRNAME)

        return TestLiteFinalReport(report)


    def _save_report_as_txt_file(self):
        with open(f'{CONFIG.REPORTSDIRNAME}/{str(threading.current_thread()).replace('<','').replace('>','')}.txt', 'w') as file:
            file.write(str(self.reports))

    
    def _save_report_as_binary_file(self):
        with open(f'{CONFIG.REPORTSDIRNAME}/{str(threading.current_thread()).replace('<','').replace('>','')}.data', 'wb') as file:
            file.write(pickle.dumps(self.reports))
    

    def _read_reports_from_binary_files(self):
        final_report = []
        listdir = os.listdir(CONFIG.REPORTSDIRNAME)
        for report_file_name in listdir:
            with open(f'{CONFIG.REPORTSDIRNAME}/{report_file_name}', 'rb') as file:
                final_report += [value for key, value in pickle.load(file).items()]
        return final_report
    
    
    def _read_reports_from_txt_files(self):
        final_report = []
        listdir = os.listdir(CONFIG.REPORTSDIRNAME)
        for report_file_name in listdir:
            with open(f'{CONFIG.REPORTSDIRNAME}/{report_file_name}', 'rb') as file:
                final_report += [value for key, value in dict(file.read()).items()]
        return final_report
  




