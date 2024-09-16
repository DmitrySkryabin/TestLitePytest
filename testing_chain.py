
from typing import Any


class FinalReport:

    def __init__(self, data):
        self.data = data
        self.json_data = None 

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.data
    
    def __repr__(self) -> str:
        return str(self.data)
    
    def __iter__(self):
        yield self.data

    @property
    def json(self):
        self.json_data =f'JSON: {self.data}'
        return self.json_data
        
    def save_json(self):
        if self.json_data is not None:
            print(f'SAVING JSON...')
            print(f'{self.json_data}')

    def print_data(self):
        print(self.data)

    def save_data(self):
        print('saving_data')


class TestingChein:

    def __init__(self, data: list=None):
        self.data = data


    def set_data(self, data: list):
        self.data = data

    def get_data(self):
        return FinalReport(self.data)



testing_cahin = TestingChein(['data1', 'data2', 'data3'])


finalreport = testing_cahin.get_data()

print(finalreport.json)
print('-------------')
finalreport.save_json()