import pytest 
import inspect
import json
import random
import shutil
import os
import pickle
import datetime
import time
from logger import Logger
from lite import TestLiteTestReports as TRs
from lite import TestLiteTestReport as TR
from lite import TestLiteFixtureReport
from lite import TestLiteFixtureReports
from lite import STATUS, TestLite_testcase_key, get_step_number_with_error, TestReportJSONEncoder, TestLiteFinalReport ,TestLiteReportManager

log = Logger(__name__).get_logger()


TestLiteFixtureReports = TestLiteFixtureReports()


def pytest_configure(config):
    config.TSTestReports = TRs()



def pytest_addoption(parser: pytest.Parser):
    parser.addoption('--runtest_show', action="store", default='False')
    parser.addoption('--testsuite', action='store')
    parser.addoption('--save_json', action='store', default=None)



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report: pytest.TestReport = outcome.get_result()
    test_report: TR = item.config.TSTestReports.get_test_report(report.nodeid)
    test_report.testcase_key = TestLite_testcase_key(item)


    if report.when == 'setup':
        test_report.params = item.callspec.params if hasattr(item, 'callspec') else None
        if report.skipped == True:
            test_report.status = STATUS.SKIP
            test_report.skipreason = report.longrepr[2]

            test_report.startime_timestamp = report.start
            test_report.stoptime_timestamp = report.stop

            # test_report.add_standart_data(report)
            # test_report.startime_timestamp = report.start
            # test_report.stoptime_timestamp = report.stop
            # test_report.duration = report.duration
            # TRs().save_test_report(test_report)

        if report.failed == True:
            test_report.precondition_status = STATUS.ERROR
            test_report.status = STATUS.ERROR
            test_report.report = report.longreprtext

            test_report.startime_timestamp = report.start
            test_report.stoptime_timestamp = report.stop

            # test_report.add_standart_data(report)
            # test_report.startime_timestamp = report.start
            # test_report.stoptime_timestamp = report.stop
            # test_report.duration = report.duration
            # test_report.report = report.longreprtext
            # test_report.log = report.caplog
            # test_report.add_log(report.caplog)
            # TRs().save_test_report(test_report)

        if report.passed == True:
            test_report.precondition_status = STATUS.PASSED

            test_report.startime_timestamp = report.start

            # test_report.add_standart_data(report)
            # test_report.startime_timestamp = report.start
            # # test_report.stoptime_timestamp = report.stop
            # # test_report.duration = report.duration
            # test_report.report = report.longreprtext
            # test_report.log = report.caplog
            # test_report.add_log(report.caplog)
            # TRs().save_test_report(test_report)

    if test_report.status != STATUS.SKIP and report.when == 'call':
        if report.passed == True:
            test_report.status = STATUS.PASSED

            # test_report.add_standart_data(report)
            # test_report.report = report.longreprtext
            # test_report.log = report.caplog
            # TRs().save_test_report(test_report)

        if report.failed == True:
            test_report.step_number_with_error = get_step_number_with_error(report.longreprtext)
            test_report.status = STATUS.FAIL
            test_report.report = report.longreprtext
            # test_report.log = report.caplog
            # test_report.add_standart_data(report)
            # TRs().save_test_report(test_report)
            

    if test_report.status != STATUS.SKIP and report.when == 'teardown':
        if report.failed == True:
            print('TEARDOWN is FAILED')
            test_report.postcondition_status = STATUS.ERROR
            test_report.report = report.longreprtext
        if report.passed == True:
            print('TEARDOWN is PASSED')
            test_report.postcondition_status = STATUS.PASSED

        # test_report.report = report.longreprtext
        test_report.log = report.caplog
        test_report.stoptime_timestamp = report.stop
        # test_report.add_standart_data(report)



    item.config.TSTestReports.save_test_report(test_report)  

    if item.config.getoption('--runtest_show') == 'True':
        print('>--------------------------pytest_runtest_makereport-------------------------------<')
        
        if report.when == 'setup':
            print('>=========================SETUP=============================<')
            print('\n')
            print('...............ITEM................')
            print(item)
            print('---------------------------------------')
            print(item.__dict__)
            print('---------------------------------------')
            print(item.funcargs)
            print('...............ITEM................\n')
            print('...............OUTCOME................')
            print(outcome)
            print('...............OUTCOME................\n')
            print('...............CALL................')
            print(call)
            print('...............CALL................\n')
            print('\n')
            print(report.__dict__)
            print(f'nodeid: {report.nodeid}')
            print(f'location: {report.location}')
            print(f'keywords: {report.keywords}')
            print(f'outcome: {report.outcome}')
            print(f'longrepr: {report.longrepr}')
            print(f'user_properties: {report.user_properties}')
            print(f'sections: {report.sections}')
            print(f'duration: {report.duration}')
            print(f'start: {report.start}')
            print(f'stop: {report.stop}')
            print(f'caplog: {report.caplog}')
            print(f'capstderr: {report.capstderr}')
            print(f'capstdout: {report.capstdout}')
            print(f'count_towards_summary: {report.count_towards_summary}')
            print(f'failed: {report.failed}')
            print(f'fspath: {report.fspath}')
            print(f'head_line: {report.head_line}')
            print(f'longreprtext: {report.longreprtext}')
            print(f'passed: {report.passed}')
            print(f'skipped: {report.skipped}')
            print('>=========================SETUP=============================<')
        if report.when == 'call':
            print('>=========================CALL=============================<')
            print('\n')
            print('...............ITEM................')
            print(item)
            print('---------------------------------------')
            print(item.__dict__)
            # print(f'CALLSPEC: {item.callspec.params}')
            print('---------------------------------------')
            print(item.funcargs)
            print('...............ITEM................\n')
            print('...............OUTCOME................')
            print(outcome)
            print('...............OUTCOME................\n')
            print('...............CALL................')
            print(call)
            print('...............CALL................\n')
            print('\n')
            print(report.__dict__)
            print(f'nodeid: {report.nodeid}')
            print(f'location: {report.location}')
            print(f'keywords: {report.keywords}')
            print(f'outcome: {report.outcome}')
            print(f'longrepr: {report.longrepr}')
            print(f'user_properties: {report.user_properties}')
            print(f'sections: {report.sections}')
            print(f'duration: {report.duration}')
            print(f'start: {report.start}')
            print(f'stop: {report.stop}')
            print(f'caplog: {report.caplog}')
            print(f'capstderr: {report.capstderr}')
            print(f'capstdout: {report.capstdout}')
            print(f'count_towards_summary: {report.count_towards_summary}')
            print(f'failed: {report.failed}')
            print(f'fspath: {report.fspath}')
            print(f'head_line: {report.head_line}')
            print(f'longreprtext: {report.longreprtext}')
            print(f'passed: {report.passed}')
            print(f'skipped: {report.skipped}')
            print('>=========================CALL=============================<')
        if report.when == 'teardown':
            print('>=========================TEARDOWN=============================<')
            print('\n')
            print('...............ITEM................')
            print(item)
            print('---------------------------------------')
            print(item.__dict__)
            print('---------------------------------------')
            print(item.funcargs)
            print('...............ITEM................\n')
            print('...............OUTCOME................')
            print(outcome)
            print('...............OUTCOME................\n')
            print('...............CALL................')
            print(call)
            print('...............CALL................\n')
            print('\n')
            print(report.__dict__)
            print(f'nodeid: {report.nodeid}')
            print(f'location: {report.location}')
            print(f'keywords: {report.keywords}')
            print(f'outcome: {report.outcome}')
            print(f'longrepr: {report.longrepr}')
            print(f'user_properties: {report.user_properties}')
            print(f'sections: {report.sections}')
            print(f'duration: {report.duration}')
            print(f'start: {report.start}')
            print(f'stop: {report.stop}')
            print(f'caplog: {report.caplog}')
            print(f'capstderr: {report.capstderr}')
            print(f'capstdout: {report.capstdout}')
            print(f'count_towards_summary: {report.count_towards_summary}')
            print(f'failed: {report.failed}')
            print(f'fspath: {report.fspath}')
            print(f'head_line: {report.head_line}')
            print(f'longreprtext: {report.longreprtext}')
            print(f'passed: {report.passed}')
            print(f'skipped: {report.skipped}')
            print('>=========================TEARDOWN=============================<')


