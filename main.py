from random import *
import matplotlib.pyplot as plt

def bucket_sort(input_list):
    max_value = max(input_list)  # Находим максимальное значение в списке
    size = max_value / len(
        input_list)  # Затем используем длину списка, чтобы определить, какое значение в списке попадет в какой блок
    buckets_list = []  # Создаем n пустых блоков, где n равно длине входного списка
    for _ in range(len(input_list)):
        buckets_list.append([])

    for i in range(len(input_list)):  # Помещаем элементы списка в разные блоки на основе size
        j = int(input_list[i] / size)
        if j != len(input_list):
            buckets_list[j].append(input_list[i])
        else:
            buckets_list[len(input_list) - 1].append(input_list[i])

    for z in range(len(input_list)):  # Сортируем элементы внутри блоков с помощью сортировки вставкой
        insertion_sort(buckets_list[z])

    final_output = []  # Объединяем блоки с отсортированными элементами в один список
    for x in range(len(input_list)):
        final_output = final_output + buckets_list[x]
    return final_output


def insertion_sort(bucket):  # Испольуем сортировку вставкой для каждого блока
    for i in range(1, len(bucket)):
        var = bucket[i]
        j = i - 1
        while (j >= 0 and var < bucket[j]):  # будет работать до тех пор, пока j не отрицательное и var меньше чем элемент под индексом j
            bucket[j + 1] = bucket[j]
            j = j - 1
        bucket[j + 1] = var

def sorted_data_plot(sorted_data, filename='sorted_data_plot.png'):
    plt.figure(figsize=(10, 5))
    plt.plot(sorted_data, marker='o', linestyle='-', color='b')
    plt.title('График отсортированных данных')
    plt.xlabel('Индекс')
    plt.ylabel('Значение')
    plt.grid()
    plt.savefig(filename)
    plt.close()
    print(f'График сохранен как {filename}')



while True:
    print("Выбери что выполнить:\n 1. Ввод данных с клавиатуры\n 2. Случайное заполнение списка")
    c = input()
    if c.isdigit() and c in ['1', '2']:  # проверка на число и на совпадение с "1" и "2"
        if c == '1':
            a_list = [float(i) for i in input("Введите список чисел:\n").split()]  # создаем список
            print('Список до сортировки:\n', a_list)
            s_list = bucket_sort(a_list)  # используем функцию блочной сортировки
            print('Список после сортировки:\n', s_list)
            exit()
        elif c == '2':
            n = randint(3, 20)  # рандомная длина списка
            a_list = [uniform(-100, 100) for i in range(n)]  # создаем список с рандомными значениями
            a_list = [round(a_list[i], 2) for i in
                      range(len(a_list))]  # округляем числа с плавающей точкой до двух знаков после запятой
            print('Список до сортировки:\n', a_list)
            s_list = bucket_sort(a_list)  # используем функцию блочной сортировки
            print('Список после сортировки:\n', s_list)
            sorted_data_plot(s_list)
            exit()
        else:
            continue  # если ввести некорректные данные, программа запускается еще раз
