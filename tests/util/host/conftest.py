from collections import namedtuple
from subprocess import PIPE, run

from pytest import fixture


@fixture(scope="session")
def hostname():

    def retrieve(*cmdlines):
        for cmdline in cmdlines:
            cmd = run(cmdline, stdout=PIPE, universal_newlines=True)
            if cmd.stdout:
                return cmd.stdout.strip()
        return ''

    name = retrieve(
        ['hostname'],
        ['uname', '-n']
    )

    yield namedtuple('HostName', ('long', 'short'))(
        long=name, short=name.split('.')[0]
    )
