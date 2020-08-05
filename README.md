rohbergplonedeployment
======================

Plone6 deployment with batou. 

**#Plone #Python #batou #ReactJS #Volto #pm2 #CMS**

stack
---------

* Varnish
* Volto app
* HAProxy
* Plone

pm2 for process management

local deployment:
Open http://localhost:3000/ to access Volto app.
Open http://localhost:11090/ to access Volto app via Varnish.


Troubleshooting
-----------------

All processes running?

`pm2 list`

Tips
-----

- cfgs in /zope/profile without Jinja


TODO
------
 
- Continuous integration has not been set up. 
GitHub Actions and several other apps can be used to automatically catch bugs and enforce style. 

Remarks
-------

HAProxy is not managed by pm2 as we expect its configuration not to change often.
