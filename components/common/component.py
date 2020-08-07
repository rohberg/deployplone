from batou import UpdateNeeded
from batou.component import Component
from batou.lib.file import Directory, File
import batou_ext.ssh


class Common(Component):

    github_ssh_key = None
    setuptools = "42.0.2"
    zc_buildout = "2.13.3"

    def configure(self):
        self.provide('common', self)
        self += SSH(key=self.github_ssh_key)


class SSH(Component):

    scan_hosts = ''

    def configure(self):
        self.scan_hosts = self.scan_hosts.split()
        for host in self.scan_hosts:
            self += batou_ext.ssh.ScanHost(host)

        self += Directory('andermatt')
        self += Directory('andermatt/.ssh')        
        self += File('andermatt/.ssh', ensure='directory', mode=0o700)
        self += File('andermatt/.ssh/config', source='ssh_config')
        self += File('andermatt/.ssh/id_rsa_github_rohbergdeployment', content=self.key, mode=0o600)


class EnsurePermissions(Component):

    namevar = 'path'
    mode = None

    def configure(self):
        self.path = self.map(self.path)

    def verify(self):
        raise UpdateNeeded()

    def update(self):
        self.cmd('chmod {} "{}"'.format(self.mode, self.path))
