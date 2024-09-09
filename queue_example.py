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
    other_elem = []
    while not queue_list.empty():
        queue_element = queue_list.get()
        if elem == queue_element:
            for element in other_elem:
                queue_list.put(element)
            return queue_element
        else:
            other_elem.append(queue_element)


test_report_1 = TestReport(name='test_1', description=None, datetime=datetime.datetime(2024, 9, 6))
test_report_2 = TestReport(name='test_2', description='Description_2', datetime=datetime.datetime(2024, 9, 4))
test_report_3 = TestReport(name='test_3', description=None, datetime=datetime.datetime(2024, 9, 6))
test_report_4 = TestReport(name='test_4', description='Description_4', datetime=datetime.datetime(2024, 9, 10))


test_reports = [test_report_1, test_report_2, test_report_3, test_report_4]

for item in test_reports:
    save_element(item)

print('------------------INITIAL PRINT---------------------------')
while not queue_list.empty():
    print(queue_list.get())
print('------------------INITIAL PRINT---------------------------')

print('------------------CONTROL PRINT---------------------------')
for report in test_reports:
    queue_list.put(report)
print('------------------CONTROL PRINT---------------------------')


print(get_element(test_report_2))
print('------------------AFTER PRINT---------------------------')
while not queue_list.empty():
    print(queue_list.get())
print('------------------AFTER PRINT---------------------------')
