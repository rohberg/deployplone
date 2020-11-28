Deploy Plone with Varnish, HAProxy, Volto and ElasticSearch
===========================================================

Plone 6 Volto deployment with Batou and pm2 process manager. 

**#Plone #Python #batou #ReactJS #Volto #pm2 #CMS**

## Stack

* Varnish
* Volto app
* HAProxy
* Plone (ZEO with two or more clients)
* ElasticSearch

pm2 for process management


# How do I use this template to setup deployment with my Volto app?

![alt text](./docs/ksuess_rohbergplonedeployment__usetemplate.png "use template rohbergplonedeployment")

Create your repository from this template. Customize it: your Volto app, current Plone version, etc..

Steps
- Create a repository from this template
- Clone your repository locally
- run ./batou
- customize your first environment dev.cfg
- deploy to your first environment with ./batou deploy dev 
- find your new environment in ./work/
- start with pm2 start ./work/pm2/website.pm2.config.js
- see processes with pm2 list 
- start haproxy with sudo haproxy -f path-to-your-project/work/haproxy/haproxy.cfg
- start redis: redis-server /usr/local/etc/redis.conf
- install ingest plugin for elasticsearch:
    ```
    cd work/elasticsearch
    bin/elasticsearch-plugin install ingest-attachment
    ```
- start eleasticsearch
    `./bin/elasticsearch -d`
- start ingest
    ````
    cd work/zope
    bin/celery -A collective.elastic.ingest.celery.app worker --detach
    ```

- create new environment: environment/mars.cfg
- deploy to mars with ./batou deploy mars

- Activate kitconcept.volto in control panel of plone instance http://localhost:8080/Plone/prefs_install_products_form
- Activate plone.restapi and collective.elastic.plone 


## Documentation of tools and components used

- Process management with pm2: https://pm2.keymetrics.io/docs/usage/pm2-doc-single-page/
- Deployment with Batou https://batou.readthedocs.io

## HAProxy

HAProxy is not managed by pm2 as we expect its configuration not to change often.

Run haproxy with 

```sudo haproxy -f /home/plone/myprojectstaging/work/haproxy/haproxy.cfg ```

cfg will drop privileges to user haproxy.

## Elasticsearch

- ElasticSearch in Plone with collective.elastic.plone https://github.com/collective/collective.elastic.plone
- component ElasticSearch https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html


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

- Remove all Rohberg project traces from this template
- plone.restapi installieren! See [plonesite]
- Installation and start of redis via batou
- Installation elasticsearch plugin ingest
- Continuous integration has not been set up. 
GitHub Actions and several other apps can be used to automatically catch bugs and enforce style. 

## Remarks
