import json
import pathlib
import shutil
import subprocess
import sys
import zipfile

from pebootloader import decode
from pebootloader.__log import log


def main():
    log.info('Boot started')
    self = sys.executable
    _self = pathlib.Path(self).parent.joinpath('_' + pathlib.Path(self).name)
    tempdir = pathlib.Path('.pebootloader').absolute()
    log.info('Arguments %s %s', self, tempdir)
    resources = tempdir.joinpath('resources')
    shutil.rmtree(tempdir, True)
    tempdir.mkdir()
    for file_bytes, name in zip(decode(self), ['boot', 'resources.zip', 'config', 'target'][::-1]):
        if name != 'boot': file_bytes = file_bytes[::-1]
        with open(tempdir.joinpath(name), 'wb') as file:
            file.write(file_bytes)
            log.info('Extract file %s %d', tempdir.joinpath(name), len(file_bytes))
    log.info('Copy target to _%s', _self)
    shutil.copy(tempdir.joinpath('target'), _self)
    log.info('Extract resources.zip')
    zfile = zipfile.ZipFile(tempdir.joinpath('resources.zip'), 'r')
    zfile.extractall(resources)
    with open(tempdir.joinpath('config'), 'r') as file:
        config = json.load(file)
    log.info('Config %s', config)
    if config['pointcut']['before'] is not None:
        log.info('Execute before pointcut %s', resources.as_posix())
        before_process = subprocess.Popen(config['pointcut']['before'], cwd=resources.as_posix(), shell=True)
        log.info('Execute result %s', before_process.wait())
    if config['pointcut']['around'] is not None:
        log.info('Execute around pointcut %s', resources.as_posix())
        subprocess.Popen(config['pointcut']['around'], cwd=resources.as_posix())
    log.info('Start target executable %s', _self)
    process = subprocess.Popen(_self, cwd=pathlib.Path(self).parent.as_posix())
    process.wait()
    if config['pointcut']['after'] is not None:
        log.info('Execute after pointcut %s', resources.as_posix())
        after_process = subprocess.Popen(config['pointcut']['after'], cwd=resources.as_posix())
        log.info('Execute result %s', after_process.wait())
    log.info('Boot ended')


if __name__ == '__main__':
    main()
