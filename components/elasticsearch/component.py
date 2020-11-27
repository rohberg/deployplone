# from batou import UpdateNeeded
from batou.component import Component, Attribute
# from batou.lib.file import File
# from batou.lib.python import VirtualEnv
# from batou.utils import Address

from batou.lib.archive import Extract
from batou.lib.download import Download

class ElasticSearch(Component):

    uri  = Attribute(str, 'https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.10.0-linux-x86_64.tar.gz')
    checksum = Attribute(str, 'sha512:5c159bdf0d6e140a2bee5fbb1c379fbe23b0ea39b01d715564f02e4674b444b065a8abfda86440229c4b70defa175722c479b60009b7eef7b3de66e2339aacea')


    def configure(self):
        # self.provide('elasticsearch:http', self)

        download = Download(self.uri, checksum=self.checksum)
        self += download

        extract = Extract(download.target, strip=1)
        self += extract
