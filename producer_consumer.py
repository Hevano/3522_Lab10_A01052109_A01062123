import city_processor

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