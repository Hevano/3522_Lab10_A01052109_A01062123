import time
from threading import Lock
from threading import Thread

from city_processor import CityDatabase
from city_processor import CityOverheadTimes
from city_processor import ISSDataRequest


class CityOverHeadTimeQueue:
    def __init__(self):
        self.data_queue = []
        self.access_queue_lock = Lock()

    def put(self, overhead_time: CityOverheadTimes) -> None:
        with self.access_queue_lock:
            self.data_queue.append(overhead_time)
            print(f"Element added to queue. Queue has {len(self.data_queue)} items.")

    def get(self) -> CityOverheadTimes:
        with self.access_queue_lock:
            if len(self.data_queue) <= 0:
                print("Queue is empty: sleeping")
                time.sleep(1)
            t = self.data_queue[0]
            del self.data_queue[0]
            print(f"Element removed from queue. Queue has {len(self.data_queue)} items.")
            return t

    def __len__(self) -> int:
        return len(self.data_queue)


class ProducerThread(Thread):
    def __init__(self, cities: list, queue: CityOverHeadTimeQueue):
        super().__init__()
        self.cities = cities
        self.queue = queue

    def run(self) -> None:
        counter = 0
        for city in self.cities:
            counter += 1
            if len(self.queue) == 5:
                time.sleep(1)
                counter = 0
            overhead = ISSDataRequest.get_overhead_pass(city)
            self.queue.put(overhead)


class ConsumerThread(Thread):
    def __init__(self, queue: CityOverHeadTimeQueue):
        super().__init__()
        self.queue = queue
        self.data_incoming = True

    def run(self) -> None:
        while self.data_incoming or len(self.queue) > 0:
            print(self.queue.get())
            time.sleep(0.5)
            if len(self.queue) <= 0:
                time.sleep(0.75)


db = CityDatabase("city_locations.xlsx")

q = CityOverHeadTimeQueue()
p_thread = ProducerThread(db.city_db[0:50], q)
p_thread2 = ProducerThread(db.city_db[51:101], q)
p_thread3 = ProducerThread(db.city_db[102:152], q)

c_thread = ConsumerThread(p_thread.queue)

p_thread.start()
p_thread2.start()
p_thread3.start()
time.sleep(0.1)
c_thread.start()

p_thread.join()
p_thread2.join()
p_thread3.join()
c_thread.data_incoming = False
