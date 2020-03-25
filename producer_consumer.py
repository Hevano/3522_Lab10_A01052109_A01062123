import city_processor
from threading import Thread

class CityOverHeadTimeQueue:
    def __init__(self):
        self.data_queue = []

    def put(self, overhead_time: city_processor.CityOverheadTimes) -> None:
        self.data_queue.append(overhead_time)

    def get(self) -> city_processor.CityOverheadTimes:
        t = self.data_queue[0]
        del self.data_queue[0]
        return t

    def __len__(self) -> int:
        return len(self.data_queue)


class ProducerThread(Thread):
    def __init__(self, cities: list, queue: CityOverHeadTimeQueue):
        self.cities = cities
        self.queue = queue

    def run(self) -> None:
        for i in range(5):
            if len(self.cities) > 0:
                self.queue.add(city_processor.ISSDataRequest.get_overhead_pass(self.cities[len(self.cities) - 1]))
                del self.cities[len(self.cities) - 1]
        self.sleep()


db = city_processor.CityDatabase("city_locations_test.xlsx")
thread = ProducerThread(db.city_db[0], CityOverHeadTimeQueue())
thread.start()
thread.join()
print(len(thread.queue))
