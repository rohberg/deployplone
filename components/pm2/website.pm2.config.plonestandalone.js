apps = [
  {
    name: "{{component.zopename}}-api-instance1",
    script: "{{component.zopecommon.workdir}}/bin/instance1",
    args: "console",
    cwd: "{{component.zopecommon.workdir}}",
    interpreter: "{{component.zopecommon.workdir}}/bin/python",
    watch: false,
    min_uptime: 10000,
    kill_timeout : 3000,
  },
]

if ("{{component.zopecommon.standalone}}" != 'standalone') {
  apps.push(
    {
      name: "{{component.zopename}}-api-zeoserver",
      script: "{{component.zopecommon.workdir}}/bin/zeoserver",
      args: "fg",
      cwd: "{{component.zopecommon.workdir}}",
      interpreter: "{{component.zopecommon.workdir}}/bin/python",
      watch: false,
      min_uptime: 10000,
      kill_timeout: 3000,
    },
  )
  apps.push(
    {
      name: "{{component.zopename}}-api-instance2",
      script: "{{component.zopecommon.workdir}}/bin/instance2",
      args: "console",
      cwd: "{{component.zopecommon.workdir}}",
      interpreter: "{{component.zopecommon.workdir}}/bin/python",
      watch: false,
      min_uptime: 10000,
      kill_timeout : 3000,
    }
  )
}


module.exports = { apps: apps };

// start all with pm2 restart <pathtofile>/website.pm2.config.js
// or ... --env development to start in development mode


// see documentation:
// https://pm2.keymetrics.io/docs/usage/application-declaration/


// TOOD restart Zope instances on batou run