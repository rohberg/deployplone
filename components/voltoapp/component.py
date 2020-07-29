"""clone voltoapp

TODO update voltoapp

yarn build if repository has changes (package.json)
"""

from batou.component import Attribute
from batou.component import Component
from batou.lib.file import File
from batou.lib.git import Clone
from batou.utils import Address

# global configuration that is not individually for environments 
configuration = {
    'apprepository': 'https://github.com/ksuess/schweikertruth.git',
}

class Voltoapp(Component):
    apprepository = Attribute(str, configuration['apprepository'])
    address = Attribute(Address, 'localhost:3000')
    razzleapipath = Attribute(str, 'localhost:11080/api') # TODO haproxy port eintragen

    def configure(self):
        self.provide('voltoapp', self)
        self += Clone(
            self.apprepository, 
            revision='HEAD', 
            vcs_update=True,
            )

        voltoportandrazzle = 'PORT={} RAZZLE_API_PATH={}'.format( \
            self.address.connect.port, self.razzleapipath)
        self += VoltoappRebuild(voltoportandrazzle)


class VoltoappRebuild(Component):

    namevar = 'buildparameter'

    def verify(self):
        self.parent.assert_file_is_current(self.workdir, ['package.json'])

    def update(self):
        self.cmd(self.buildparameter + ' yarn build')
        print("VoltoApp rebuild")
