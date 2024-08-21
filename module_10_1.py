from time import sleep, time
from threading import Thread

def write_words(word_count, fname):
    with open(fname, 'w') as f:
        for j in range(word_count):
            f.write(f'Какое-то слово № {j}\n')
            sleep(0.025)
    print(f'Завершилась запись в файл {fname}')

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        tau = -time()
        func(*args, **kwargs)
        tau += time()
        print(f'Время выполнения: {tau} с')

    return wrapper

@timing_decorator
def main_via_functions():
    write_words(10, 'example1.txt')
    write_words(30, 'example2.txt')
    write_words(200, 'example3.txt')
    write_words(100, 'example4.txt')

@timing_decorator
def main_with_threads():
    thread1 = Thread(target=write_words, args=(10, 'example5.txt'))
    thread2 = Thread(target=write_words, args=(30, 'example6.txt'))
    thread3 = Thread(target=write_words, args=(200, 'example7.txt'))
    thread4 = Thread(target=write_words, args=(100, 'example8.txt'))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

def main():
    print('Последовательные вызовы функций:')
    main_via_functions()
    print('\nС использованием потоков:')
    main_with_threads()

if __name__ == '__main__':
    main()
'''
Задача "Потоковая запись в файлы":
Необходимо создать функцию write_words(word_count, file_name), где word_count - количество записываемых слов, 
file_name - название файла, куда будут записываться слова.
Функция должна вести запись слов "Какое-то слово № <номер слова по порядку>" в соответствующий файл с прерыванием после 
записи каждого на 0.1 секунду.
Сделать паузу можно при помощи функции sleep из модуля time, предварительно импортировав её: from time import sleep.
В конце работы функции вывести строку "Завершилась запись в файл <название файла>".

После создания файла вызовите 4 раза функцию write_words, передав в неё следующие значения:
10, example1.txt
30, example2.txt
200, example3.txt
100, example4.txt
После вызовов функций создайте 4 потока для вызова этой функции со следующими аргументами для функции:
10, example5.txt
30, example6.txt
200, example7.txt
100, example8.txt
Запустите эти потоки методом start не забыв, сделать остановку основного потока при помощи join.
Также измерьте время затраченное на выполнение функций и потоков. Как это сделать рассказано в лекции к домашнему заданию.

Пример результата выполнения программы:
Алгоритм работы кода:
# Импорты необходимых модулей и функций
# Объявление функции write_words
# Взятие текущего времени
# Запуск функций с аргументами из задачи
# Взятие текущего времени
# Вывод разницы начала и конца работы функций
# Взятие текущего времени
# Создание и запуск потоков с аргументами из задачи
# Взятие текущего времени
# Вывод разницы начала и конца работы потоков
Вывод на консоль:
Завершилась запись в файл example1.txt
Завершилась запись в файл example2.txt
Завершилась запись в файл example3.txt
Завершилась запись в файл example4.txt
Работа потоков 0:00:34.003411 # Может быть другое время
Завершилась запись в файл example5.txt
Завершилась запись в файл example6.txt
Завершилась запись в файл example8.txt
Завершилась запись в файл example7.txt
Работа потоков 0:00:20.071575 # Может быть другое время
'''

# "C:\Users\Admin\YandexDisk\Urban University 2024\module10\.venv\Scripts\python.exe" "C:\Users\Admin\YandexDisk\Urban University 2024\module10\module_10_1.py"
# Последовательные вызовы функций:
# Завершилась запись в файл example1.txt
# Завершилась запись в файл example2.txt
# Завершилась запись в файл example3.txt
# Завершилась запись в файл example4.txt
# Время выполнения: 8.849347114562988 с
#
# С использованием потоков:
# Завершилась запись в файл example5.txt
# Завершилась запись в файл example6.txt
# Завершилась запись в файл example8.txt
# Завершилась запись в файл example7.txt
# Время выполнения: 5.178734064102173 с
#
# Process finished with exit code 0