import pytest 
import inspect
import json
import random
import shutil
import os
import pickle
from logger import Logger
from lite import TestLiteTestReports as TRs
from lite import TestLiteTestReport as TR
from lite import STATUS, TestLite_testcase_key, get_step_number_with_error, TestReportJSONEncoder, TestLiteFinalReport ,TestLiteReportManager

log = Logger(__name__).get_logger()



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