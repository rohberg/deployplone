module.exports = {
  apps: [
    {
      name: "{{component.voltoappname}}",
      script: "{{component.voltoapp.workdir}}/build/server.js",
      cwd: "{{component.voltoapp.workdir}}",
      watch: true,
      env: {
        "NODE_ENV": "production",
      },
      env_development : {
         "NODE_ENV": "development"
      }
    },

    {
      name: "{{component.zopename}}-api-zeoserver",
      script: "{{component.zopecommon.workdir}}/bin/zeoserver",
      args: "fg",
      cwd: "{{component.zopecommon.workdir}}",
      interpreter: "{{component.zopecommon.workdir}}/bin/python",
      min_uptime: 10000,
      kill_timeout: 3000,
    },
    {
      name: "{{component.zopename}}-api-instance1",
      script: "{{component.zopecommon.workdir}}/bin/instance1",
      args: "console",
      cwd: "{{component.zopecommon.workdir}}",
      interpreter: "{{component.zopecommon.workdir}}/bin/python",
      watch: ["{{component.zopecommon.workdir}}"],
      min_uptime: 10000,
      kill_timeout : 3000,
    },
    {
      name: "{{component.zopename}}-api-instance2",
      script: "{{component.zopecommon.workdir}}/bin/instance2",
      args: "console",
      cwd: "{{component.zopecommon.workdir}}",
      interpreter: "{{component.zopecommon.workdir}}/bin/python",
      watch: ["{{component.zopecommon.workdir}}"],
      min_uptime: 10000,
      kill_timeout : 3000,
    },

    {
      name: "{{component.varnishname}}",
      script: "{{component.varnish.workdir}}/{{component.varnish.daemon}}",
      args: "{{component.varnish.daemonargs}}",
      cwd: "{{component.varnish.workdir}}",
    },

  ]
};

// start all with pm2 restart <pathtofile>/website.pm2.config.js
// or ... --env development to start in development mode


// see documentation:
// https://pm2.keymetrics.io/docs/usage/application-declaration/


// TOOD restart Zope instances on batou run