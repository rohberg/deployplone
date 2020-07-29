from batou import UpdateNeeded
from batou.component import Component, Attribute
from batou.lib.cmmi import Build
from batou.lib.file import File
from batou.utils import Address


class Varnish(Component):

    address = Attribute(Address, 'localhost:11090')
    control_port = Attribute(int, '11091')

    def configure(self):
        # self.provide('varnish:http', self)
        self.purgehosts = self.require('zope:http')
        self.haproxy = self.require_one('haproxy:frontend')

        self += Build(
            'https://varnish-cache.org/_downloads/varnish-6.4.0.tgz',
            checksum='sha256:f636ba2d881b146f480fb52efefae468b36c2c3e6620d07460f9ccbe364a76c2',
        )
        self += File('websiteplone.vcl', source='websiteplone.vcl')
        # self += Program(
        #     'varnish',
        #     priority=20,
        #     command='sbin/varnishd',
        #     args=self.expand(
        #         '-F -f {{component.workdir}}/zhkath.vcl '
        #         '-T localhost:{{component.control_port}} '
        #         '-a {{component.address.listen}} -p thread_pool_min=10 '
        #         '-p thread_pool_max=50 -s malloc,250M '
        #         '-n zhkath'
        #     )
        # )

        self += PurgeCache()


class PurgeCache(Component):

    varnishadm = 'bin/varnishadm'

    def verify(self):
        raise UpdateNeeded()

    def update(self):
        self.cmd(self.expand(
            '{{component.varnishadm}}'
            ' -S {{component.workdir}}/var/varnish/zhkath/_.secret'
            ' -T "localhost:{{component.parent.control_port}}"'
            ' "ban req.url ~ .*"')
        )
