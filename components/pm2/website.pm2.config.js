apps = [
  {
    name: "{{component.pm2prefix}}zope-instance1",
    script: "{{component.zopecommon.workdir}}/bin/instance1",
    args: "console",
    cwd: "{{component.zopecommon.workdir}}",
    interpreter: "{{component.zopecommon.workdir}}/bin/python",
    watch: false,
    min_uptime: 10000,
    kill_timeout : 3000,
  },
  {
    name: "{{component.pm2prefix}}zope-instance2",
    script: "{{component.zopecommon.workdir}}/bin/instance2",
    args: "console",
    cwd: "{{component.zopecommon.workdir}}",
    interpreter: "{{component.zopecommon.workdir}}/bin/python",
    watch: false,
    min_uptime: 10000,
    kill_timeout : 3000,
  },
  {
    name: "{{component.pm2prefix}}zope-zeoserver",
    script: "{{component.zopecommon.workdir}}/bin/zeoserver",
    args: "fg",
    cwd: "{{component.zopecommon.workdir}}",
    interpreter: "{{component.zopecommon.workdir}}/bin/python",
    watch: false,
    min_uptime: 10000,
    kill_timeout: 3000,
  },
  {
    name: "{{component.pm2prefix}}voltoapp",
    script: "{{component.voltoapp.workdir}}/build/server.js",
    cwd: "{{component.voltoapp.workdir}}",
    watch: false,
    env: {
      "NODE_ENV": "production",
    },
    env_development : {
       "NODE_ENV": "development"
    }
  },
  {
    name: "{{component.pm2prefix}}varnish",
    script: "{{component.varnish.workdir}}/{{component.varnish.daemon}}",
    args: "{{component.varnish.daemonargs}}",
    cwd: "{{component.varnish.workdir}}",
    watch: false,
  },
  // {
  //   name: "{{component.pm2prefix}}elasticsearch",
  //   script: "{{component.elasticsearch.workdir}}/bin/elasticsearch -d",
  //   cwd: "{{component.elasticsearch.workdir}}",
  //   watch: false,
  // },
  // {
  //   name: "{{component.pm2prefix}}ingest",
  //   script: "{{component.zopecommon.workdir}}/bin/celery -A collective.elastic.ingest.celery.app worker --detach",
  //   cwd: "{{component.zopecommon.workdir}}",
  //   env: {
  //     "CELERY_BROKER=redis://localhost:6379/0": "redis://localhost:6379/0",
  //     "ELASTICSEARCH_INGEST_SERVER": "localhost:9200",
  //     "ELASTICSEARCH_INGEST_USE_SSL": "0",
  //     "PLONE_SERVICE": "http://localhost:8080",
  //     "PLONE_PATH": "Plone",
  //     "PLONE_USER": "admin",
  //     "PLONE_PASSWORD": "admin",
  //     "MAPPINGS_FILE": "{{component.workdir}}/elasticsearch-mappings.json",
  //     "PREPROCESSINGS_FILE": "{{component.workdir}}/elasticsearch-preprocessings.json",
  //   },
  //   watch: false,
  // }
]


module.exports = { apps: apps };

// start all with pm2 restart <pathtofile>/website.pm2.config.js
// or ... --env development to start in development mode


// see documentation:
// https://pm2.keymetrics.io/docs/usage/application-declaration/


// TOOD restart Zope instances on batou run