import inspect
import io
import json
import os
import pathlib
import shutil
import sys
import tempfile
import textwrap
import typing
import zipfile

import configloaders

from . import encode
from .__boot import get_bytes as get_boot_bytes
from .utils import *


class Config:
    class pointcut:
        before: str | None = None
        around: str | None = None
        after: str | None = None


class PEInjecter:
    def __init__(self):
        self.config = configloaders.load({}, Config)
        self.boot_bytes = get_boot_bytes()
        self.resources_bytesio = io.BytesIO()
        self.resources_zip = zipfile.ZipFile(self.resources_bytesio, 'w')

    def add_resource(self, file: str | pathlib.Path, filename: str | pathlib.Path | None = None):
        file = pathlib.Path(file)
        if file.name == 'config.json':
            with open(file) as f: self.config = json.load(f)
        self.resources_zip.write(file, arcname=filename)

    def add_resources(self, file: str | pathlib.Path, dirname: str | pathlib.Path | None = None):
        file = pathlib.Path(file)
        files = []
        for f in file.glob('**/*'):
            files.append(f)
        for file in files:
            self.add_resource(file.relative_to(dirname))

    def header(self, config: dict | Config = {}, **kwargs) -> bytes:
        configloaders.load(self.config, config, {'pointcut': kwargs})
        self.resources_zip.close()
        self.resources_bytes = self.resources_bytesio.getvalue()
        self.config_bytes = json.dumps(self.config).encode('utf-8')
        return encode(self.boot_bytes, self.resources_bytes[::-1], self.config_bytes[::-1])

    def inject(self, target: str | io.TextIOWrapper, output: str | io.TextIOWrapper, config: dict | Config = {}, **kwargs) -> None:
        if isinstance(target, str): target = open(target, 'rb')
        if isinstance(output, str): output = open(output, 'wb')
        target_bytes = target.read()
        target.close()
        output.write(self.header(config, **kwargs) + encode(target_bytes.read()[::-1]))
        output.close()


def inject(target: str | io.TextIOWrapper,
           output: str | io.TextIOWrapper | None = None,
           before: typing.Callable[[], None] | None = None,
           around: typing.Callable[[], None] | None = None,
           after: typing.Callable[[], None] | None = None):
    output = output or target
    config = {'before': before, 'around': around, 'after': after}

    if not getattr(sys, 'frozen', False): build(before=before, around=around, after=after)

    if isinstance(target, str):
        with open(target, 'rb') as file: target_bytes = file.read()
    else: target_bytes = target.read()

    injecter = PEInjecter()
    root = pathlib.Path(getattr(sys, '_MEIPASS')) if hasattr(sys, '_MEIPASS') else pathlib.Path('./dist')
    for name in ['before', 'around', 'after']:
        pointcut = config[name]
        if pointcut is not None:
            if inspect.isfunction(pointcut):
                pointcut = glob_ex(f'{root.as_posix()}/{pointcut.__name__}*', lambda f: injecter.add_resource(f, pathlib.Path(f).name))[0]
            elif isinstance(pointcut, str):
                if pointcut.endswith('.py'):
                    pointcut = pathlib.Path(pointcut).with_suffix('').name
                pointcut = glob_ex(f'{root.as_posix()}/{pointcut}*', lambda f: injecter.add_resource(f, pathlib.Path(f).name))[0]
            else: raise TypeError()
            config[name] = pathlib.Path(pointcut).name
    header_bytes = injecter.header({'pointcut': config})

    if isinstance(output, str):
        with open(output, 'wb') as file: file.write(header_bytes + encode(target_bytes[::-1]))
    else: output.write(header_bytes + encode(target_bytes[::-1]))


def build(name: str | None = None,
          args: str = '-F -w --uac-admin',
          before: typing.Callable[[], None] | None = None,
          around: typing.Callable[[], None] | None = None,
          after: typing.Callable[[], None] | None = None):
    main = pathlib.Path(sys.argv[0])
    main_name = name or main.with_suffix('').name
    config = {'before': before, 'around': around, 'after': after}

    tmpdir = tempfile.TemporaryDirectory()
    root = pathlib.Path('./dist')
    for name in ['before', 'around', 'after']:
        pointcut = config[name]
        if pointcut is not None:
            if inspect.isfunction(pointcut):
                tfile = f'__peinjecter_{pointcut.__name__}.py'
                with open(tfile, 'w') as file:
                    file.write(textwrap.dedent(f'''
                        import {main_name}
                        if __name__ == '__main__': {main_name}.{pointcut.__name__}()
                    '''[1:]))
                os.system(f'pyinstaller {tfile} -n {pointcut.__name__} {args}')
                os.remove(tfile)
                glob_ex(f'{root.as_posix()}/{pointcut.__name__}*', lambda f: shutil.copy(f, tmpdir.name))
            elif isinstance(pointcut, str):
                if pointcut.endswith('.py'):
                    pname = pathlib.Path(pointcut).with_suffix('').name
                    os.system(f'pyinstaller {pointcut} -n {pname} {args}')
                    glob_ex(f'{root.as_posix()}/{pname}*', lambda f: shutil.copy(f, tmpdir.name))
                else:
                    shutil.copy(pointcut, tmpdir.name)
            else: raise TypeError()

    shutil.rmtree('build', True)
    os.system(f'pyinstaller {sys.argv[0]} -n {main_name} --add-data \"{pathlib.Path(tmpdir.name).as_posix()}/*;.\" {args}')
    tmpdir.cleanup()
