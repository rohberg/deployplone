from batou.component import Component
from batou.lib.file import File


class Tick(Component):

    def configure(self):
        # self.common = self.require_one('common', host=self.host)
        self += File(
            'tick.sh',
            mode=0o700,
            content="""\
#!/bin/bash
while true; do
  date
  sleep 1
done
""")