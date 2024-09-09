import multiprocessing as mp
from PIL import Image # pip install pillow
from queue import Empty
import os

def resize_image(fnames, queue):
    for fname in fnames:
        img = Image.open(fname)
        img = img.resize((640, 360)) #кортеж в аргументе (xr, yr)
        queue.put((fname, img))

def change_color_and_save(queue):
    while True:
        try:
            fname, img = queue.get(timeout=5) #после опустошения ждем 5 секунд и вырубаемся
        except Empty:
            break
        img = img.convert('L') #L - черно-белый
        img.save(fname[:-3] + 'bw.png')

if __name__ == '__main__':
    data = []
    queue = mp.Queue()

    #for image in range(1, 10):
    #    data.append(f'./images/img_{image}.jpg')
    data = ['./images/'+fname for fname in os.listdir('./images/') if '.png' in fname]

    resize_process = mp.Process(target=resize_image, args=(data, queue))
    change_process = mp.Process(target=change_color_and_save, args=(queue, )) #кортеж на входе поэтому (.., )

    resize_process.start()
    change_process.start()

    resize_process.join()
    change_process.join()