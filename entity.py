from abc import ABC, abstractmethod


class Entity(ABC):
    @abstractmethod
    def reduce(self, action):
        pass
