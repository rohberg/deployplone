from batou.component import Attribute
from batou.component import Component
from batou.lib.buildout import Buildout
from batou.lib.file import Directory
from batou.lib.file import File
from batou.lib.supervisor import Program
from batou.utils import Address


class Zope(Component):
    backupsdir = Attribute(str, '')
    adminpw = 'admin'
    instance_name = 'zeoclientoderso'
    zeoaddress = Attribute(Address, '127.0.0.1:11981')

    def configure(self):
        # self.provide('zopecommon', self)
        self.common = self.require_one('common', host=self.host)
        self.zope_instances = self.require('zope:http')
        self.backupsdir = self.backupsdir or self.expand('{{component.workdir}}/var/backup')

        self += Buildout(
            python='3.7', 
            version=self.common.zc_buildout, 
            setuptools=self.common.setuptools,
            additional_config=[Directory('profiles', source='profiles')]
            )
        self += Program(
            'zeoserver',
            priority=10,
            options={'startsecs': 30},
            command=self.map('bin/zeoserver start'),
            args=self.expand('-C {{component.workdir}}/parts/zeoserver/zeo.conf')
        )
        for instance in self.zope_instances:
            self += Program(
                instance.script_id,
                priority=11,
                options={
                    'startsecs': 20,
                    'stopsignal': 'INT',
                    'stopwaitsecs': 5,
                },
                command=self.map('bin/{} console'.format(instance.script_id)),
            )


class BaseInstance(Component):
    workdir = '{{component.zope.workdir}}'
    address = Attribute(Address, '127.0.0.1:11991')
    script_id = "instance1"

    def configure(self):
        self.provide('zope:http', self)


class Instance1(BaseInstance):
    """Use defaults."""


class Instance2(BaseInstance):
    address = Attribute(Address, '127.0.0.1:11992')
    script_id = "instance2"


# class Instance3(BaseInstance):
#     address = Attribute(Address, '127.0.0.1:9083')
#     script_id = "instance3"


# class Instance4(BaseInstance):
#     address = Attribute(Address, '127.0.0.1:9084')
#     script_id = "instance4"
