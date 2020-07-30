from batou.component import Attribute
from batou.component import Component
from batou.lib.file import File
from batou.lib.git import Clone

# INFO restart not necessary as process is started with --watch

class Pm2(Component):

    voltoappname = Attribute(str, "environment.website-volto")
    varnishname = Attribute(str, "environment.website-varnish")
    zopename = Attribute(str, "environment.website-zope")

    def configure(self):
        # self.provide('pm2', self)
        self.voltoapp = self.require_one('voltoapp')
        self.varnish = self.require_one('varnish:http')
        self.zopecommon = self.require_one('zopecommon')
        self += File(
            'website.pm2.config.js', 
            source='website.pm2.config.js'
            )
        self.cmd("pm2 restart {} --watch".format(self.workdir + '/website.pm2.config.js'))