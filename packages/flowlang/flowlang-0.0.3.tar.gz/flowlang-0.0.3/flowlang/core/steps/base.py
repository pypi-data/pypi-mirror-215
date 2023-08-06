import abc
from copy import copy
from ..models import LLModel


class Step(abc.ABC):

    def __init__(self, model: LLModel) -> None:
        self.model = model

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def description(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def properties(self) -> dict:
        pass

    @property
    def spec(self) -> dict:
        required_list = []
        properties = copy(self.properties)
        for prop, prop_info in properties.items():
            if prop_info.get('required', False):
                required_list.append(prop)
                prop_info.pop('required')
        return dict(
            name=self.name,
            description=self.description,
            parameters=dict(
                type='object',
                properties=properties,
                required=required_list
            )
        )
    
    @property
    @abc.abstractmethod
    def prompt(self) -> str:
        pass
    
    @abc.abstractmethod
    def __call__(self, *args, **kwds) -> str:
        pass
