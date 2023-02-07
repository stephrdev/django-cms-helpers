import importlib.metadata as importlib_metadata


try:
    __version__ = importlib_metadata.version('django-cms-helpers')
except Exception:
    __version__ = 'HEAD'
