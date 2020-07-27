from batou.component import Component, Attribute
from batou.lib.buildout import Buildout
from batou.lib.file import Directory
from batou.lib.supervisor import Program
from batou.utils import Address


class ZEO(Component):
    address = Attribute(Address, '127.0.0.1:9100')
    profile = 'base'
    eggs_directory = '{{component.environment.workdir_base}}/eggs'


    def configure(self):
        self.common = self.require_one('common', host=self.host)
        self.provide('zhkath:zeo:server', self.address)
        self += Directory('download-cache')
        self.eggs_directory = self.expand(self.eggs_directory)

        self += Buildout(
            python='3.7', 
            version=self.common.zc_buildout, 
            setuptools=self.common.setuptools,
            )

        # self += Program(
        #     'zeo',
        #     priority=10,
        #     options={'startsecs': 30},
        #     command=self.map('bin/zeo start'),
        #     args=self.expand('-C {{component.workdir}}/parts/zeo/zeo.conf')
        # )
