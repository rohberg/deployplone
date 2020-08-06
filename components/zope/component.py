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
    buildoutuser = Attribute(str, 'plone')

    def configure(self):
        self.provide('zopecommon', self)
        self.common = self.require_one('common', host=self.host)
        self.zope_instances = self.require('zope:http')
        self.zope_instances.sort(key=lambda s: s.script_id)
        self.backupsdir = self.backupsdir or self.expand('{{component.workdir}}/var/backup')

        self += Buildout(
            python='3.7', 
            version=self.common.zc_buildout, 
            setuptools=self.common.setuptools,
            additional_config=[Directory('profiles', source='profiles')]
            )

# TODO update: restart on change

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
