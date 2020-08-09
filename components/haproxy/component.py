from batou.component import Component, Attribute, platform
from batou.lib.file import File, Directory
from batou.utils import Address


class HAProxy(Component):
    """TODO Documentation HAProxy."""

    port = '11080'
    address = Attribute(Address, 'localhost:11080')
    stats_socket = Attribute(str, '{{component.workdir}}/haproxy_admin.sock')
    jail_dir = Attribute(str, '{{component.workdir}}/jail')

    def configure(self):
        self.provide('haproxy:frontend', self)

        self.bindspec = str(self.address.listen)
        if '127.0.0.1:' + self.port not in self.bindspec:
            # need to cater for the standard nagios check as well
            self.bindspec += ',127.0.0.1:' + self.port

        self.servers = self.require('zope:http')
        self.servers.sort(key=lambda s: s.script_id)

        self += File(
            self.expand('{{component.workdir}}/haproxy.cfg'),
            source='haproxy.cfg'
        )
        self += Directory('jail')


@platform('ubuntu', HAProxy)
class HAProxyReload(Component):

    def verify(self):
        self.parent.assert_no_subcomponent_changes()

    def update(self):
        self.cmd('sudo -n /etc/init.d/haproxy reload')
