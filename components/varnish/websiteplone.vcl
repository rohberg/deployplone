# Generated from template; don't edit manually
vcl 4.0;

/*
24h 86400
1 week 604800
4 weeks 4233600
one year 31536000
*/

import std;

backend default {
    .host = "{{component.voltoapp.address.connect.host}}";
    .port = "{{component.voltoapp.address.connect.port}}";
}
backend api {
    .host = "{{component.haproxy.address.connect.host}}";
    .port = "{{component.haproxy.address.connect.port}}";
}

acl purge {
    "127.0.0.1";
    {% for server in component.purgehosts: %}
    "{{server.address.connect.host}}";
    {% endfor %}
}


sub vcl_recv {
    if (req.method == "PURGE") {
        if (!client.ip ~purge) {
            # error 405 "Not allowed.";
            return (synth(405, "Not allowed."));
        }
        # return(lookup);
        # If you got this stage (and didn't error out above), purge the cached result
        return (purge);
    }

    # backends Plone and Volto
    if (req.url ~ "^/VirtualHostBase/") {
        set req.backend_hint = api;
    } else {
        set req.backend_hint = default;
    }
    
    # Remove PIWIK Matomo Cookies
    set req.http.Cookie = regsuball(req.http.Cookie, "_pk_.=[^;]+(; )?", "");
    set req.http.Cookie = regsuball(req.http.Cookie, "MATOMO_SESSID.=[^;]+(; )?", "");


    # Remove a ";" prefix, if present.
    set req.http.Cookie = regsub(req.http.Cookie, "^;\s*", "");


    # if (req.http.Authorization) {
    if (req.http.Authorization || req.http.Cookie ~ "__ac") {
        # All assests from the theme should be cached anonymously, also from ++plone++static
        if (req.url !~ "(\+\+plone\+\+production|\+\+plone\+\+static|\+\+resource|\+\+plone\+\+rohberg|\+\+plone\+\+patternslib)") {
            return (pass);
        } else {
            unset req.http.Authorization;
            unset req.http.Cookie;
            return (hash);
            }
    }


    # revalidate content images
    # get content images from cache
    if (req.url ~ "(/@@images/)") {
     return (hash);
    }

    # get any other image from cache
    if (req.url ~ "\.(svg|ico|jpg|jpeg|gif|png)$") {
        return (hash);
    }
    # get fonts from cache
    if (req.url ~ "(\.(otf|ttf|woff|woff2)$|\.(otf|ttf|woff|woff2)\?)") {
        return (hash);
    }
    # get audio and video from cache
    if (req.url ~ "\.(mp3|mp4|mpeg|wav)$") {
        return (hash);
    }

    # get javascript and css from cache
    if (req.url ~ "(\.(js|css|map)$|\.(js|css)\?version|\.(js|css)\?t)") {
        return (hash);
    }
    # get pdf from cache
    if (req.url ~ "\.(pdf|xls|txt|docx)$") {
        return (hash);
    }

    # # get everything else from backend
    # return(pass);
}



sub vcl_hash {
    hash_data(req.url);
    return(lookup);
}



# sub vcl_hit {
#     if (req.method == "PURGE") {
#         return(purge);
#         # error 200 "Purged.";
#         return (synth(200, "Purged."));
#    }
# }
# sub vcl_miss {
#     if (req.method == "PURGE") {
#         return(purge);
#         # error 200 "Purged.";
#     }
# }


