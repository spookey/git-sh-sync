#!/usr/bin/env python3

from datetime import datetime
from os import path
from pprint import pprint

from setuptools import find_packages


class Info:
    _v_major = '0'
    _v_minor = '0'
    _v_patch = '0'

    @property
    def version(self):
        return '{}.{}'.format(self._v_major, self._v_minor)

    @property
    def release(self):
        return '{}.{}'.format(self.version, self._v_patch)

    #

    project = 'git-sh-sync'
    description = '''
        Python library to automatically synchronize git repositories via shell
    '''.strip()

    _contrib = [
        ('Frieder Grießhammer', 'frieder.griesshammer@der-beweis.de')
    ]

    @property
    def author_name(self):
        return self._contrib[-1][0]

    @property
    def author_email(self):
        return self._contrib[-1][1]

    @property
    def copyright(self):
        now = datetime.utcnow()
        return '{}, {}'.format(now.year, self.author_name)

    #

    @staticmethod
    def location(*joins):
        root = path.dirname(path.realpath(__file__))
        return path.realpath(path.join(root, *joins))

    _readme_name = 'README.rst'

    @property
    def readme(self):
        result = ''
        with open(self.location(self._readme_name), 'r') as handle:
            result = handle.read()
        return result.strip()

    #

    def _urlparse_readme(self, ident):
        result = ''
        for elem in reversed([
                line.strip() for line in self.readme.splitlines()
                if line.startswith(ident)
        ]):
            result = elem.partition(ident)[-1]
        return result.strip()

    @property
    def url_docs(self):
        return self._urlparse_readme(':Read the Docs:')

    @property
    def url_travis(self):
        return self._urlparse_readme(':Travis CI:')

    @property
    def url_github(self):
        return self._urlparse_readme(':GitHub:')

    @property
    def url_github_download(self):
        return '{}/archive/{}.tar.gz'.format(
            self.url_github,
            self.release
        )

    @property
    def project_urls(self):
        return {
            'GitHub': self.url_github,
            'Read the Docs': self.url_docs,
            'Travis-CI': self.url_travis,
        }

    #

    @property
    def packages(self):
        return find_packages(
            where=self.location(),
            exclude=['tests*', 'docs*']
        )

    #

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: System :: Archiving',
        'Topic :: System :: Filesystems',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Recovery Tools',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ]

    keywords = ' '.join([
        'git',
        'library',
        'auto-sync'
    ])

    #

    def __call__(self):
        return dict(
            name=self.project,
            version=self.release,
            description=self.description,
            long_description=self.readme,
            long_description_content_type='text/x-rst',
            url=self.url_github,
            author=self.author_name,
            author_email=self.author_email,
            download_url=self.url_github_download,
            classifiers=self.classifiers,
            keywords=self.keywords,
            packages=self.packages,
            project_urls=self.project_urls,
            install_requires=[],
            python_requires='>=3.5',
        )


INFO = Info()


if __name__ == '__main__':
    pprint(INFO())
