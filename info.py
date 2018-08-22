from datetime import datetime


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
        python library to sync git repositories via shell
    '''.strip()

    _contrib = [
        ('Frieder Grießhammer', 'frieder.griesshammer@der-beweis.de')
    ]

    @property
    def author(self):
        return self._contrib[-1][0]

    @property
    def copyright(self):
        now = datetime.utcnow()
        return '{}, {}'.format(now.year, self.author)
