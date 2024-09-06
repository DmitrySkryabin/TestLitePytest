import queue
import dataclasses
import datetime

queue_list = queue.Queue()

@dataclasses.dataclass
class TestReport:
    name: str = None
    description: str = None
    datetime:str = None


def save_element(elem):
    queue_list.put(elem)


def get_element(elem):
    while elem != queue_list.get():
        pass
    else:
        print(queue_list.get())


test_report_1 = TestReport(name='test_1', description=None, datetime=datetime.datetime(2024, 9, 6))
test_report_2 = TestReport(name='test_2', description='Description_2', datetime=datetime.datetime(2024, 9, 4))
test_report_3 = TestReport(name='test_3', description=None, datetime=datetime.datetime(2024, 9, 6))
test_report_4 = TestReport(name='test_4', description='Description_4', datetime=datetime.datetime(2024, 9, 10))


test_reports = [test_report_1, test_report_2, test_report_3, test_report_4]

for item in test_reports:
    save_element(item)


get_element(test_report_2)
