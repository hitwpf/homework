import threading
from time import sleep
from .mvsearch import movieSearch
from .localCache import localCache

# 伴随线程，主要是提供异步拉取数据功能，内置有任务队列
class DaemonThread(threading.Thread):
    def __init__(self):
        super(DaemonThread, self).__init__()
        self.queue = []
        self.max_size = 100
        self.current_position = -1

    def enqueue(self, title):
        if self.current_position >= self.max_size:
            self.queue[0] = title
        else:
            self.queue.append(title)
            self.current_position += 1

    def run(self):
        while True:
            if self.current_position > -1:
                title = self.queue[self.current_position]
                self.current_position -= 1
                if localCache.get(title) is not None:
                    continue
                try:
                    films = movieSearch.search_1(title)
                except KeyError:
                    films = None
                data = []
                if films is not None:
                    for film in films:
                        data.append(film.toJson())
                localCache.add(title, data)
            else:
                sleep(1)