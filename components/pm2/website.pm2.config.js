module.exports = {
  apps: [
    {
      script: "{{component.voltoapp.workdir}}/build/server.js",
      name: "{{component.voltoappname}}",
      cwd: "{{component.voltoapp.workdir}}"
    }
  ]
};


// TOOD zeo, zope, instances