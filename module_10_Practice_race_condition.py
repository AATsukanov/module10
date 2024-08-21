import threading

''' В версии python выше 3.10
    эта проблема решена!
'''

x = 0

def thread_task_no_lock(n):
    global x
    for _ in range(n):
        x = x + 1

lock1 = threading.Lock()
def thread_task(n):
    global x
    for _ in range(n):
        lock1.acquire()
        x = x + 1
        lock1.release()

# или
#     with lock...
#         x += 1

def main():
    t1 = threading.Thread(target=thread_task, args=(1_000_000,))
    t2 = threading.Thread(target=thread_task, args=(1_000_000,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(x)

if __name__ == '__main__':
    main()