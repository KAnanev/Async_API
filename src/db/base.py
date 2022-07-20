from abc import abstractmethod, ABC


class AsyncStorage(ABC):
    @abstractmethod
    async def get(self, _index: str, object_id: str, **kwargs):
        pass

    @abstractmethod
    async def search(self, _index: str, data, **kwargs):
        pass


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int, **kwargs):
        pass
