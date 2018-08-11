from git_sh_sync.util.host import get_hostname


def test_get_hostname_long(hostname):
    name = get_hostname(short=False)
    assert name == hostname.long


def test_get_hostname_short(hostname):
    name = get_hostname(short=True)
    assert name == hostname.short
