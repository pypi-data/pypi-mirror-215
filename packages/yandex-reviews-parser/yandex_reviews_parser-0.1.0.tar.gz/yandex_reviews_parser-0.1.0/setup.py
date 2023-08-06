# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['undetected-chromedriver>=3.5.0,<4.0.0']

setup_kwargs = {
    'name': 'yandex-reviews-parser',
    'version': '0.1.0',
    'description': 'Python yandex company reviews parser',
    'long_description': '# Парсер отзывов c Yandex Карт\n\nСкрипт парсит отзывы с Yandex Карт<br>\nДля парсинга необходимо указать id компании в начале обработки скрипта\n\nПо результатам выполнения, создается файл result.json, в котором:\n```json\n{\n  "company_info": {\n    "name": "Дилерский центр Hyundai",\n    "rating": 5.0,\n    "count_rating": 380,\n    "stars": 5\n  },\n  "company_reviews": [\n    {\n      "name": "Иван Иванов",\n      "icon_href": "https://avatars.mds.yandex.net/get-yapic/51381/cs8Tx0sigtfayYhRQBDJkavzJU-1/islands-68",\n      "date": 1681992580.04,\n      "text": "Выражаю огромную благодарность работникам ",\n      "stars": 5\n    }\n  ]\n}\n```\n\n\nНеобходимо установить пакеты<br>\n```shell\npip install -R requirements.txt\n```\n\nДалее запусить main.py\n```shell\npython main.py\n```\nВводим ID компании которую нужно спарсить.<br>\nИ получаем результат',
    'author': 'Daniil',
    'author_email': 'danil16m@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
