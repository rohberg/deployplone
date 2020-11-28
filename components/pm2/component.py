from batou import UpdateNeeded
from batou.component import Attribute
from batou.component import Component
from batou.lib.file import File
from batou.lib.git import Clone

# INFO restart not necessary as process is started with --watch

class Pm2(Component):

    pm2prefix = Attribute(str, 'local.mydomain.ch-')

    def configure(self):
        # self.provide('pm2', self)
        self.voltoapp = self.require_one('voltoapp')
        self.varnish = self.require_one('varnish:http')
        self.zopecommon = self.require_one('zopecommon')
        self.elasticsearch = self.require_one('elasticsearch')
        self += File(
            'website.pm2.config.js', 
            source='website.pm2.config.js'
            )
        self += RestartTasks('all')


class RestartTasks(Component):

    namevar = 'appname'

    def verify(self):
        raise UpdateNeeded()

    def update(self):
        self.cmd('pm2 start {{component.workdir}}/website.pm2.config.js')
        self.log('Restarted tasks')
