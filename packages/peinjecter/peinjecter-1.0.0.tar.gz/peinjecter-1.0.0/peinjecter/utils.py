import glob
import pathlib


def glob_ex(pattern: str, callback=lambda file: None, _filter=lambda x: not pathlib.Path(x).is_dir(), _n=1, _recursive=False):
    result = []
    for _, file in zip(range(_n), list(filter(_filter, glob.glob(pattern, recursive=_recursive)))):
        callback(file)
        result.append(file)
    return result
