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

# def pytest_configure_node(node):
#     print('START---------------pytest_configure_node-------------------------')
#     print(node.__dict__)
#     print('END---------------pytest_configure_node-------------------------')


def pytest_configure(config):
    print('START++++++++++++++++++++++++++++++PYTEST CONFIGURE++++++++++++++++++++++++++++++++START')
    config.TSTestReports = TRs()
    if not hasattr(config, "workerinput"):
        config.FinalReport = pickle.dumps([])
    print('END++++++++++++++++++++++++++++++++PYTEST CONFIGURE++++++++++++++++++++++++++++++++++END')

def pytest_configure_node(node):
    node.workerinput["FinalReport"] = pickle.dumps(node.config.FinalReport)


def pytest_addoption(parser: pytest.Parser):
    parser.addoption('--runtest_show', action="store", default='False')
    parser.addoption('--send_report', action='store', default='True')
    parser.addoption('--save_json', action='store', default=None)



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    print('>>>pytest_runtest_makereportpytest_runtest_makereportpytest_runtest_makereportpytest_runtest_makereportpytest_runtest_makereport<<<<')
    outcome = yield
    report: pytest.TestReport = outcome.get_result()
    log.info(f'CONFIG1: {item.config.TSTestReports}')
    test_report: TR = item.config.TSTestReports.get_test_report(report.nodeid)
    test_report.testcase_key = TestLite_testcase_key(item)
    if report.when == 'setup':
        if report.skipped == True:
            print(f'SETUP is SKIPED')
            test_report.status = STATUS.SKIP
            test_report.skipreason = report.longrepr[2]
            # test_report.add_standart_data(report)
            test_report.startime_timestamp = report.start
            test_report.stoptime_timestamp = report.stop
            test_report.duration = report.duration
            # TRs().save_test_report(test_report)
        if report.failed == True:
            print(f'SETUP is FAILED')
            test_report.precondition_status = STATUS.ERROR
            test_report.status = STATUS.ERROR
            test_report.report = report.longreprtext
            # test_report.add_standart_data(report)
            test_report.startime_timestamp = report.start
            test_report.stoptime_timestamp = report.stop
            test_report.duration = report.duration
            test_report.report = report.longreprtext
            test_report.log = report.caplog
            # test_report.add_log(report.caplog)
            # TRs().save_test_report(test_report)
        if report.passed == True:
            print(f'SETUP is PASSED')
            test_report.precondition_status = STATUS.PASSED
            # test_report.add_standart_data(report)
            test_report.startime_timestamp = report.start
            # test_report.stoptime_timestamp = report.stop
            # test_report.duration = report.duration
            test_report.report = report.longreprtext
            test_report.log = report.caplog
            # test_report.add_log(report.caplog)
            # TRs().save_test_report(test_report)

    if test_report.status != STATUS.SKIP and report.when == 'call':
        if report.passed == True:
            print(f'CALL is PASSED')
            test_report.status = STATUS.PASSED
            # test_report.add_standart_data(report)
            test_report.report = report.longreprtext
            test_report.log = report.caplog
            # TRs().save_test_report(test_report)
        if report.failed == True:
            print(f'CALL is FAILED')
            test_report.step_number_with_error = get_step_number_with_error(report.longreprtext)
            test_report.status = STATUS.FAIL
            test_report.report = report.longreprtext
            test_report.log = report.caplog
            # test_report.add_standart_data(report)
            # TRs().save_test_report(test_report)
            

    if test_report.status != STATUS.SKIP and report.when == 'teardown':
        # print('TEARDOWN')
        # for line_number, test_code_line in enumerate(inspect.getsource(item.obj).split('\n')):
        #     print(f'{line_number}: {test_code_line}')
        if report.failed == True:
            print('TEARDOWN is FAILED')
            test_report.postcondition_status = STATUS.ERROR
        if report.passed == True:
            print('TEARDOWN is PASSED')
            test_report.postcondition_status = STATUS.PASSED
        # test_report.add_standart_data(report)
        test_report.report = report.longreprtext
        test_report.log = report.caplog
        test_report.stoptime_timestamp = report.stop
        # TRs().save_test_report(test_report)
    
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

        if report.when == 'call':
            print('>=========================CALL=============================<')
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
        
        print('<--------------------------pytest_runtest_makereport------------------------------->\n\n')

    print('<<<<pytest_runtest_makereportpytest_runtest_makereportpytest_runtest_makereportpytest_runtest_makereportpytest_runtest_makereport>>>>')
        


def pytest_sessionfinish(session: pytest.Session, exitstatus):
    print('||||||||||||||||||||||||||||||||||||||||||SESSIONFINISH||||||||||||||||||||||||||||||||||||||||||||||')
    # session.config.FinalReport = pickle.dumps(pickle.loads(session.config.FinalReport) + TestLiteFinalReport().get_report_as_list())
    # log.info(f'SESSION_FINISH: {pickle.loads(session.config.FinalReport)}')
    if hasattr(session.config, "workerinput"):
        TestLiteReportManager().save_report()
    else:
        final_report = TestLiteReportManager().get_reports()
        if session.config.getoption('--save_json') is not None:
            final_report.save_json_file(session.config.getoption("--save_json"))
        if session.config.getoption('--send_report') == 'True':
            final_report.send_json_in_TestLite()
    # json_report = TestLiteFinalReport.get_serialize_finall_report()
    # print(json_report)
    # if session.config.getoption('--save_json') is not None:
    #     with open(f'{session.config.getoption("--save_json")}', 'w') as file:
    #         file.write(json_report)
    print('||||||||||||||||||||||||||||||||||||||||||SESSIONFINISH||||||||||||||||||||||||||||||||||||||||||||||')