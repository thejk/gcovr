import os
import pytest
import shutil
import tempfile

from ..ignore import ignore_file


@pytest.fixture
def workdir():
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


class Options(object):
    def __init__(self, root_dir):
        self.verbose = True
        self.root_dir = root_dir


#
# Create an empty file
#
def touch(filename):
    with open(filename, 'w') as f:
        f.write('\n')


#
# Create an ignore file in directory with list of rules
#
def ignore(path, rules):
    with open(os.path.join(path, '.gcovrignore'), 'w') as f:
        for rule in rules:
            f.write('%s\n' % rule)
        f.write('\n')


def test_no_files(workdir):
    touch(os.path.join(workdir, 'test.cc'))
    assert not ignore_file('test.cc', Options(workdir))


def test_no_files_relative(workdir):
    os.makedirs(os.path.join(workdir, 'build'))
    os.makedirs(os.path.join(workdir, 'src'))
    touch(os.path.join(workdir, 'src/test.cc'))
    assert not ignore_file('../src/test.cc',
                           Options(os.path.join(workdir, 'build')))


def test_ignore_samedir(workdir):
    touch(os.path.join(workdir, 'test.cc'))
    ignore(workdir, ['test.cc'])
    assert ignore_file('test.cc', Options(workdir))


def test_ignore_samedir_no_match(workdir):
    touch(os.path.join(workdir, 'test.cc'))
    ignore(workdir, ['foobar'])
    assert not ignore_file('test.cc', Options(workdir))


def test_ignore_relative_subdir(workdir):
    os.makedirs(os.path.join(workdir, 'build'))
    os.makedirs(os.path.join(workdir, 'src'))
    touch(os.path.join(workdir, 'src/test.cc'))
    ignore(workdir, ['src/'])
    assert ignore_file('../src/test.cc',
                       Options(os.path.join(workdir, 'build')))


def test_ignore_relative_file(workdir):
    os.makedirs(os.path.join(workdir, 'build'))
    os.makedirs(os.path.join(workdir, 'src'))
    touch(os.path.join(workdir, 'src/test.cc'))
    ignore(os.path.join(workdir, 'src'), ['test.cc'])
    assert ignore_file('../src/test.cc',
                       Options(os.path.join(workdir, 'build')))


def test_ignore_relative_file_relative_rule(workdir):
    os.makedirs(os.path.join(workdir, 'build'))
    os.makedirs(os.path.join(workdir, 'src'))
    touch(os.path.join(workdir, 'src/test.cc'))
    ignore(workdir, ['src/test.cc'])
    assert ignore_file('../src/test.cc',
                       Options(os.path.join(workdir, 'build')))


def test_ignore_subdir(workdir):
    os.makedirs(os.path.join(workdir, 'src'))
    touch(os.path.join(workdir, 'src/test.cc'))
    ignore(workdir, ['src/'])
    assert ignore_file('src/test.cc', Options(workdir))


def test_ignore_subdir_file_full(workdir):
    os.makedirs(os.path.join(workdir, 'src'))
    touch(os.path.join(workdir, 'src/test.cc'))
    ignore(workdir, ['src/test.cc'])
    assert ignore_file('src/test.cc', Options(workdir))


def test_ignore_subdir_file(workdir):
    os.makedirs(os.path.join(workdir, 'src'))
    touch(os.path.join(workdir, 'src/test.cc'))
    ignore(os.path.join(workdir, 'src'), ['test.cc'])
    assert ignore_file('src/test.cc', Options(workdir))
