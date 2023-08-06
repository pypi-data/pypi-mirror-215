import re
from abc import ABCMeta
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Type, TypeVar, Union

import yaml
from parquetranger import TableRepo
from structlog import get_logger
from zimmauth import ZimmAuth

from .dvc_util import get_default_remote
from .exceptions import ProjectSetupException
from .metadata.complete_id import CompleteId
from .naming import (
    AUTH_HEX_ENV_VAR,
    AUTH_PASS_ENV_VAR,
    BASE_CONF_PATH,
    DEFAULT_ENV_NAME,
    DEFAULT_REGISTRY,
    RUN_CONF_PATH,
    USER_CONF_PATH,
    get_data_path,
)

if TYPE_CHECKING:
    from .persistent_state import PersistentState

logger = get_logger(ctx="config loading")


T = TypeVar("T")


@dataclass
class ProjectEnv:
    name: str = DEFAULT_ENV_NAME
    remote: Optional[str] = None
    parent: Optional[str] = None
    params: dict = field(default_factory=dict)
    import_envs: dict = field(default_factory=dict)

    @property
    def true_remote(self):
        return self.remote or get_default_remote()


@dataclass
class ImportedProject:
    name: str
    data_namespaces: list = None
    version: str = ""


@dataclass
class AswanSpec:
    name: str
    current_leaf: Optional[str] = None


@dataclass
class Config:
    name: str
    version: str
    cron: str = ""
    default_env: str = None
    registry: str = DEFAULT_REGISTRY
    envs: list[ProjectEnv] = None
    imported_projects: list[ImportedProject] = field(default_factory=list)
    aswan_projects: list[AswanSpec] = field(default_factory=list)
    persistent_states: dict[str, dict] = field(default_factory=dict)

    def __post_init__(self):
        if not self.envs:
            self.envs = [ProjectEnv()]
        if self.default_env is None:
            self.default_env = self.envs[0].name
        _parse_version(self.version)
        msg = f"name can only contain lower case letters or -. {self.name}"
        assert re.compile(r"^[a-z\-]+$").findall(self.name), msg
        self.version = self.version[1:]

    def get_env(self, env_name: str) -> ProjectEnv:
        return _get(self.envs, env_name)

    def get_import(self, project_name: str) -> ImportedProject:
        return _get(self.imported_projects, project_name)

    def get_aswan_spec(self, name: str) -> AswanSpec:
        try:
            return _get(self.aswan_projects, name)
        except KeyError:
            self.aswan_projects.append(AswanSpec(name))
            return _get(self.aswan_projects, name)

    def create_trepo(
        self, id_: CompleteId, partitioning_cols=None, max_partition_size=None
    ):
        envs_of_ns = self.get_data_envs(id_.project, id_.namespace)
        if not envs_of_ns:
            return UnavailableTrepo()
        default_env = self.resolve_ns_env(id_.project, self.default_env)
        parents_dict = {
            env: get_data_path(id_.project, id_.namespace, env) for env in envs_of_ns
        }
        main_path = parents_dict[default_env] / id_.obj_id
        return TableRepo(
            main_path,
            group_cols=partitioning_cols,
            max_records=max_partition_size or 0,
            env_parents=parents_dict,
            drop_group_cols=True,
        )

    def get_data_envs(self, project, ns):
        if project == self.name:
            return [e.name for e in self.envs]
        for iaf in self.imported_projects:
            if iaf.name == project:
                dnss = iaf.data_namespaces
                if dnss and (ns not in dnss):
                    return []
        data_envs = [e.import_envs.get(project) for e in self.envs]
        return set(filter(None, data_envs))

    def get_data_env(self, env_name, data_project):
        env = self.get_env(env_name)
        data_env = env.import_envs.get(data_project)
        return data_env or self.get_data_env(env.parent, data_project)

    def resolve_ns_env(self, project, env):
        if project == self.name:
            return env
        return self.get_data_env(env, project)

    def dump_persistent_state(self, state: "PersistentState"):
        self.persistent_states[state.get_full_name()] = asdict(state)
        self._update_raw({CONF_KEYS.persistent_states: self.persistent_states})

    def update_aswan_spec(self, project_name, new_state):
        logger.info("global aswan", name=project_name, latest=new_state)
        self.get_aswan_spec(project_name).current_leaf = new_state
        raw_specs = {d.pop("name"): d for d in map(asdict, self.aswan_projects)}
        self._update_raw({CONF_KEYS.aswan_projects: raw_specs})

    def dump(self):
        d = asdict(self)
        for k in _DC_ATTRIBUTES.keys():
            d[k] = {e.pop("name"): e for e in d[k]}
        d[CONF_KEYS.version] = f"v{d[CONF_KEYS.version]}"
        BASE_CONF_PATH.write_text(yaml.safe_dump(d))

    @classmethod
    def load(cls):
        dic = cls._load_raw()
        ldic = {k: _to_list(dic.pop(k, {}), v) for k, v in _DC_ATTRIBUTES.items()}
        return cls(**dic, **ldic)

    @property
    def sorted_envs(self):
        _remote = self.get_env(self.default_env).true_remote
        return sorted(
            self.envs, key=lambda env: (env.true_remote == _remote, env.true_remote)
        )

    @property
    def env_names(self):
        return [e.name for e in self.envs]

    def _update_raw(self, dic: dict):
        BASE_CONF_PATH.write_text(yaml.dump(self._load_raw() | dic, sort_keys=False))

    @classmethod
    def _load_raw(cls):
        return _yaml_or_err(BASE_CONF_PATH)


