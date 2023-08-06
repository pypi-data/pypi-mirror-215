import pandas as pd
import cv2
from openpyxl import Workbook

num_of_table = 0


def get_num():
    return num_of_table


def update_num(new_value):
    global num_of_table
    num_of_table = new_value


def do_df(contours):
    len_contours = len(contours)
    df = pd.DataFrame()
    # Добавляем название столбца
    column_name = "Площадь капли"
    for i in range(len_contours):
        # Генерируем название строки
        row_name = f"Капля  {i + 1}"

        # Генерируем значение для столбца
        value = cv2.contourArea(contours[i])

        # Добавляем строку в датафрейм
        df.loc[row_name, column_name] = value
    to_exel(df)
    return df


def to_exel(data):
    global num_of_table
    workbook = Workbook()

    # Получаем активный лист
    sheet = workbook.active
    print(sheet)
    # Сохраняем рабочую книгу в файл
    workbook.save(f'exel/new{num_of_table}.xlsx')

    data.to_excel(f'exel/new{num_of_table}.xlsx')
    num_of_table += 1
    update_num(num_of_table)
