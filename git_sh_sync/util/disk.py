'''
This modules handles disk operations.
Namely combining paths, checking them and creating folders..
'''

from logging import getLogger
from os import makedirs, path

LOG = getLogger(__name__)


def joined(*locs):
    '''
    Joins paths together.

    :param locs:
        Single path elements to :py:func:`join <os.path.join>` together.

    :returns:
        A full path combined by the following rules:

    * Leading :py:data:`slashes <os.sep>` are stripped from all
      but the first element
    * :py:func:`Expanduser <os.path.expanduser>` is applied (``~``)
    * :py:func:`Expandvars <os.path.expandvars>` is applied
      (e.g. ``$HOME`` is then the same as ``~``)
    * Finally :py:func:`realpath <os.path.realpath>` is applied
      to resolve symlinks and return a full path
    '''

    return path.realpath(path.expandvars(path.expanduser(path.join(*(
        (loc.lstrip(path.sep) if num != 0 else loc)
        for num, loc in enumerate(locs)
    )))))


def spare(*locs, folder=False):
    '''
    Checks if a path is not already occupied

    :param locs: Input Parameter for :func:`joined`
    :param folder: Flag to signal if to check for a file or folder
    :returns:
        ``True``, ``False`` or ``None`` by the following rules:

    * If a folder is present and *folder* = ``True``: ``False``
    * If a folder is present and *folder* = ``False``: ``None``
    * If a file is present and *folder* = ``False``: ``False``
    * If a file is present and *folder* = ``True``: ``None``
    * If nothing is present: ``True``
    '''
    location = joined(*locs)
    if path.exists(location):
        if folder and path.isdir(location):
            return False
        if not folder and path.isfile(location):
            return False
        return None
    return True


def ensured(*locs, folder=False):
    '''
    Checks if the path already exists and creates (parent-)folders
    if necessary

    :param locs: Input Parameter for :func:`spare`
    :param folder: Treat *locs* Parameter as file or folder
    :returns:
        Output of :func:`joined`
    '''

    location = joined(*locs)
    src_loc = location if folder else path.dirname(location)
    if spare(src_loc, folder=True):
        LOG.info('creating folder: "%s"', src_loc)
        makedirs(src_loc)
    return location
