### Парсер цен интернет-магазинов.

Используется для мониторинга поставщиками рекомендуемых розничных цен (РРЦ) у своих контрагентов.

На вход подаются заранее сформированные информационной системой поставщика файлы в формате **json** со ссылками на
контролируемые товары в интернет-магазинах контрагентов.

На выходе формируются файлы в формате **json** с ценами в интернет-магазинах контрагентов. Полученные файлы готовы
для дальнейшего анализа и сопоставления с текущим прайсом информационной системой поставщика .

Парсинг производится с помощью библиотеки **BeautifulSoup** по правилам, которые прописываются в файле **rules.json**.

#### Правила (rules.json)

Список из словарей с правилами парсинга каждого интернет-магазина.

[ { "name" : "название_инет_магазина_1",
    "input_file" : "input/входящий_файл_1.json",
    "output_file" : "output/входящий_файл_1.json",
    "rules" :
      [
        {
          "name" : "_имя_парсинга_1_",
          "tag" : "_тег_в_BeautifulSoup_1_",
          "class" : "_класс_в_BeautifulSoup_1_",
          "type" : "_тип_1_"
        }
      ]
    }
]

где: BeautifulSoup.find(_тег_в_BeautifulSoup_n_, class_=_класс_в_BeautifulSoup_n_)

#### Входящий файл:

Список из словарей с парой id - url, где:
id - внутренний артикул товара поставщика,
url - ссылка на данный товар у конрагента.

[ { "id" : _код_товара_1_, "url" : "_url_товара_1_" },
{ "id" : _код_товара_2_, "url" : "_url_товара_2_" }]

#### Исходящий файл:

Список из словарей с данными парсинга по правилам в **rules.json**

[{"id": "_код_товара_1_",
"_имя_парсинга_1_1_" : "_результат_парсинга_1_1_", 
"_имя_парсинга_1_2_": "_результат_парсинга_1_2_"},
{"id": "_код_товара_2_",
"_имя_парсинга_2_1_" : "_результат_парсинга_2_1_", 
"_имя_парсинга_2_2_": "_результат_парсинга_2_2_", 
"_имя_парсинга_2_3_": "_результат_парсинга_2_3_"}]