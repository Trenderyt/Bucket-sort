from random import *
from __init__ import * # <-- Подключаю собственную библиотеку


# основная программа
while True:
    print("Выбери что выполнить:\n 1. Ввод данных с клавиатуры\n 2. Случайное заполнение списка")
    c = input()
    if c.isdigit() and c in ['1', '2']:  # проверка на число и на совпадение с "1" и "2"
        if c == '1':
            arr = [float(i) for i in input("Введите список чисел:\n").split()]  # создаем список
            block_size = int(input('Какой размерности будут блоки: ')) #задаем размер блоков
            print('Список до сортировки:\n', arr)
            s_arr = block_sort(arr,block_size)  # используем функцию блочной сортировки
            print('Список после сортировки:\n', s_arr)
            sorted_data_plot(s_arr)
            exit()
        elif c == '2':
            n = randint(3, 20)  # рандомная длина списка
            block_size = randint(1,n) #задаем размер блоков
            arr = [uniform(-100, 100) for i in range(n)]  # создаем список с рандомными значениями
            arr = [round(arr[i], 2) for i in range(len(arr))]  # округляем числа с плавающей точкой до двух знаков после запятой
            print('Размер блоков:', block_size)
            print('Список до сортировки:\n', arr)
            s_arr = block_sort(arr,block_size)  # используем функцию блочной сортировки
            print('Список после сортировки:\n', s_arr)
            sorted_data_plot(s_arr)
            exit()
        else:
            continue  # если ввести некорректные данные, программа запускается еще раз