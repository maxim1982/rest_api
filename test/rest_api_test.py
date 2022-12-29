
from src.rest_api import *
import pytest
from unittest.mock import patch

@pytest.mark.parametrize('data, expected',
                         ([
                           ({'search/part.json' :{'part_code':'ph588'}}, ['ph588',]),
                           
                           ({'basket/add.json': {'part_id': 3,
					                            'warehouse_id': 2,
					                            'quantity': 10 }} , [3, 2, 10]),
                        ])
)
def test_init_query_params(data, expected):
    service = Service_AK('demo', '111122')

    service.init_query_params(data)
    
    index = 0
    for method, params in data.items():
        for key, value in params.items():
            assert  service.query_with_params[method][key] == expected[index]
            index+=1

def test__init__():
    assert True

@patch('requests.get')
def test_request_api(req):
    """
    Проверка метода request_api - 
    основной метод получения данных по API
    """
    
    service = Service_AK('demo', '111122')
    
    service.request_api('basket/add.json')
    assert True

def test_response_api():
    """
    тест полученного результата 
    """
    assert True
