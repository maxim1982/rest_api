from urllib import response
import requests
from json import JSONDecodeError


class Service_AK:
    
    rest_url = 'http://api.autokontinent.ru/v1/'
    error_msg = {
                '1': 'Ошибка авторизации',
                '2': 'Метод не найден',
                '3': 'Обязательный параметр запроса отсутствует или имеет недопустимое значение',
                '4': 'Ошибка данных',
                '5': 'Произошло конкурентное изменение данных',
    }
    
    user_client = ''
    user_pass = ''

    status = {
            '1': 'Принят',
            '2': 'Проверка кредитного лимита',
            '3': 'Заблокирован, требует оплаты',
            '4': 'В работе на складе',
            '5': 'Отгружен',
            '6': 'Отправлен заказ поставщику',
            '7': 'Отказ поставщика',
            '8': 'Поступил на склад',
            '9': 'Отказ',
            '10': 'Подтвержден поставщиком',
            '11': 'Отправлен на аутпост',
            '12': 'Прибыл на аутпост',   
    }
    
    query_with_params = {
        'search/part.json' : {'part_code':  '-'},    # Осуществляет поиск по артикулу товара и возвращает массив найденых карточек товаров.
        'search/price.json' : {'part_id': 0},        # Осуществляет поиск наличия и цен товара и возвращает массив найденых карточек товаров.
        'basket/add.json': {'part_id': 0,           # Добавляет товар в корзину.
                            'warehouse_id': 0,
                            'quantity': 0 },
        'basket/get.json' : None,                   # Возвращает в виде массива список всех позиций, находящихся в корзине
        'basket/del.json' : {'basket_id':0,         # Удаляет позицию из корзины по номеру строки.
                            'version':0},
        'basket/clear.json' : None,                 # Удаляет все позиции из корзины.

        'basket/order.json' : {'delivery_mode_id' : 1}, # Осуществляет отправку всех позиций, содержащихся в корзине, в заказ
        'order/get.json' : {'date_from date' : None,  # Осуществляет получение списка всех заказов клиента за выбранный период, но не раньше чем три месяца назад.
                            'date_to': None },
    }

    response_server = dict()


    def __init__(self, user, password):
        
        #requests.get(url, auth=(username, password))

        if user is not None and password is not None:
            self.user_client = user
            self.user_pass = password
        else :
            raise ValueError(self.error_msg['1'])
    

    def init_query_params(self, params)-> None:
        """
        Инициализация query_params из запроса
        """
        
        for method, data in params.items():
            for key, value in data.items():
                self.query_with_params[method][key] = value


    def request_api(self, method):
        """
        Общий метод для запросов к АПИ Автоконтинета
        """
        
        data = {}
        response = {}

        try:
            response = requests.get(self.rest_url+method, params=self.query_with_params[method], timeout=4)
        except requests.exceptions.RequestException as error:
            raise ValueError(error)
                
        try:
            data = response.json()
        except JSONDecodeError as error2:
            data = {}

        return data
    

    def response_api(self, response):
        """
        Подготовка данных из запроса 
        """

        self.response_server = response 


service = Service_AK('demo', '111122')
data = {'search/part.json' :{'part_code':'ph588'}}
service.init_query_params(data)

data = {'basket/add.json': {'part_id': 12220, 
                            'warehouse_id': 1,
                            'quantity': 99 }}

service.init_query_params(data)

print(service.query_with_params)

service.request_api('search/part.json') #TODO :  ERROR JSON 