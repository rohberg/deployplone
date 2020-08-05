"""clone voltoapp

TODO update voltoapp

yarn build if repository has changes (package.json)
"""

from batou.component import Attribute
from batou.component import Component
from batou.lib.file import File
from batou.lib.git import Clone
from batou.utils import Address

import os.path

# global configuration that is not individually for environments 
configuration = {
    'apprepository': 'https://github.com/ksuess/schweikertruth.git',
}

class Voltoapp(Component):
    apprepository = Attribute(str, configuration['apprepository'])
    address = Attribute(Address, 'localhost:3000')
    razzleapipath = Attribute(str, 'http://localhost:11080/Plone') # TODO haproxy port eintragen

    def configure(self):
        self.provide('voltoapp', self)
        self += Clone(
            self.apprepository,
            branch='master')

    def verify(self):
        self.assert_no_changes()
        if not os.path.exists(self.workdir + '/build'):
            raise UpdateNeeded()

    def update(self):
        if not os.path.exists(self.workdir + "/node_modules"):
            self.cmd("yarn")
        voltoportandrazzle = 'PORT={} RAZZLE_API_PATH={}'.format( \
            self.address.connect.port, self.razzleapipath)
        self.cmd(voltoportandrazzle + ' yarn build')
        self.log("Voltoapp rebuild with {}".format(voltoportandrazzle))



# class VoltoappRebuild(Component):

#     namevar = 'buildparameter'

#     def verify(self):
#         self.assert_no_changes()
#         assert os.path.exists(self.workdir + "/build")

#     def update(self):
#         if not os.path.exists(self.workdir + "/node_modules"):
#             self.cmd("yarn")
#         self.cmd(self.buildparameter + ' yarn build')
