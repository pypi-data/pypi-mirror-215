"""Represent (Finnish: edustaa) markdown text parts as a whole in markdown, html, pdf, and troff format guided by conventions."""
# [[[fill git_describe()]]]
__version__ = '2023.6.24+parent.80fb84ab'
# [[[end]]] (checksum: 657a0f8517c2674267a2ffdbd93aa4bb)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)

APP_NAME = 'Represent (Finnish: edustaa) markdown text parts as a whole in markdown, html, pdf, and troff format guided by conventions.'
APP_ALIAS = 'edustoa'
APP_ENV = APP_ALIAS.upper()
VERSION = __version__
VERSION_INFO = __version_info__

__all__ = [
    'APP_ALIAS',
    'APP_ENV',
    'APP_NAME',
    'VERSION',
    'VERSION_INFO',
]
