import logging
import pandas


def panda_filter(link: str) -> pandas.core.frame.DataFrame:
    """Принимает ссылку на страницу и возвращает
    объект DataFrame нужной таблицы, с нужными солбцами
    и с отфильтрованными строками"""

    df = pandas.read_excel(link, usecols='B:F,O')
    start_row_index = df[df.iloc[:, 0] == 'Единица измерения: Метрическая тонна'].index[0]
    end_row_index = df.iloc[start_row_index + 3:, 0][
        (df.iloc[start_row_index + 3:, 0] == 'Итого:') | (df.iloc[start_row_index + 3:, 0].isna())].index[0]
    df = df.iloc[start_row_index + 3:end_row_index]
    df.reset_index(drop=True, inplace=True)
    col_contract_count = df.columns[-1]
    df[col_contract_count] = pandas.to_numeric(df[col_contract_count], errors='coerce')
    df = df[df[col_contract_count].notnull()]
    df = df[df[col_contract_count] > 0]

    return df


def parser_xls(link: str, date: str) -> list[tuple]:
    """Парсит страницу, доставая из нее необходимые данные"""

    total_data_from_page = []

    df = panda_filter(link)

    for row in df.itertuples(index=True, name='Pandas'):
        try:
            exchange_product_id = row[1]
            exchange_product_name = row[2]
            delivery_basis_name = row[3]
            volume = int(row[4])
            total = int(row[5])
            count = int(row[6])
            total_data_from_page.append(
                (
                    exchange_product_id,
                    exchange_product_name,
                    exchange_product_id[:4],
                    exchange_product_id[4:7],
                    delivery_basis_name,
                    exchange_product_id[-1],
                    volume,
                    total,
                    count,
                    date,
                )
            )

        except Exception as e:
            logging.error(f"Данные неверно спарсились, ошибка при попытке обращения к данным. Ошибка {e}")

    return total_data_from_page
