module.exports = {
  apps: [
    {
      name: "{{component.voltoappname}}",
      script: "{{component.voltoapp.workdir}}/build/server.js",
      cwd: "{{component.voltoapp.workdir}}",
      watch       : true,
      env: {
        "NODE_ENV": "production",
      },
      env_development : {
         "NODE_ENV": "development"
      }
    },
    {
      name: "{{component.varnishname}}",
      script: "{{component.varnish.workdir}}/{{component.varnish.daemon}}",
      args: "{{component.varnish.daemonargs}}",
      cwd: "{{component.varnish.workdir}}",
    }
  ]
};

// start with pm2 restart <pathtofile>/website.pm2.config.js
// or ... --env development to start in development mode



// see documentation:
// https://pm2.keymetrics.io/docs/usage/application-declaration/

// TOOD haproxy, zeo, zope, instances