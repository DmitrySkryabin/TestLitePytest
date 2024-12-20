import pytest
import requests
from testlite._reports import (
    TestLiteTestReport,
    TestLiteTestReports,
    TestLiteFixtureReport,
    TestLiteFixtureReports,
    TestLiteReportManager
)
from testlite._config import CONFIG
from testlite._helper import get_time
from testlite._reports import fixture_after_save
from testlite._models import STATUS
from testlite._Testlite import TestLite_testcase_key, get_step_number_with_error


def pytest_addoption(parser):
    group = parser.getgroup('TestLitePytest')
    group.addoption(
        '--testsuite',
        action='store',
        dest='testsuite',
        help='Set TestSuite Key. If the option is specified, then at the end we will try to send the results to TestLite'
    )
    group.addoption(
        '--savejson',
        action='store',
        dest='savejson',
        default=None,
        help='After end of testing saving JSON file with report'
    )
    group.addoption(
        '--collectfromtestlite',
        action='store_true',
        dest='collectfromtestlite',
        help='Collect tests from TestLite from the received keys'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')



def pytest_configure(config):
    config.TSTestReports = TestLiteTestReports


def pytest_collection_modifyitems(session, config, items):
    if config.getoption('collectfromtestlite'):
        try:
            # Модифицируем наши коллекции
            response = requests.get(
                url= f'{CONFIG().TESTLITEURL}/api/v1/testsuite/{config.getoption("testsuite")}/get/testcases'
            )
            if response.status_code == 200:
                collected_keys = response.json()['keys']
                print(f'\nTestLitePytest output::\ncollecting keys: {collected_keys}')
                remove_items = []
                items_copy = items.copy()
                items.clear()
                for item in items_copy:
                    if TestLite_testcase_key(item) in collected_keys:
                        items.append(item)
                    else:
                        remove_items.append(item)

                config.hook.pytest_deselected(items=remove_items)
            else:
                raise Exception('Error when testlitepytest plugin tried to collect tests from TestLite')
        except:
            raise Exception('Error when testlitepytest plugin tried to collect tests from TestLite')



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report: pytest.TestReport = outcome.get_result()
    test_report: TestLiteTestReport = item.config.TSTestReports.get_test_report(report.nodeid)
    test_report.testcase_key = TestLite_testcase_key(item)


    if report.when == 'setup':

        test_report.params = item.callspec.params if hasattr(item, 'callspec') else None

        if report.skipped == True:
            test_report.status = STATUS.SKIP
            test_report.skipreason = report.longrepr[2]

            test_report.startime_timestamp = report.start
            test_report.stoptime_timestamp = report.stop


        if report.failed == True:
            test_report.precondition_status = STATUS.ERROR
            test_report.status = STATUS.ERROR
            test_report.report = report.longreprtext

            test_report.startime_timestamp = report.start
            test_report.stoptime_timestamp = report.stop


        if report.passed == True:
            test_report.precondition_status = STATUS.PASSED

            test_report.startime_timestamp = report.start


    if test_report.status != STATUS.SKIP and report.when == 'call':
        if report.passed == True:
            test_report.status = STATUS.PASSED


        if report.failed == True:
            test_report.step_number_with_error = get_step_number_with_error(report.longreprtext)
            test_report.status = STATUS.FAIL
            test_report.report = report.longreprtext


    if test_report.status != STATUS.SKIP and report.when == 'teardown':
        if report.failed == True:
            test_report.postcondition_status = STATUS.ERROR
            test_report.report = report.longreprtext
        if report.passed == True:
            test_report.postcondition_status = STATUS.PASSED

        test_report.log = report.caplog
        test_report.stoptime_timestamp = report.stop

    item.config.TSTestReports.save_test_report(test_report) 



@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if fixturedef.baseid != '':
        test_function_name = str(request._pyfuncitem).split(' ')[1][:-1]
        id = f'{test_function_name}::{request.fixturename}'
        nodeid = f'{fixturedef.baseid}::{test_function_name}'

        fixture_report = TestLiteFixtureReports.get_fixture_report(id, nodeid)
        fixture_report.before_start_time = get_time()
        TestLiteFixtureReports.save_fixture_report(id, fixture_report)

        outcome = yield

        finalizers = getattr(fixturedef, '_finalizers', [])
        for index, finalizer in enumerate(finalizers):
            finalizers[index] = fixture_after_save(finalizer, id, nodeid)
            
        fixture_report.before_stop_time = get_time()
        TestLiteFixtureReports.save_fixture_report(id, fixture_report)
    else:
        yield



def pytest_fixture_post_finalizer(fixturedef, request):
    if fixturedef.baseid != '':
        test_function_name = str(request._pyfuncitem).split(' ')[1][:-1]
        id = f'{test_function_name}::{request.fixturename}'
        nodeid = f'{fixturedef.baseid}::{test_function_name}'

        fixture_report = TestLiteFixtureReports.get_fixture_report(id, nodeid)
        fixture_report.name = request.fixturename
        if fixture_report.cached_result is None:
            # При вызое из под другой фикстуры чота странно вызывается финалайзер
            fixture_report.cached_result = fixturedef.cached_result
        TestLiteFixtureReports.save_fixture_report(id, fixture_report)



def pytest_sessionfinish(session: pytest.Session, exitstatus):
    if hasattr(session.config, "workerinput"):
        TestLiteReportManager().save_report()
    else:
        TestLiteReportManager().save_report()
        final_report = TestLiteReportManager().get_reports()
        if session.config.getoption('--savejson') is not None:
            final_report.save_json_file(session.config.getoption("--savejson"))
        if session.config.getoption('--testsuite'):
            final_report.send_json_in_TestLite(testsuite=session.config.getoption('--testsuite'))