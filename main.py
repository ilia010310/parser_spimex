import time

from collector_links import collector_links
from parser import parser_xls
from core import create_tables, inset_data

if __name__ == '__main__':
    start = time.monotonic()
    links = collector_links()
    create_tables()
    for link, date in links:
        data_from_page = parser_xls(link, date)
        inset_data(data_from_page)

    end = time.monotonic()
    work_time = end - start

    print(f'Время выполнения программы: {int(work_time // 60)}мин. {int(work_time % 60)} сек.')
