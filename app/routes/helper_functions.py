from app.models import City, Node, ModelAccum, State, Equipment, Accum, History, LogCity


def get_model(table_name):
    """
    Функция get_model(table_name) возвращает модель данных, соответствующую указанному названию таблицы.

    Аргументы:
    table_name (str): Название таблицы, для которой нужно получить модель данных.

    Возвращает:
    data[table_name] (Model): Модель данных, соответствующая указанному названию таблицы.

    Исключения:
    KeyError: Возникает, если указанное название таблицы отсутствует в словаре data.

    Пример использования:
    get_model('cities') # Возвращает модель City

    """

    print("in get_model(table_name): table_name =", table_name)
    try:
        data = {
            'cities': City, 
            'nodes':  Node,
            'models': ModelAccum,
            'states': State,
            'equip': Equipment,
            'accs':  Accum,
            'history': History,
            'log_cities': LogCity
            }
        
        # вывод в терминал отладочной информации
        print("in get_model(table_name): return data[table_name] =", data[table_name])
        
        return data[table_name]
    
    except KeyError as err:
        error_message = f"KeyError!!! Ключ '{table_name}' словаря 'data' в data функции get_model(table_name) не найден. Mодель не получена."
        print(error_message)
        raise err(error_message)
    
