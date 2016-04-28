# Pypiserver

2016-04-28 AWPUG Pypiserver Tal

Author: Matthew Planchard
E-mail: msplanchard@gmail.com


# Introduction

### About Me
* M.S. in Biochemistry (???) from USM
* Moved to Austin in 2014
* Started working for Ihiji in December
* Python applications for embedded devices
* Started maintaining pypiserver early this year

### What is pypiserver?
* Minimal, lightweight server
* Works with pip & standard Python install tools

### Who is this talk for?
* Custom application/library writers
* Forkers
* People who need 100% availability of critical packages
* People who need old versions of packages
* Teams who want to more easily share code
* Open source groups who want to test deployment before uploading to 
the **real** PyPI

### Caveats
* This talk is not about packaging
* Won't be covering 100% of functionality
* There are other pacakges that do similar things
    * Devpi
    * [others](http://stackoverflow.com/questions/1235331/how-to-roll-my-own-pypi)


# Getting Started

### Installation on Ubuntu 14.04 & First Steps

From a non-root user's home directory:

> `pyvenv-3.4 .`
> `source bin/activate`
> `pip install pypiserver`
> `mkdir packages`
> `sudo bin/pypi-server -p 80 packages`

We can now access pypiserver via a web browser (52.39.114.20)

Let's upload a package the old-fashioned way from our local machine

> `scp awpug_sample_package-1.0.0-py3-none-any.whl awpug_aws:~/packages`

The web interface should now reflect the presence of this package

Let's install our package with pip from our local machine

> `pip install --extra-index-url http://52.39.114.20/simple \`
> `--trusted-host 52.39.114.20 awpug_sample_package`
> `awpug`

### Enabling Uploads

> `rm packages/awpug_sample_package-1.0.0-py3-none-any.whl`
> `pip install passlib`
> `htpasswd -sc htpasswd.txt pypi_user` (pypi_test as pw)
> `sudo bin/pypi-server -p 80 -P htpasswd.txt packages`

Configure `~/.pypirc` on the local machine:

````
[distutils]
index-servers =
    awpug

[awpug]
repository = http://52.39.114.20
username = pypi_user
password = pypi_test
````

> `twine upload -r awpug ./*`

### Authentication

Use the same htpasswd file to enable authentication

Updates, web portal access, and downloads can be restricted

Let's restrict portal access and downloads:

> `sudo bin/pypi-server -p 80 -P htpasswd.txt -a list,download packages`

Now let's see if we can see packages on the web server

And whether we can download something locally

### Mirroring PyPI packages

> `cd packages`
> `pip install -d . requests`

From our local machine, let's handicap /etc/hosts so we can't access PyPI

And then reinstall the requests package

# Next steps

* No built-in support for SSL, so it's probably best to put it behind
 another webserver
* (Premature?) optimization

### nginx proxy config (SSL)

* Set up pypiserver to listen on a high-numbered port
* Configure nginx to act as a reverse proxy to pypiserver

````
upstream pypi {
    server 127.0.0.1:7001 fail_timeout=10s;
}

server {
    listen 80;
    server_name pypi.me.com;
    rewrite ^ https://$server_name$request_uri? permanent;
}

server {
   listen 443 ssl;
   server_name pypi.me.com;

    ssl_certificate         /etc/ssl/certs/my_cert.crt;
    ssl_certificate_key     /etc/ssl/private/my_keyfile;

    ssl_session_timeout 5m;
    ssl_protocols SSLv3 TLSv1;
    ssl_ciphers HIGH:!ADH:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
    	proxy_read_timeout 600;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        add_header Pragma "no-cache";
        proxy_pass http://pypi;
    }
}
````


### nginx config with caching

Note this is very similar to the nginx config used by the real PyPI

````
upstream pypi {
    server 127.0.0.1:7001 fail_timeout=10s;
}

proxy_cache_path /var/lib/nginx/pypi levels=1:2 keys_zone=pypi:16m inactive=1M max_size=1G;

server {
    listen 80;
    server_name pypi.me.com;
    rewrite ^ https://$server_name$request_uri? permanent;
}

server {
    listen 443 ssl;
    server_name pypi.me.com;

    ssl_certificate         /etc/ssl/certs/my_cert.crt;
    ssl_certificate_key     /etc/ssl/private/my_keyfile;

    ssl_session_timeout 5m;
    ssl_protocols SSLv3 TLSv1;
    ssl_ciphers HIGH:!ADH:!MD5;
    ssl_prefer_server_ciphers on;

    proxy_cache pypi;
    proxy_cache_key $uri;
    proxy_cache_lock on;
    proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;

    location / {
    	proxy_read_timeout 600;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        add_header Pragma "no-cache";
        proxy_pass http://pypi;
        proxy_cache_valid any 5m;
    }
}
````

The above config is capable of serving hundreds (if not thousands) of
packages per minute

### Monitoring and starting with supervisord

> `sudo apt install supervisor`

Add the following config file at `/etc/supervisor.d/pypiserver.conf`

````
[program:pypiserver]
command=/home/ubuntu/bin/pypi-server -p 7001 -P /home/ubuntu/htpasswd.txt /home/ubuntu/packages
process_name=%(program_name)s
numprocs=1
numprocs_start=0
priority=999
autostart=true
autorestart=true
startsecs=1
startretries=3
exitcodes=0,2
stopsignal=TERM
stopwaitsecs=10
user=pypi
redirect_stderr=false
directory=/home/ubuntu
serverurl=AUTO
````

> `sudo service supervisor start`

# Questions?
