import pytest 
import inspect
import json
from lite import TestLiteTestReports as TRs
from lite import TestLiteTestReport as TR
from lite import STATUS, TestLite_id, get_step_number_with_error, TestReportJSONEncoder, TestLiteFinalReport


# def pytest_configure_node(node):
#     print('START---------------pytest_configure_node-------------------------')
#     print(node.__dict__)
#     print('END---------------pytest_configure_node-------------------------')

# def pytest_xdist_node_collection_finished(node, ids):
#     print('START---------------pytest_xdist_node_collection_finished-------------------------')
#     print(node.__dict__)
#     print('-----------------------------------------------------------------------------------')
#     print('END---------------pytest_xdist_node_collection_finished-------------------------')


def pytest_configure(config):
    print('START++++++++++++++++++++++++++++++PYTEST CONFIGURE++++++++++++++++++++++++++++++++START')
    TRs()
    print('END++++++++++++++++++++++++++++++++PYTEST CONFIGURE++++++++++++++++++++++++++++++++++END')


def pytest_addoption(parser: pytest.Parser):
    parser.addoption('--runtest_show', action="store", default='True')
    parser.addoption('--save_json', action='store', default=None)



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    print('>>>pytest_runtest_makereportpytest_runtest_makereportpytest_runtest_makereportpytest_runtest_makereportpytest_runtest_makereport<<<<')
    outcome = yield
    report:pytest.TestReport = outcome.get_result()

    test_report = TRs.get_test_report(report.nodeid)
    if report.when == 'setup':
        if report.skipped == True:
            print(f'SETUP is SKIPED')
            test_report.status = STATUS.SKIP
            test_report.skipreason = report.longrepr[2]
            test_report.add_standart_data(report)
            # TRs.save_test_report(test_report)
        if report.failed == True:
            print(f'SETUP is FAILED')
            test_report.precondition_status = STATUS.ERROR
            test_report.status = STATUS.ERROR
            test_report.report = report.longreprtext
            test_report.add_standart_data(report)
            # TRs.save_test_report(test_report)
        if report.passed == True:
            print(f'SETUP is PASSED')
            test_report.precondition_status = STATUS.PASSED
            test_report.add_standart_data(report)
            # TRs.save_test_report(test_report)

    if test_report.status != STATUS.SKIP and report.when == 'call':
        if report.passed == True:
            print(f'CALL is PASSED')
            test_report.status = STATUS.PASSED
            test_report.add_standart_data(report)
            # TRs.save_test_report(test_report)
        if report.failed == True:
            print(f'CALL is FAILED')
            test_report.step_number_with_error = get_step_number_with_error(report.longreprtext)
            test_report.status = STATUS.FAIL
            test_report.report = report.longreprtext
            test_report.add_standart_data(report)
            # TRs.save_test_report(test_report)
            

    if test_report.status != STATUS.SKIP and report.when == 'teardown':
        # for line_number, test_code_line in enumerate(inspect.getsource(item.obj).split('\n')):
        #     print(f'{line_number}: {test_code_line}')
        test_report.testcase_uuid = TestLite_id(item)
        if report.failed == True:
            print('TEARDOWN is FAILED')
            test_report.postcondition_status = STATUS.ERROR
        if report.passed == True:
            print('TEARDOWN is PASSED')
            test_report.postcondition_status = STATUS.PASSED
        test_report.add_standart_data(report)
        # TRs.save_test_report(test_report)
    
    print('TESTREPORTTESTREPORTTESTREPORTTESTREPORTTESTREPORTTESTREPORTTESTREPORTTESTREPORT\n')
    print(test_report)
    with open(f'test_reports/{test_report.nodeid.split(":")[-1]}___{report.when}.json', 'w') as file:
        file.write(TestLiteFinalReport.get_serialize_finall_report())
    from logger import Logger
    log = Logger(__name__).get_logger()
    log.info('-------------------------------------------------------------------------------')
    log.info(call.__dict__)
    log.info('-------------------------------------------------------------------------------')
    print('TESTREPORTTESTREPORTTESTREPORTTESTREPORTTESTREPORTTESTREPORTTESTREPORTTESTREPORT\n')
    TRs.save_test_report(test_report)
    # TRs.save_current_queue(TRs.counter)
    # TRs.counter = TRs.counter + 1

        

    

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
    # for test_report in TRs.TestReports:
    #     print('---------------------------------------')
    #     print(TRs.TestReports[test_report])
    #     print('----------------encoded_data---------------------')
    #     print(TestReportJSONEncoder().encode(TRs.TestReports[test_report]))
    #     print('---------------------------------------')
    # print(TestLiteFinalReport.get_finall_report())
    json_report = TestLiteFinalReport.get_serialize_finall_report()
    # print(json_report)
    if session.config.getoption('--save_json') is not None:
        with open(f'{session.config.getoption("--save_json")}', 'w') as file:
            file.write(json_report)
    print('||||||||||||||||||||||||||||||||||||||||||SESSIONFINISH||||||||||||||||||||||||||||||||||||||||||||||')