from __future__ import annotations
import os
import sys
from configparser import ConfigParser, _UNSET
from pathlib import Path


def get_config(pathpart: str = None, *, local: str|Path|list[str|Path] = 'local.conf', default: str|Path|list[str|Path] = None) -> ExtendedConfigParser:
    files = get_config_files(pathpart, local=local, default=default)
    
    parser = ExtendedConfigParser()
    parser.read(files, encoding='utf-8')
    return parser


def get_config_files(pathpart: str = None, *, local: str|Path|list[str|Path] = 'local.conf', default: str|Path|list[str|Path] = None, only_existing: bool = False) -> list[str]:
    files = []

    # Add default file(s)
    if default:
        if not isinstance(default, (list,tuple)):
            default = [default]

        for path in default:
            if not isinstance(path, Path):
                path = Path(path)
            path = path.expanduser()
            if not only_existing or os.path.exists(path):
                files.append(path)

    # Add system and user files
    if pathpart:
        if not pathpart.endswith('.conf'):
            pathpart = f'{pathpart}.conf'

        # Add system file
        path = Path(f'C:/ProgramData/{pathpart}' if sys.platform == 'win32' else f'/etc/{pathpart}').expanduser()
        if not only_existing or os.path.exists(path):
            files.append(path)
        
        # Add user file
        path = Path(f'~/.config/{pathpart}').expanduser()        
        if not only_existing or os.path.exists(path):
            files.append(path)

    # Add local file(s)
    if local:
        if not isinstance(local, (list,tuple)):
            local = [local]

        for path in local:
            if not isinstance(path, Path):
                path = Path(path)
            path = path.expanduser()
            if not only_existing or os.path.exists(path):
                files.append(path)

    return files


class ExtendedConfigParser(ConfigParser):
    def getlist(self, section: str, option: str, *, fallback: list[str]|None = _UNSET, separator: str = ',') -> list[str]:
        try:            
            values_str = self.get(section, option)
        except:
            if fallback != _UNSET:
                return fallback
            raise

        values = []
        for value in values_str.split(separator):
            value = value.strip()
            if not value:
                continue
            values.append(value)

        return values
