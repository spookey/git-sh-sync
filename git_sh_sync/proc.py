from collections import namedtuple
from logging import getLogger
from pprint import pformat
from shlex import split
from subprocess import PIPE, Popen

LOG = getLogger(__name__)

ResCommand = namedtuple('command', (
    'cmd', 'cwd', 'cin', 'exc', 'code',
    'out', 'stdout', 'err', 'stderr'
))


def command(cmd, *, cwd=None, cin=None):
    out, err, stdout, stderr = [], [], '', ''
    exc, code = None, None

    if isinstance(cmd, str):
        cmd = split(cmd)

    LOG.debug('launching command "%s" (in "%s")', ' '.join(cmd), cwd)

    try:
        proc = Popen(
            cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE,
            cwd=cwd, universal_newlines=True
        )
    except(OSError, TypeError, ValueError) as ex:
        exc = ex
    else:
        stdout, stderr = proc.communicate(input=cin)
        code = proc.returncode
        stdout = stdout.strip()
        stderr = stderr.strip()
        out = stdout.splitlines()
        err = stderr.splitlines()

    details = pformat(dict(
        cmd=' '.join(cmd), cwd=cwd, cin=cin,
        out=out, err=err, exc=exc, code=code
    ))

    if code == 0:
        LOG.info('command success: """%s"""', details)
    else:
        LOG.error('command failed: """%s"""', details)

    return ResCommand(
        cmd=cmd, cwd=cwd, cin=cin, exc=exc, code=code,
        out=out, stdout=stdout, err=err, stderr=stderr,
    )
