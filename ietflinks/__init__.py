from collections import abc
from importlib import metadata

version = metadata.version('pymdown-ietflinks')
version_info: abc.MutableSequence[int | str] = []
version_info.extend(int(c) for c in version.split('.')[:3])
version_info.extend(version.split('.')[3:])
del abc, metadata

__version__ = version