class fixture_after_save:

    def __init__(self, fixture_function, id, nodeid):
        print('FIXTURE AFTER SAVE')
        self.fixture_function = fixture_function
        self.id = id
        self.nodeid = nodeid
        self.fixture_report = TestLiteFixtureReports.get_fixture_report(id, nodeid)

    def __call__(self, *args, **kwargs):
        print('FIXTURE AFTER SAVE ---- CALL')
        print(f'FUNCTION: {self.fixture_function.__dict__}')
        with self:
            return self.fixture_function(*args, **kwargs)

    def __enter__(self):
        print('TESTLITE: enter START')
        self.fixture_report.after_start_time = round(time.time(), 2)
        TestLiteFixtureReports.save_fixture_report(self.id, self.fixture_report)
        print('TESTLITE: enter END')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('TESTLITE: exit START')
        print(exc_type)
        print(exc_val)
        print(exc_tb)
        self.fixture_report.after_stop_time = round(time.time(), 2)
        self.fixture_report.after_status = exc_val
        TestLiteFixtureReports.save_fixture_report(self.id, self.fixture_report)
        print('TESTLITE: exit END')


@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if fixturedef.baseid != '':
        print('\n↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓pytest_fixture_setup↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓')
        # print(fixturedef.__dict__)
        # print(fixturedef.baseid)
        # for key, value in request.__dict__.items():
        #     print(f'[{key}: {value}]')
        
        test_function_name = str(request._pyfuncitem).split(' ')[1][:-1]
        id = f'{test_function_name}::{request.fixturename}'
        nodeid = f'{fixturedef.baseid}::{test_function_name}'
        print(f'ID: {id}')
        print(f'NODEID: {nodeid}')
        fixture_report = TestLiteFixtureReports.get_fixture_report(id, nodeid)
        # fixture_report.start_time = datetime.datetime.now()
        fixture_report.before_start_time = round(time.time(), 2)
        TestLiteFixtureReports.save_fixture_report(id, fixture_report)
        outcome = yield
        print(f'OUTCOME: {outcome._result}')
        # fixture_report.stop_time = datetime.datetime.now()s
        print('AFTER YIELD')
        finalizers = getattr(fixturedef, '_finalizers', [])
        for index, finalizer in enumerate(finalizers):
            # finalizer_name = getattr(finalizer, "__name__", index)
            # name = f'{request.fixturename}::{finalizer_name}'
            finalizers[index] = fixture_after_save(finalizer, id, nodeid)
            
        # finalizers = getattr(fixturedef, '_finalizers', [])
        fixture_report.before_stop_time = round(time.time(), 2)
        TestLiteFixtureReports.save_fixture_report(id, fixture_report)
    else:
        yield
        print('↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑pytest_fixture_setup↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑\n')


