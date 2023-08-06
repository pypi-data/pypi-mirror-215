from dataclasses import dataclass
from typing import Optional

from ..exceptions import NotADzObject
from ..naming import MAIN_MODULE_NAME, META_MODULE_NAME, from_mod_name


@dataclass
class CompleteId:
    """bedrock id with a namespace prefix

    namespace/project None means local id
    """

    project: Optional[str]
    namespace: Optional[str]
    obj_id: str

    @property
    def sql_id(self):
        return "__".join([self.project, self.namespace, self.obj_id]).replace("-", "_")


@dataclass
class CompleteIdBase:
    project: Optional[str] = None
    namespace: Optional[str] = None

    def __eq__(self, __o: object) -> bool:
        return self.__hash__() == __o.__hash__()

    def __hash__(self) -> int:
        return (self.project, self.namespace).__hash__()

    def to_id(self, name) -> CompleteId:
        return CompleteId(self.project, self.namespace, name)

    @classmethod
    def from_cls(cls, py_cls, project=None):
        _mod = py_cls.__module__
        return cls.from_module_name(_mod, project)

    @classmethod
    def from_module_name(cls, module_name, project=None):
        _splitted = module_name.split(".")
        if _splitted[0] == META_MODULE_NAME:
            return cls(from_mod_name(_splitted[1]), _splitted[2])
        elif (_splitted[0] == MAIN_MODULE_NAME) and (len(_splitted) > 1):
            return cls(project, _splitted[1])
        raise NotADzObject(module_name)
