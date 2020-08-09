"""clone voltoapp

TODO update voltoapp

yarn build if repository has changes (package.json)
"""

from batou import UpdateNeeded
from batou.component import Attribute
from batou.component import Component
from batou.lib.file import File
from batou.lib.git import Clone
from batou.utils import Address

import os.path

# global configuration that is not individually for environments 
configuration = {
    'apprepository': 'git@github.com:ksuess/schweikertruth.git',
}

class Voltoapp(Component):
    apprepository = Attribute(str, configuration['apprepository'])
    address = Attribute(Address, 'localhost:3000')
    razzleapipath = Attribute(str, 'http://localhost:11080/Plone') # TODO haproxy port eintragen

    def configure(self):
        self.provide('voltoapp', self)
        # TODO Try to avoid dependency cycle without setting dirty=True
        # self.varnish = self.require_one('varnish:http', reverse=True, dirty=True)
        self += Clone(
            self.apprepository,
            branch='master')

    def verify(self):
        # raise UpdateNeeded() # enforce rebuild of Volto app
        self.assert_no_changes()
        if not os.path.exists(self.workdir + '/build'):
            raise UpdateNeeded()

    def update(self):
        # yarn production build
        if not os.path.exists(self.workdir + "/node_modules"):
            self.cmd("yarn")
        port = self.address.connect.port
        voltoportandrazzle = 'PORT={} RAZZLE_API_PATH={}'.format( \
            port, self.razzleapipath)
        self.cmd('{} yarn build'.format(voltoportandrazzle or ''))
        self.log("Voltoapp rebuild with {}".format(voltoportandrazzle))
