def bucket_sort(input_list):
    # Находим максимальное значение в списке
    max_value = max(input_list)
    # Затем используем длину списка, чтобы определить, какое значение в списке попадет в какой блок
    size = max_value / len(input_list)

    # Создаем n пустых блоков, где n равно длине входного списка
    buckets_list = []
    for x in range(len(input_list)):
        buckets_list.append([])

    # Помещаем элементы списка в разные блоки на основе size
    for i in range(len(input_list)):
        j = int(input_list[i] / size)
        if j != len(input_list):
            buckets_list[j].append(input_list[i])
        else:
            buckets_list[len(input_list) - 1].append(input_list[i])

    # Сортируем элементы внутри блоков с помощью сортировки вставкой
    for z in range(len(input_list)):
        insertion_sort(buckets_list[z])

    # Объединяем блоки с отсортированными элементами в один список
    final_output = []
    for x in range(len(input_list)):
        final_output = final_output + buckets_list[x]
    return final_output


def insertion_sort(bucket):
    for i in range(1, len(bucket)):
        var = bucket[i]
        j = i - 1
        while (j >= 0 and var < bucket[j]):
            bucket[j + 1] = bucket[j]
            j = j - 1
        bucket[j + 1] = var


input_list = [1.20, 0.22, 0.43, 0.36, 0.39, 0.27]
print('Список до сортировки:')
print(input_list)
sorted_list = bucket_sort(input_list)
print('Список после сортировки:')
print(sorted_list)
