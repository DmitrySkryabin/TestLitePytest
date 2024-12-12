import pytest 
import datetime
import json
import dataclasses
import queue
import re
import random
import pickle
import os
import shutil
import threading
import requests
import traceback
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
class FixtureRunResult:
    result: str = None # Что возвращает фикстура
    status: STATUS = None
    error: str = None


@dataclasses.dataclass
class TestLiteFixtureReport:
    id: str
    nodeid: str 
    name: str = None
    cached_result: tuple = None
    before_start_time: float = None
    before_stop_time: float = None
    after_start_time: float = None
    after_stop_time: float = None

    _after_error = None

    @property
    def before_duration(self):
        if self.before_stop_time is not None:
            return self.before_stop_time - self.before_start_time
        else:
            return 0 - self.before_start_time
    
    @property
    def after_duration(self):
        if self.after_stop_time is not None and self.after_start_time is not None:
            return self.after_stop_time - self.after_start_time
        else:
            return None
        
    @property
    def before_status(self):
        if self.cached_result[2] is None:
            return FixtureRunResult(
                result=self.cached_result[0],
                status=STATUS.PASSED
            )
        else:
            return FixtureRunResult(
                status=STATUS.ERROR,
                error=self.cached_result[2]
            )
    
    @property
    def after_status(self):
        return self._after_error
    
    @after_status.setter
    def after_status(self, exc_val):
        if exc_val is not None:
            self._after_error = FixtureRunResult(
                status=STATUS.ERROR,
                error=exc_val
            )
        else:
            self._after_error = FixtureRunResult(
                status=STATUS.PASSED
            )



@dataclasses.dataclass
class TestLiteTestReport:
    nodeid: str
    testcase_key: str = None
    status: str = None
    startime_timestamp: float = None
    stoptime_timestamp: float = None
    report: str = None
    log: str = None
    params: str = None
    skipreason: str = None
    precondition_status: str = None
    postcondition_status: str = None
    step_number_with_error: int = None
    
    # _fixtures: dict = None

    @property
    def parametrize_name(self):
        name = re.search('\[.*\]', self.nodeid)
        if name is None:
            return None
        else:
            return name[0]


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

    @property
    def fixtures(self):
        fixture_dict = {
            'before': [],
            'after': []
        }
        fixtures = TestLiteFixtureReports.get_all_fixtures_by_nodeid(self.nodeid)
        for fixture in fixtures:
            fixture_dict['before'].append(fixture)
            if fixture.after_duration is not None:
                fixture_dict['after'].append(fixture)

        return fixture_dict

    
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
 


class TestLiteFixtureReports:
    # Ебани сюда пикл и проверь, а потом еще добавь хуету чтобы вконце все потоки соединили свою хуету в одну хуету
    __metaclass__ = TestLiteTestReportsMetaClass

    FixtureReports:dict[str, TestLiteFixtureReport] = {}
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
    def get_all_fixtures_by_nodeid(cls, nodeid):
        return [item for item in cls.FixtureReports.values() if item.nodeid == nodeid]
        

    @classmethod    
    def get_fixture_report(cls, id: str, nodeid: str):
        '''
        id - уникальный идентификатор именно этой фикстуры для этого теста
        '''
        fixture_report = cls.FixtureReports.get(id)
        if fixture_report is None:
            return TestLiteFixtureReport(id=id, nodeid=nodeid)
        return fixture_report
    
    @classmethod
    def save_fixture_report(cls, id,  FixtureReport: TestLiteFixtureReport):
        '''
        id - уникальный идентификатор именно этой фикстуры для этого теста
        '''
        cls.FixtureReports.update({
            id: FixtureReport
        })



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
        

class MakeDict():

    def __init__(self):
        self.remake_object = None


    def _make_dict_from_FixtureRunResult(self, obj):
        if isinstance(obj, FixtureRunResult):
            item = dataclasses.asdict(obj)
            item.update({
                'error': "".join(traceback.format_exception_only(type(obj.error), obj.error)).strip() if obj.error is not None else None
            })
            return item
        else:
            raise Exception('Its not a FixtureRunResult clas')
    

    def remake(self, obj, key):
        if isinstance(obj, TestLiteFixtureReport):
            item = {}
            if key == 'before':
                item.update({
                    'name': obj.name,
                    'start_time': obj.before_start_time,
                    'stop_time': obj.before_stop_time,
                    'duration': obj.before_duration,
                    'status': self._make_dict_from_FixtureRunResult(obj.before_status)
                    # 'status': dataclasses.asdict(obj.before_status),
                    # 'result:': obj.cached_result[0]
                })
            if key == 'after':
                item.update({
                    'name': obj.name,
                    'start_time': obj.after_start_time,
                    'stop_time': obj.after_stop_time,
                    'duration': obj.after_duration,
                    'status': self._make_dict_from_FixtureRunResult(obj.after_status)
                    # 'status': dataclasses.asdict(obj.after_status)
                })
            return item
        else:
            raise Exception('Its not TestLiteFixtureReport class')

    def make_pure_dict_from_fixtures_dict(self, fixtures_dict):
        self.remake_object = fixtures_dict
        if isinstance(self.remake_object, dict):
            for key, value in self.remake_object.items():
                for i, item in enumerate(value):
                    self.remake_object[key][i] = self.remake(item, key)
            return self.remake_object
        else:
            raise Exception('Its not a dict')
        


class TestReportJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, TestLiteTestReport):
            item = dataclasses.asdict(o)
            item.update({
                'parametrize_name': str(o.parametrize_name),
                'startime_readable': str(o.startime_readable),
                'stoptime_readable': str(o.stoptime_readable), 
                'duration': float(o.duration),
                'fixtures': MakeDict().make_pure_dict_from_fixtures_dict(o.fixtures)
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
  




