from batou import UpdateNeeded
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
        self += RestartVoltoapp(self.voltoappname) 
        # self += RestartZopeInstances(self.zopename)


class RestartVoltoapp(Component):

    namevar = 'appname'

    def verify(self):
        self.voltoapp = self.require_one('voltoapp')
        self.voltoapp.assert_no_changes()

    def update(self):
        self.cmd("pm2 restart {}".format(self.appname))
        self.log('Restarted {}'.format(self.appname))


class RestartZopeInstances(Component):
    """ Check if Plone or Plone add-ons changed and restart Zope instances if they did."""

    namevar = 'appname'

    def verify(self):
        raise UpdateNeeded()

    def update(self):
        for zopeinstance in self.require("zope:http"):
            self.cmd("pm2 restart {}-api-{}".format(self.appname, zopeinstance.script_id))
        self.log("Zope instances restarted")