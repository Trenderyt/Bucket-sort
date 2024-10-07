from random import *
import matplotlib.pyplot as plt

def block_sort(arr, block_size):
    blocks = [] #создаем пустой список для хранения отсортированных блоков
    for i in range(0, len(arr), block_size): #Разбиваем список на блоки с заданным размером
        block = arr[i:i + block_size]
        blocks.append(sorted(block)) #сортируем каждый блок и добавляем его в список отсортированных блоков
        #blocks.append(sorted(block, reverse=True)) #для реверсивной программы

    result = [] #создаем пустой список для отсортированных блоков

    # цикл для сортировки по убыванию
    # while blocks:
    #     max_idx = 0
    #     for i in range(1, len(blocks)):  # находим наибольший элемент в каждом блоке
    #         if blocks[i][0] > blocks[max_idx][0]:
    #             max_idx = i
    #     result.append(blocks[max_idx].pop(0))  # удаляем из блока самый большой элемент и добавляем его в результат
    #     if len(blocks[max_idx]) == 0:  # если блок пустой, мы удаляем его из списка отсортированных блоков
    #         blocks.pop(max_idx)

    while blocks: #объединяем отсортированные блоки в список результат
        min_idx = 0
        for i in range(1, len(blocks)): #Находим наименьший элемент в каждом блоке
            if blocks[i][0] < blocks[min_idx][0]:
                min_idx = i
        result.append(blocks[min_idx].pop(0)) #Удаляем из блока самый маленький элемент и добавляем его в результат
        if len(blocks[min_idx]) == 0: #если блок пустой мы удаляем его из списка отсортированных блоков
            blocks.pop(min_idx)

    return result #выводим результат(отсортированный список в порядке возрастания)


def sorted_data_plot(s_arr, filename='sorted_data_plot.png'):
    plt.figure(figsize=(10, 5))
    plt.plot(s_arr, marker='o', linestyle='-', color='b')
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