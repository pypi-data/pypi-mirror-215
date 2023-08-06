import abc


class LLModel(abc.ABC):

    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> str:
        pass