_DC_ATTRIBUTES = {  # what attributes of config need parsing as dataclasses
    k: v.__args__[0]
    for k, v in Config.__annotations__.items()
    if (list in v.mro()) and isinstance(getattr(v, "__args__", [None])[0], type)
}


class _IoConf:
    def dump(self):
        self._cpath().write_text(yaml.safe_dump(asdict(self)))

    @classmethod
    def load(cls):
        return cls(**_yaml_or_err(cls._cpath(), cls.__name__))

    @classmethod
    def _cpath(cls) -> Path:
        return ...


@dataclass
class RunConfig(_IoConf):
    profile: bool = False
    write_env: Optional[str] = None
    read_env: Optional[str] = None
    reset_aswan: bool = False

    def __enter__(self):
        self.dump()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cpath().unlink()

    @classmethod
    def _cpath(cls):
        return RUN_CONF_PATH


@dataclass
class UserConfig(_IoConf):
    first_name: str
    last_name: str
    orcid: str

    @classmethod
    def _cpath(cls):
        return USER_CONF_PATH


class UnavailableTrepo(TableRepo):
    def __init__(self):
        pass


class KeyMeta(ABCMeta):
    def __getattribute__(cls, attid: str):
        if attid.startswith("_"):
            return super().__getattribute__(attid)
        return attid


class CONF_KEYS(Config, metaclass=KeyMeta):
    pass


class SPEC_KEYS(AswanSpec, metaclass=KeyMeta):
    pass


class ENV_KEYS(ProjectEnv, metaclass=KeyMeta):
    pass


def get_full_auth():
    return ZimmAuth.from_env(AUTH_HEX_ENV_VAR, AUTH_PASS_ENV_VAR)


def get_aswan_leaf_param_id(project_name):
    return ".".join([CONF_KEYS.aswan_projects, project_name, SPEC_KEYS.current_leaf])


def _to_list(entities: Union[dict, list], cls: Type[T], key_name="name") -> list[T]:
    if isinstance(entities, list):
        entities = {k: {} for k in entities}
    return [cls(**{key_name: k, **kwargs}) for k, kwargs in entities.items()]


def _parse_version(v: str):
    assert v[0] == "v", f"version must start with v, but is {v}"
    return tuple(map(int, v[1:].split(".")))


def _yaml_or_err(path, desc=None):
    try:
        return yaml.safe_load(path.read_text()) or {}
    except FileNotFoundError as e:
        msg = f"Config of {desc or path} not found in {e}"
        raise ProjectSetupException(msg)


def _get(obj_l, key):
    for obj in obj_l:
        if obj.name == key:
            return obj
    raise KeyError(key)