def pytest_fixture_post_finalizer(fixturedef, request):
    if fixturedef.baseid != '':
        print('\n↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓pytest_fixture_post_finalize↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓')
        
        # print(fixturedef.__dict__)
        # print(fixturedef.cached_result)
        # print(fixturedef._finalizers)
        # # print(type(request.__dict__))
        # for key, value in request.__dict__.items():
        #     print(f'[{key}: {value}]')
        # print(f'\n{request._pyfuncitem.originalname}')
        # print(f'\n{request._pyfuncitem}')
        # print('\n')
        # print(request._pyfuncitem.__dict__)
        # print(request._parent_request)
        # print(request._fixturedef)
        
        test_function_name = str(request._pyfuncitem).split(' ')[1][:-1]
        id = f'{test_function_name}::{request.fixturename}'
        nodeid = f'{fixturedef.baseid}::{test_function_name}'
        print(f'ID: {id}')
        print(f'NODEID: {nodeid}')
        fixture_report = TestLiteFixtureReports.get_fixture_report(id, nodeid)
        fixture_report.name = request.fixturename
        fixture_report.cached_result = fixturedef.cached_result
        TestLiteFixtureReports.save_fixture_report(id, fixture_report)

        print('↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑pytest_fixture_post_finalizer↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑\n')



def pytest_sessionfinish(session: pytest.Session, exitstatus):
    if hasattr(session.config, "workerinput"):
        TestLiteReportManager().save_report()
    else:
        TestLiteReportManager().save_report()
        final_report = TestLiteReportManager().get_reports()
        if session.config.getoption('--save_json') is not None:
            final_report.save_json_file(session.config.getoption("--save_json"))
        if session.config.getoption('--testsuite'):
            final_report.send_json_in_TestLite(testsuite=session.config.getoption('--testsuite'))

    print('---------------------------------SESSION_FINISH ENDING-------------------------------------')
    for key, value in TestLiteFixtureReports.FixtureReports.items():
        print(f'{key} : {value}\n')
        print(value.before_duration)
        print(value.after_duration)
        print('\n')
        print(value.before_status)
        print(value.after_status)
        # print(value.stop_time)