from batou.component import Attribute
from batou.component import Component
from batou.lib.buildout import Buildout
from batou.lib.file import Directory
from batou.lib.file import File
from batou.lib.supervisor import Program
from batou.utils import Address


class Zope(Component):
    adminpw = 'admin'
    profile = 'base'
    eggs_directory = '{{component.environment.workdir_base}}/eggs'
    instance_name = 'zhkath'
    backupsdir = '{{component.environment.workdir_base}}/backup'


    def configure(self):
        self.zeo = self.require_one('zhkath:zeo:server')
        self.common = self.require_one('common', host=self.host)
        self.zope_instances = self.require('zope:http')
        # self.provide('zope:common', self)
        self.eggs_directory = self.expand(self.eggs_directory)

        self += Buildout(
            python='3.7', 
            version=self.common.zc_buildout, 
            setuptools=self.common.setuptools,
            additional_config=[Directory('profiles', source='profiles')]
            )

        # for instance in self.zope_instances:
        #     self += Program(
        #         instance.script_id,
        #         priority=11,
        #         options={
        #             'startsecs': 20,
        #             'stopsignal': 'INT',
        #             'stopwaitsecs': 5,
        #         },
        #         command=self.map('bin/{} console'.format(instance.script_id)),
        #     )


class BaseInstance(Component):
    workdir = '{{component.zope.workdir}}'
    address = Attribute(Address, '127.0.0.1:9081')
    script_id = "instance1"

    def configure(self):
        self.provide('zope:http', self)


class Instance1(BaseInstance):
    """Use defaults."""


class Instance2(BaseInstance):
    address = Attribute(Address, '127.0.0.1:9082')
    script_id = "instance2"


# class Instance3(BaseInstance):
#     address = Attribute(Address, '127.0.0.1:9083')
#     script_id = "instance3"


# class Instance4(BaseInstance):
#     address = Attribute(Address, '127.0.0.1:9084')
#     script_id = "instance4"
