import json
import requests
import re
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, rules_file):
        self._rules_file = rules_file
        self._parsing()

    def _parsing(self):
        # чтение правил парсинга из файла
        try:
            print(f'Чтение правил парсинга из файла "{self._rules_file}"')
            with open(self._rules_file, 'r') as f:
                data = json.load(f)
        except:
            print(f'Ошибка чтения файла правил парсинга "{self._rules_file}"')
            return

        # извлечение правил и запуск парсинга
        for i in data:
            try:
                name = i['name']
                input_file = i['input_file']
                output_file = i['output_file']
                rules = i['rules']
            except:
                print('Ошибка извлечения правил парсинга', i)
                continue

            self._parse_from_file(name, input_file, output_file, rules)
            print('Ок!')

    def _parse_from_file(self, name, input_file, output_file, rules):
        print(f'Парсинг "{name}"')
        print(f'Чтение входящего файла "{input_file}"')

        try:
            with open(input_file, 'r') as f:
                in_data = json.load(f)
        except:
            print(f'Ошибка чтения входящего файла "{input_file}"')
            return

        out_data = []  # исходящие данные
        count = 0
        errors = 0
        url_errors = 0

        # парсинг каждой модели товара из списка во входящем файле
        for i in in_data:
            idc = i['id']   # id товара
            url = i['url']  # ссылка на товар в интернет-магазине
            count += 1

            print(f'Загрузка URL: {url}')
            try:
                response = requests.get(url)
                if response.status_code:
                    print(f'Ошибка статуса (код {response.status_code})')
                    raise Exception
            except:
                url_errors += 1
                print(f'Ошибка чтения {url}')
            else:
                soup = BeautifulSoup(response.text, 'html.parser')
                r_data = {'id': idc}

                for j in rules:
                    r_name = j['name']
                    r_tag = j['tag']
                    r_class = j['class']
                    r_type = j['type']

                    try:
                        item = soup.find(r_tag, class_=r_class)  # первичное извлечение данных
                        if not item:
                            item = ''
                        else:
                            # если тип данных str, убираем двойные пробелы и переводы строк
                            if r_type == 'str':
                                item = re.sub('^\s+|\n|\r|\s+$', '', str(item.text)).replace('  ', ' ')

                            # если тип данных int, убираем всё, что не цифры
                            if r_type == 'int':
                                item = ''.join(c for c in item.text.replace(' ', '') if c.isdigit())
                                try:
                                    item = int(item)
                                except:
                                    pass

                        if not item and r_type == 'int':
                            continue

                        r_data[r_name] = item
                    except:
                        errors += 1

                out_data.append(r_data)

        print(f'Обработано {count} позиций, ошибок обработки: {errors}, ошибок чтения url: {url_errors}')
        print(f'Запись исходящего файла "{output_file}"')

        try:
            with open(output_file, 'w', encoding='utf8') as f:
                f.write(json.dumps(out_data, ensure_ascii=False))
        except:
            print(f'Ошибка записи исходящего файла "{output_file}"')
