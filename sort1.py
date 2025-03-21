import time
import random


arr = [random.randint(1, 10000) for _ in range(10000)]

def bubble_sort(array):
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array

def heapify(array, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and array[left] > array[largest]:
        largest = left

    if right < n and array[right] > array[largest]:
        largest = right

    if largest != i:
        array[i], array[largest] = array[largest], array[i]
        heapify(array, n, largest)

def heap_sort(array):
    n = len(array)

    for i in range(n // 2 - 1, -1, -1):
        heapify(array, n, i)

    for i in range(n - 1, 0, -1):
        array[i], array[0] = array[0], array[i]
        heapify(array, i, 0)
    return array

def shell_sort(array):
    n = len(array)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = array[i]
            j = i
            while j >= gap and array[j - gap] > temp:
                array[j] = array[j - gap]
                j -= gap
            array[j] = temp
        gap //= 2
    return array

def measure_time(sort_function, array):
    total_time = 0
    for _ in range(10):
        arr_copy = array.copy()
        start_time = time.time()
        sort_function(arr_copy)
        end_time = time.time()
        total_time += (end_time - start_time)
    return total_time / 10

bubble_time = measure_time(bubble_sort, arr)
heap_time = measure_time(heap_sort, arr)
shell_time = measure_time(shell_sort, arr)

# Вывод результатов
print(f"Среднее время пузырьковой сортировки: {bubble_time:.5f} секунд")
print(f"Среднее время пирамидальной сортировки: {heap_time:.5f} секунд")
print(f"Среднее время сортировки Шелла: {shell_time:.5f} секунд")