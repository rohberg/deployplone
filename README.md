rohbergplonedeployment
======================

Plone 6 Volto deployment with Batou. 

**#Plone #Python #batou #ReactJS #Volto #pm2 #CMS**

## Stack

* Varnish
* Volto app
* HAProxy
* Plone (ZEO with two clients)

pm2 for process management

## Documentation of tools and components used

- Process management with pm2: https://pm2.keymetrics.io/docs/usage/pm2-doc-single-page/
- Deployment with Batou https://batou.readthedocs.io

## HAProxy

HAProxy is not managed by pm2 as we expect its configuration not to change often.

Run haproxy with 

```sudo haproxy -f /home/plone/schweikertstaging/work/haproxy/haproxy.cfg ```

cfg will drop privileges to user haproxy.

## Local deployment on nginx


```
upstream volto {
    server localhost:3000;
}
upstream ploneapi {
    server localhost:11080;
}

location ~ /api($|/.*) {
  rewrite ^/api($|/.*) /VirtualHostBase/http/voltodeployment.example.com:80/Plone/VirtualHostRoot/_vh_api$1 break;
  proxy_pass http://ploneapi;
}

location ~ / {
  # Default set to 1m - this is mainly to make PSI happy, adjust to your needs
  location ~* \.(ico|jpg|jpeg|png|gif|svg|js|jsx|css|less|swf|eot|ttf|otf|woff|woff2)$ {
  add_header Cache-Control "public";
  expires +1m;
  proxy_pass http://volto;
}
````

Open http://voltodeployment.example.com/ to access Volto app via Varnish.


## Troubleshooting


All processes running?

`pm2 list`

![alt text](./docs/pm2-list.png "pm2 list")


## Tips


- No Jinja in cfgs in /zope/profile

## Sugar

`pm2 show local.mywebsite.ch-volto`

shows even last git update date.


## TODO
 
- Continuous integration has not been set up. 
GitHub Actions and several other apps can be used to automatically catch bugs and enforce style. 

## Remarks
