from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def get_all_news(self):
        pass
