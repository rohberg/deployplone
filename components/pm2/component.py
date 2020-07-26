from batou.component import Attribute
from batou.component import Component
from batou.lib.file import File
from batou.lib.git import Clone

# TODO watch for new build

class Pm2(Component):

    voltoappname = Attribute(str, "ruthschweikert.ch-volto")

    def configure(self):
        self.voltoapp = self.require_one('voltoapp')
        self += File(
            'website.pm2.config.js', 
            source='website.pm2.config.js'
            )