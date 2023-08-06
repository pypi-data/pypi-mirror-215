import logging
from typing import Any, Dict, Optional, Tuple, Type, TypeVar
from pydantic import BaseSettings, create_model, PrivateAttr, BaseModel
from pydantic.env_settings import SettingsSourceCallable
import tomlkit
from pathlib import Path

class TemplateMeta(type(BaseSettings)):

    def __init__(self, name, bases, *args, **kwargs) -> None:
        super().__init__(name, bases, *args, **kwargs)
        # if len(bases) > 1:
        #     raise TypeError("Multiple inheritance not supported")
        if name == "TemplateConfig":
            self._env_fields: list[str] = []
            self._file_fields: list[str] = []
            self._extra_env = False
            self._extra_file = False
        else:
            b = bases[0]
            self._env_fields = self._env_fields.copy()
            self._file_fields = self._file_fields.copy()
            if any(b._extra_env for b in bases):
                self._env_fields += [
                    k for k in self.__fields__.keys() if k not in
                    [f for b in bases for f in b.__fields__.keys()] 
                ]
                self._extra_env = False
            if any(b._extra_file for b in bases):
                self._file_fields += [
                    k for k in self.__fields__.keys() if k not in
                    [f for b in bases for f in b.__fields__.keys()] 
                ]
                self._extra_file = False

class TemplateConfig(BaseSettings, metaclass=TemplateMeta):
    
    def to_toml(self, config_file=None):
        config_file = config_file or self.__config__.config_file
        Path(config_file).touch(exist_ok=True)
        with open(config_file, 'w') as f:
            tomlkit.dump(self.file_dict(), f)

    def file_dict(self) -> Dict[str, Any]:
        file_dict = {}
        fs = {k: v for k, v in self if k in self._file_fields}
        for k, v in fs.items(): 
            # add submodels
            if isinstance(v, TemplateConfig):
                file_dict[k] = v.file_dict()
            elif isinstance(v, BaseModel):
                file_dict[k] = v.dict()
            else:
                file_dict[k] = v
        return file_dict

    def to_dotenv(self, env_file=None):
        env_file = env_file or self.__config__.env_file
        if self._env_fields:
            with open(env_file, 'w') as f:
                f.writelines(f"{k}={v}\n" for k,v in self.env_dict().items())

    def env_dict(self, prefix="") -> Dict[str, str]:
        env_name = lambda f: (prefix + next(
            n for n in
            self.__fields__[f].field_info.extra['env_names']
        )).upper()
        env_dict = {}
        # add submodels
        for k, v in self: 
            if isinstance(v, TemplateConfig):
                p = k+self.__config__.env_nested_delimiter
                env_dict.update(v.env_dict(prefix=p))
            elif k in self._env_fields:
                if isinstance(v, BaseModel):
                    env_dict[env_name(k)] = v.json()
                else:
                    env_dict[env_name(k)] = v
        return env_dict

    class Config:
        env_nested_delimiter = '__' # cannot use it in naming the fields
        config_file_type = 'toml'
        config_file: Optional[str] = None

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            file_settings = {
                'toml': toml_settings,
            }[cls.config_file_type]
            return init_settings, env_settings, file_secret_settings, file_settings,

def toml_settings(settings: TemplateConfig) -> Dict[str, Any]:
    if not settings.__config__.config_file:
        return {}
    path = Path(settings.__config__.config_file)
    if path.exists():
        with open(path, 'r') as f:
            conf_dict = tomlkit.load(f).value
        return conf_dict
    else:
        return {}

class FileConfig(TemplateConfig):
    _extra_file = True

class EnvConfig(TemplateConfig):
    _extra_env = True

T = TypeVar("T")

def extra_env(base: Type[T]) -> Type[T]:
    class ExtraEnv(base):
        _extra_env = True

    return ExtraEnv

