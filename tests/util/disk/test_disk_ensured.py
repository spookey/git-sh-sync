from logging import INFO

from git_sh_sync.util.disk import ensured


def test_ensured_folder(tmpdir):
    folder = tmpdir.join('folder')
    assert folder.stat(raising=False) is None

    assert ensured(str(folder), folder=True) == folder

    assert folder.stat(raising=False) is not None
    assert folder.remove() is None


def test_ensured_file(tmpdir):
    folder = tmpdir.join('folder')
    file = folder.join('file')
    assert folder.stat(raising=False) is None
    assert file.stat(raising=False) is None

    assert ensured(str(file), folder=False) == file

    assert folder.stat(raising=False) is not None
    assert file.stat(raising=False) is None
    assert folder.remove() is None


def test_ensured_logging(caplog, tmpdir):
    caplog.set_level(INFO)
    folder = tmpdir.join('folder')
    file = folder.join('file')

    assert ensured(str(file), folder=False) == file

    assert folder.remove() is None

    assert len(caplog.records) == 1
    rec = caplog.records[-1]
    assert rec.levelno == INFO
    assert 'creating folder: "%s"' in rec.msg
    assert str(folder) in rec.args[-1]
