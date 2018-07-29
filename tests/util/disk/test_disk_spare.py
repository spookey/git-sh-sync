from git_sh_sync.util.disk import spare


def test_spare_nothing(tmpdir):
    thing = tmpdir.join('thing')
    assert spare(str(thing), folder=False) is True
    assert spare(str(thing), folder=True) is True


def test_spare_on_file(tmpdir):
    file = tmpdir.ensure('file')
    assert spare(str(file), folder=False) is False
    assert tmpdir.remove(file) is None


def test_spare_not_on_file(tmpdir):
    file = tmpdir.ensure('file')
    assert spare(str(file), folder=True) is None
    assert tmpdir.remove(file) is None


def test_spare_on_folder(tmpdir):
    folder = tmpdir.mkdir('folder')
    assert spare(str(folder), folder=True) is False
    assert tmpdir.remove(folder) is None


def test_spare_not_on_folder(tmpdir):
    folder = tmpdir.mkdir('folder')
    assert spare(str(folder), folder=False) is None
    assert tmpdir.remove(folder) is None
