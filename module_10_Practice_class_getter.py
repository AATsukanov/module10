from threading import Thread
import requests

class Getter(Thread):

    results = []
    def __init__(self, URL):
        self.URL = URL
        super().__init__()

    def run(self):
        response = requests.get(url=self.URL)
        Getter.results.append(response.json())

def main():
    threads = []
    nn = 8

    for n in range(nn):
        thread = Getter(URL='https://binaryjazz.us/wp-json/genrenator/v1/genre/')
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(Getter.results)

if __name__ == '__main__':
    main()