from batou import UpdateNeeded
from batou.component import Component, Attribute
from batou.lib.file import Directory, File, Purge
from batou_ext.ssh import ScanHost


class Common(Component):

    # github_ssh_key = None
    id_rsa_github_rohbergdeployment = None
    id_rsa_github_rohbergdeployment_pub = None

    setuptools = "42.0.2"
    zc_buildout = "2.13.3"

    def configure(self):
        self.provide('common', self)
        # self += SSH(key=self.github_ssh_key)
        self += SSHKeyPairCustom(provide_itself=False, id_rsa=self.id_rsa_github_rohbergdeployment, id_rsa_pub=self.id_rsa_github_rohbergdeployment_pub)


# class SSH(Component):

#     scan_hosts = ''

#     def configure(self):
#         self.scan_hosts = self.scan_hosts.split()
#         for host in self.scan_hosts:
#             self += batou_ext.ssh.ScanHost(host)

#         self += Directory('andermatt')
#         self += Directory('andermatt/.ssh')        
#         self += File('andermatt/.ssh', ensure='directory', mode=0o700)
#         self += File('andermatt/.ssh/config', source='ssh_config')
#         self += File('andermatt/.ssh/id_rsa_github_rohbergdeployment', content=self.key, mode=0o600)

class SSHKeyPairCustom(Component):

    """Install SSH user and host keys.
    User keys are read from the secrets file and written to
    ~/.ssh/id_rsa{,.pub} and/or ~/.ssh/id_ed25519{,.pub}.
    
    changes: no Directory
    """

    # RSA-keys
    id_rsa = None
    id_rsa_pub = None

    # ed25510-keys
    id_ed25519 = None
    id_ed25519_pub = None

    scan_hosts = Attribute('list', '')
    provide_itself = Attribute('literal', True)
    purge_unmanaged_keys = Attribute('literal', False)

    def configure(self):
        if self.provide_itself:
            self.provide('sshkeypair', self)

        # self += Directory('~/.ssh', mode=0o700)

        # RSA
        if self.id_rsa:
            self += File('~/.ssh/id_rsa',
                         content=self.id_rsa,
                         mode=0o600,
                         sensitive_data=True)
        elif self.purge_unmanaged_keys:
            self += Purge('~/.ssh/id_rsa')

        if self.id_rsa_pub:
            self += File('~/.ssh/id_rsa.pub',
                         content=self.id_rsa_pub)

        # ED25519
        if self.id_ed25519:
            self += File('~/.ssh/id_ed25519',
                         content='{}\n'.format(self.id_ed25519),
                         mode=0o600,
                         sensitive_data=True)

        elif self.purge_unmanaged_keys:
            self += Purge('~/.ssh/id_ed25519')

        if self.id_ed25519_pub:
            self += File('~/.ssh/id_ed25519.pub',
                         content=self.id_ed25519_pub)

        # ScanHost
        for host in self.scan_hosts:
            self += ScanHost(host)

class EnsurePermissions(Component):

    namevar = 'path'
    mode = None

    def configure(self):
        self.path = self.map(self.path)

    def verify(self):
        raise UpdateNeeded()

    def update(self):
        self.cmd('chmod {} "{}"'.format(self.mode, self.path))
