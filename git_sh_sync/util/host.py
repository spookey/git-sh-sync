'''
This module handles host operations.
Namely getting the hostname of the local machine...
'''

from socket import gethostname


def get_hostname(short=True):
    '''
    Retrieves current hostname.

    :param short: only emit the first part if ``true``
    :returns: hostname (long or short form)
    '''

    name = gethostname()
    if short:
        name = name.split('.')[0]
    return name
