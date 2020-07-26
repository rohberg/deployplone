"""clone voltoapp

TODO update voltoapp

yarn build if repository has changes (package.json)
"""

from batou.component import Attribute
from batou.component import Component
from batou.lib.file import File
from batou.lib.git import Clone

port = "PORT="
razzle = "RAZZLE_API_PATH="

class Voltoapp(Component):
    apprepository = Attribute(str, 'https://github.com/ksuess/schweikertruth.git')
    voltoport = Attribute(str, '')
    razzleapipath = Attribute(str, '')

    def configure(self):
        self.provide('voltoapp', self)
        self += Clone(
            self.apprepository, 
            revision='HEAD', 
            vcs_update=True,
            )

        voltoportandrazzle = (self.voltoport and self.razzleapipath) and '{}={} {}={}'.format( \
            port, self.voltoport, razzle, self.razzleapipath) or ''
        self += VoltoappRebuild(voltoportandrazzle)


class VoltoappRebuild(Component):

    namevar = 'buildparameter'

    def verify(self):
        self.parent.assert_file_is_current(self.workdir, ['package.json'])

    def update(self):
        self.cmd(self.buildparameter + ' yarn build')
        print("VoltoApp rebuild")
