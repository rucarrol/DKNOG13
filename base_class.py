import abc


class BaseClass(abc.ABC):
    @abc.abstractmethod
    def isUserConfigured(username: str) -> bool:
        pass

    @abc.abstractmethod
    def fetchModel() -> str:
        pass

    @abc.abstractmethod
    def fetchRunningVersion() -> dict:
        pass

    @abc.abstractmethod
    def fetchARPTable() -> list[dict]:
        pass

    @abc.abstractmethod
    def fetchISISAdjacency() -> list[dict]:
        pass

