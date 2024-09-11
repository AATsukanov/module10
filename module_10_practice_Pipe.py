import multiprocessing as mp
from PIL import Image # pip install pillow
import os

def resize_image(fnames, pipe: mp.Pipe, stop_event):
    for fname in fnames:
        img = Image.open(fname)
        img = img.resize((640, 360)) #кортеж в аргументе (xr, yr)
        img.save(fname)
        pipe.send(fname)
    stop_event.set()

def change_color_and_save(pipe: mp.Pipe, stop_event):
    while not stop_event.is_set():
        fname = pipe.recv()
        img = Image.open(fname)
        img = img.convert('L') #'L' - черно-белый, '1' - dithering
        img.save(fname[:-3] + 'bw.png')

if __name__ == '__main__':
    data = []
    conn1, conn2 = mp.Pipe() #используем Pipe!
    stop_event = mp.Event()

    #for image in range(1, 10):
    #    data.append(f'./images/img_{image}.jpg')
    data = ['./images/'+fname for fname in os.listdir('./images/') if '.png' in fname]

    resize_process = mp.Process(target=resize_image, args=(data, conn1, stop_event)) # ВАЖНО: передаем концы трубы conn1 и в сл.строке conn2
    change_process = mp.Process(target=change_color_and_save, args=(conn2, stop_event)) # в обоих случаях передаем stop_event

    resize_process.start()
    change_process.start()

    resize_process.join()
    change_process.join()