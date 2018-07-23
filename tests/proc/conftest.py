from collections import namedtuple

from pytest import fixture

from git_sh_sync.proc import Command


@fixture
def helpcmd():
    def init(cmd, **kwargs):
        return Command(cmd, **kwargs)

    def edit(obj, **kwargs):
        data = getattr(obj, '_data', {})
        for key, val in kwargs.items():
            data[key] = val
        setattr(obj, '_data', data)

    def fields(obj):
        return getattr(obj, '_fields', None)

    yield namedtuple('helpcmd', ('init', 'edit', 'fields'))(
        init=init,
        edit=edit,
        fields=fields
    )
