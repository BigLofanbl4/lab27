# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

#Решите следующую задачу: напишите программу, которая будет генерировать матрицу из
#случайных целых чисел. Пользователь может указать число строк и столбцов, а также
#диапазон целых чисел. Произведите обработку ошибок ввода пользователя.

from random import randint


if __name__ == "__main__":
    rows = input("rows: ")
    columns = input("columns: ")
    min_val = input("min_val: ")
    max_val = input("max_val: ")

    try:
        rows = int(rows)
        columns = int(columns)
        min_val = int(min_val)
        max_val = int(max_val)

        if rows <= 0 or columns <= 0:
            raise ValueError("Rows & Colums must be > 0!")

        if min_val >= max_val:
            raise ValueError("min_val must be < max_val!")
    except ValueError as e:
        print(e)
        exit(1)

    # matrix = []
    # for i in range(rows):
    #     row = []
    #     for j in range(columns):
    #         num = randint(min_val, max_val)
    #         row.append(num)
    #     matrix.append(row)

    matrix = [
        [randint(min_val, max_val) for _ in range(columns)] for _ in range(rows)
    ]
    print("Generated matrix:")
    for row in matrix:
        print(row)