sub vcl_backend_response {
    # Happens after we have read the response headers from the backend.
    #
    # Here you clean the response headers, removing silly Set-Cookie headers
    # and other mistakes your backend does.

    /* scaled images
    if we have scaled images, make sure they are cached.
    Don't cache in the browser though, it might change,
    and then we want to deliver the new one immediately.
    TODO: gibts ein revalidate: schaut Varnish, ob die etwa von Zope veraendert wurden?
    */
    if (bereq.url ~ "/@@images/") {
        set beresp.ttl = 604800s;
        set beresp.http.cache-control = "max-age=0;s-maxage=604800;must-revalidate";
        set beresp.http.max-age = "0";
        set beresp.http.s-maxage = "604800";
        unset beresp.http.set-cookie;
        return (deliver);
    }

    /* if we have teaser images,
    user can cache them in the local browser cache for a four weeks
    */
    if (bereq.url ~ "mood-galerie-images/") {
        # zip resources
        set beresp.do_gzip = true;
        set beresp.ttl = 86400s;
        set beresp.http.cache-control = "max-age=4233600;s-maxage=86400";
        set beresp.http.max-age = "4233600";
        set beresp.http.s-maxage = "86400";
        unset beresp.http.set-cookie;
        return (deliver);
    }

    /* cache font files, regardless of where they live */
    if (bereq.url ~ "\.(otf|ttf|woff|woff2)$") {
        set beresp.ttl = 86400s;
        set beresp.http.cache-control = "max-age=31536000;s-maxage=86400";
        set beresp.http.max-age = "31536000";
        set beresp.http.s-maxage = "86400";
        unset beresp.http.set-cookie;
        return (deliver);
    }

  # Cache Images
  if (bereq.url ~ "\.(jpg|gif|png|svg)$") {
      # zip resources
      set beresp.do_gzip = true;
      set beresp.ttl = 1209600s;
      set beresp.http.cache-control = "max-age=1209600;s-maxage=1209600";
      set beresp.http.max-age = "1209600";
      set beresp.http.s-maxage = "1209600";
#      set beresp.http.expires = "1209600";
      unset beresp.http.set-cookie;
      return (deliver);
  }

  /* cache resource files in resource registry */
  if (bereq.url ~ "\.(js|css|map)$") {
      # zip resources
      set beresp.do_gzip = true;
      set beresp.ttl = 31536000s;
      set beresp.http.cache-control = "max-age=31536000;s-maxage=31536000";
      set beresp.http.max-age = "31536000";
      set beresp.http.s-maxage = "31536000";
      # set beresp.http.expires = "31536000";
      unset beresp.http.set-cookie;
      return (deliver);
  }

  if (beresp.status >= 400 || beresp.status == 302) {
     set beresp.ttl = 0s;
  }

  /* should be the last rule */
  /* don't cache anything that looks like the login form, nor anything that has the __ac cookie */
  if (bereq.url ~ "/login_form$" || bereq.url ~ "/login$" || bereq.http.Cookie ~ "__ac" ) {
      # return (hit_for_pass);
      set beresp.uncacheable = true;
      set beresp.ttl = 10s;
      return (deliver);
  }


  set beresp.do_gzip = true;
  return (deliver);
}


// sub vcl_backend_error {
//       if (beresp.status == 503 && bereq.retries == 3) {
//           synthetic(std.fileread("/var/www/vhosts/mywebsite.ch/httpdocs/error_docs/503.html"));
//           return(deliver);
//        } else {
//           return(retry);
//        }
//  }


# vcl_backend_error: This subroutine is called if we fail the backend fetch.
# See https://www.varnish-cache.org/docs/4.0/users-guide/vcl-built-in-subs.html#vcl-backend-error
sub vcl_backend_error {

  /* Try to restart request in case of failure */
  #TODO# Confirm max_retries default value
  # SeeV3 https://www.varnish-cache.org/trac/wiki/VCLExampleRestarts
  if ( bereq.retries < 4 ) {
    return (retry);
  }

  /* Debugging headers */
  # Please consider the risks of showing publicly this information, we can wrap
  # this with an ACL.
  # Retry count
  if ( bereq.retries > 0 ) {
    set beresp.http.X-Varnish-Retries = bereq.retries;
  }

  set beresp.http.Content-Type = "text/html; charset=utf-8";
  set beresp.http.Retry-After = "5";
  synthetic( {"<!DOCTYPE html>
<html>
  <head>
    <title>"} + beresp.status + " " + beresp.reason + {"</title>
  </head>
  <body>
    <h1>Error "} + beresp.status + " " + beresp.reason + {"</h1>
    <p>"} + beresp.reason + {"</p>
    <h3>Something went wrong:</h3>
    <p>XID: "} + bereq.xid + {"</p>
    <hr>
    <p>Varnish cache server</p>
  </body>
</html>
"} );

  /* Bypass built-in logic */
  # We make sure no built-in logic is processed after ours returning at this
  # point.
  return (deliver);
}

sub vcl_deliver {
    # Happens when we have all the pieces we need, and are about to send the
    # response to the client.
    #
    # You can do accounting or modifying the final object here.

    set resp.http.X-Hits = obj.hits;
    if (obj.hits > 0) {
            set resp.http.X-Cache = "HIT";
    } else {
            set resp.http.X-Cache = "MISS";
    }
    set resp.http.X-Powered-By = "Plone";
}
