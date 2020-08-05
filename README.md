rohbergplonedeployment
======================

Plone6 deployment with batou. 

#Plone #Python #batou #ReactJS #Volto #pm2 #CMS

stack
---------

* varnish
* Volto app
* HAProxy
* Plone

pm2 for process management


Open http://localhost:3000/ to access Volto app


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
