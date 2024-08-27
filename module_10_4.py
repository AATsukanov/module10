import queue
from threading import Thread
from time import sleep
from random import randint

'''Цель: Применить очереди в работе с потоками, используя класс Queue.'''

class Table:
    '''
    Задача "Потоки гостей в кафе":
    Необходимо имитировать ситуацию с посещением гостями кафе.
    Создайте 3 класса: Table, Guest и Cafe.
    Класс Table:
    Объекты этого класса должны создаваться следующим способом - Table(1)
    Обладать атрибутами number - номер стола и guest - гость, который сидит за этим столом (по умолчанию None)'''
    def __init__(self, number: int):
        self.number = number
        self.guest = None

    def __bool__(self):
        if self.guest == None:
            return False
        return True

class Guest(Thread):
    '''
    Класс Guest:
    Должен наследоваться от класса Thread (быть потоком).
    Объекты этого класса должны создаваться следующим способом - Guest('Vasya').
    Обладать атрибутом name - имя гостя.
    Обладать методом run, где происходит ожидание случайным образом от 3 до 10 секунд.
    '''
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        tau = randint(3, 10)
        sleep(tau)

    def __str__(self):
        return self.name

class Cafe:
    # Класс Cafe:
    # Объекты этого класса должны создаваться следующим способом - Cafe(Table(1), Table(2),....)
    # Обладать атрибутами queue - очередь (объект класса Queue) и tables - столы в этом кафе (любая коллекция).
    # Обладать методами guest_arrival (прибытие гостей) и discuss_guests (обслужить гостей).
    def __init__(self, *tables: Table):
        self.queue = queue.Queue()
        self.tables = {table.number: table for table in tables}
        # self.tables = tables

    # Метод guest_arrival(self, *guests):
    # Должен принимать неограниченное кол-во гостей (объектов класса Guest).
    # Далее, если есть свободный стол, то сажать гостя за стол (назначать столу guest),
    # запускать поток гостя и выводить на экран строку "<имя гостя> сел(-а) за стол номер <номер стола>".
    # Если же свободных столов для посадки не осталось,
    # то помещать гостя в очередь queue и выводить сообщение "<имя гостя> в очереди".
    def _find_free_table(self):
        for n, table in self.tables.items():
            if not table:
                return n
        # в самом конце подразумеваем:
        # return None

    def _all_tables_free(self):
        for n, table in self.tables.items():
            if table:
                return False
        return True

    def guest_arrival(self, *guests: Guest):
        for guest in guests:
            n = self._find_free_table()
            if n is None:
                self.queue.put(guest)
                print(f'{guest} ждет в очереди...')
            else:
                self.tables[n].guest = guest
                guest.start()
                print(f'{guest} сел(-а) за стол номер {n}.')

    # Метод discuss_guests(self):
    # Этот метод имитирует процесс обслуживания гостей.
    # Обслуживание должно происходить пока очередь не пустая (метод empty) или хотя бы один стол занят.
    # Если за столом есть гость(поток) и гость(поток) закончил приём пищи(поток завершил работу - метод is_alive),
    # то вывести строки "<имя гостя за текущим столом> покушал(-а) и ушёл(ушла)" и "Стол номер <номер стола> свободен". Так же текущий стол освобождается (table.guest = None).
    # Если очередь ещё не пуста (метод empty) и стол один из столов освободился (None),
    # то текущему столу присваивается гость взятый из очереди (queue.get()).
    # Далее выводится строка "<имя гостя из очереди> вышел(-ла) из очереди и сел(-а) за стол номер <номер стола>"
    def discuss_guests(self):
        while not (self._all_tables_free() and self.queue.empty()):
            for n, t in self.tables.items():
                if not t.guest is None:
                    if not t.guest.is_alive():
                        print(f'{t.guest} покушал(-а) и ушёл(ушла).\nСтол номер {n} свободен.')
                        if not self.queue.empty():
                            self.tables[n].guest = self.queue.get()
                            self.tables[n].guest.start()
                            print(f'{t.guest} вышел(-ла) из очереди и сел(-а) за стол номер {n}.')
                        else:
                            self.tables[n].guest = None
            # print(f'В очереди {self.queue.qsize()} посетителей.')

# Далее запустить поток этого гостя (start)
# Таким образом мы получаем 3 класса на основе которых имитируется работа кафе:
# Table - стол, хранит информацию о находящемся за ним гостем (Guest).
# Guest - гость, поток, при запуске которого происходит задержка от 3 до 10 секунд.
# Cafe - кафе, в котором есть определённое кол-во столов и происходит имитация прибытия гостей
# (guest_arrival) и их обслуживания (discuss_guests).

def main():
    # Создание столов
    tables = [Table(number) for number in range(1, 6)]
    # Имена гостей
    guests_names = ['Мария', 'Олег', 'Вахтанг', 'Серёга', 'Даша', 'Арман', 'Виктория', 'Никита', 'Павел', 'Илья', 'Александр']
    # Создание гостей
    guests = [Guest(name) for name in guests_names]
    # Заполнение кафе столами
    cafe = Cafe(*tables)
    # Приём гостей
    cafe.guest_arrival(*guests)
    # Обслуживание гостей
    cafe.discuss_guests()

if __name__ == '__main__':
    main()

'''
Вывод на консоль (последовательность может меняться из-за случайного время пребывания гостя):
Maria сел(-а) за стол номер 1
Oleg сел(-а) за стол номер 2
Vakhtang сел(-а) за стол номер 3
Sergey сел(-а) за стол номер 4
Darya сел(-а) за стол номер 5
Arman в очереди
Vitoria в очереди
Nikita в очереди
Galina в очереди
Pavel в очереди
Ilya в очереди
Alexandra в очереди
Oleg покушал(-а) и ушёл(ушла)
Стол номер 2 свободен
Arman вышел(-ла) из очереди и сел(-а) за стол номер 2
.....
Alexandra покушал(-а) и ушёл(ушла)
Стол номер 4 свободен
Pavel покушал(-а) и ушёл(ушла)
Стол номер 3 свободен
Примечания:
Для проверки значения на None используйте оператор is (table.guest is None).
Для добавления в очередь используйте метод put, для взятия - get.
Для проверки пустоты очереди используйте метод empty.
Для проверки выполнения потока в текущий момент используйте метод is_alive.'''