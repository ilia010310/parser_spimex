import logging

import requests
from bs4 import BeautifulSoup


def collector_links_from_page(url: str) -> (list[tuple[str, str]], bool):
    """Собирает ссылки с одной страницы.
    Принимает ссылку на страницу.
    Отдает список с данными и флаг для остановки/продолжения цикла"""

    tm_links = []
    stop_loop = False
    # отправляем запрос на страницу и логируем всевозможные ошибки
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectTimeout:
        logging.error(f'Время ожидания вышло. Невозможно получить ответ от страницы {url}')
        raise requests.exceptions.ConnectTimeout
    except requests.exceptions.ConnectionError:
        logging.error(f'Невозможно получить ответ от страницы {url}')
        raise requests.exceptions.ConnectionError
    if response.status_code != 200:
        logging.error(f'Страничка {url} не ответила на запрос.')
        raise requests.exceptions.RequestException
    html_content = response.text

    # парсим
    soup = BeautifulSoup(html_content, 'html.parser')

    # получаем значения ссылок и даты
    for link in soup.find_all(
            'a',
            class_='accordeon-inner__item-title link xls')[:10]:
        tm_links.append(f'https://spimex.com{link.get("href")}')
    counter = -1
    for div in soup.find_all('div', class_='accordeon-inner__item-inner__title')[:10]:
        counter += 1
        for span in div.find_all('span'):
            date = span.get_text(strip=True)

        if int(date.split('.')[2]) < 2024:
            del tm_links[counter:]
            stop_loop = True
            break

        else:
            tm_links[counter] = (tm_links[counter], date)

    return tm_links, stop_loop


def collector_links() -> list[tuple[str, str]]:
    """Собирает все ссылки на xls формы только за 2024 год,
     со всех страниц, возвразает список с кортежами,
    в каждом из которых: ссылка в виде строки и дата в виде строки"""

    num = 0  # пагинация страницы, на которой собираем ссылки
    stop_loop = False  # флаг, обозначающий конец сбора ссылок, когда попался другой год

    total_links = []  # итоговый лист с кортежами
    while not stop_loop:
        num += 1
        url = f'https://spimex.com/markets/oil_products/trades/results/?page=page-{num}'
        try:
            tm_links, stop_loop = collector_links_from_page(url)
        except Exception:
            break

        total_links.extend(tm_links)

    return total_links
