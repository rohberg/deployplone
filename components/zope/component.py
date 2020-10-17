from batou.component import Attribute
from batou.component import Component
from batou.lib.buildout import Buildout
from batou.lib.file import Directory
from batou.lib.file import File
from batou.lib.supervisor import Program
from batou.utils import Address


class Zope(Component):
    standalone = Attribute(str, 'zeo')
    backupsdir = Attribute(str, '')
    adminpw = 'admin'
    zeoaddress = Attribute(Address, '127.0.0.1:11981')
    buildoutuser = Attribute(str, 'plone')

    def configure(self):
        self.provide('zopecommon', self)
        self.common = self.require_one('common', host=self.host)
        self.zope_instances = self.require('zope:http')
        self.zope_instances.sort(key=lambda s: s.script_id)
        self.backupsdir = self.backupsdir or self.expand('{{component.workdir}}/var/backup')

        config_file_name = (self.standalone=='standalone' and 'standalone.cfg') or 'buildout.cfg'
        additional_config = [Directory('profiles', source='profiles')]
        if self.standalone=='standalone':
            additional_config.append(File(
                'standalone.cfg', 
                source='standalone.cfg',
                template_context=self
                ))

        self += Buildout(
            python='3.7', 
            version=self.common.zc_buildout, 
            setuptools=self.common.setuptools,
            config_file_name = config_file_name,
            additional_config = additional_config
            )        
        self.log("self.standalone: " + self.standalone)
        self.log("self.zope_instances: " + str(self.zope_instances))
        self.log("self.config_file_name: " + config_file_name)

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
