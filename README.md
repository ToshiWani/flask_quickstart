# flask_quickstart
Flask Quickstart with MongoDB on Ubuntu Server 18.0.4


## Preparation

Use the following two commands to check which version of Python 3 is installed. The python version should be 3.6.x and the location `/usr/bin/python3`

```bash
$ python3 --version
$ which python3
```

Install following packages after upgrading

```bash
$ sudo apt update && sudo apt upgrade
$ sudo apt install python3-dev python3-pip python3-virtualenv
```

Install Apache server if it is not installed yet.

```bash
$ sudo apt install apache2 apache2-dev
```


## Clone this quickstart

Clone this quickstart project under Apache's document directory `/var/www`. And, give permission to www-
```bash
$ git clone https://github.com/ToshiWani/flask_quickstart.git /var/www/flask_quickstart
$ sudo chown -R www-data:www-data /var/www/flask_quickstart/
$ sudo chmod -R 775 /var/www/flask_quickstart/
```


## Virtual Environment

Upgrade pip and setuptools to the latest version

```bash
$ pip3 install --upgrade pip setuptools
```

Create a shared venv location in a user-neutral directory, and make it group-readable

```bash
$ sudo mkdir /usr/local/share/venvs
$ sudo chown -R www-data:www-data /usr/local/share/venvs/
$ sudo chmod -R 775 /usr/local/share/venvs/
```

Create virtual environment

```bash
$ python3 -m venv /usr/local/share/venvs/flask_quickstart_venv
```

Active the virtualenv

```bash
$ source /usr/local/share/venvs/flask_quickstart_venv/bin/activate
```

At this point, virtual environment should be activated.  Your SSH terminal should looks like this:

```bash
(flask_quickstart_venv) username@yourmachine:~$ 
```

## Setup apache server

To run Flask on Apache server, we need to install a gateway interface called WSGI (Web Server Gateway Interface)

```bash
$ pip3.6 install mod_wsgi
```

Next, we need to linkup the shared object file and home directory of WSGI.

```bash
$ mod_wsgi-express module-config

LoadModule wsgi_module "/usr/local/share/venvs/flask_quickstart_venv/lib/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so"
WSGIPythonHome "/usr/local/share/venvs/flask_quickstart_venv"
```

Open the `wsgi.load` file and replace the contents with the two lines of codes generated the previous step. (You may want to keep the backup of the file before overwrite it.)
```bash
$ sudo cp /etc/apache2/mods-available/wsgi.load /etc/apache2/mods-available/wsgi.load.bak
$ sudo vim /etc/apache2/mods-available/wsgi.load
```

Enable updated WSGI and restart Apache server
```bash
$ sudo a2enmod wsgi
$ sudo service apache2 restart
```

## Update VirtualHost

Restore packages from `requirements.txt`

```bash
$ pip3.6 install -r /var/www/flask_quickstart/requirements.txt
```

Create `flask_quickstart.wsgi` file 
```bash
$ vim /var/www/flask_quickstart/flask_quickstart.wsgi
```

Copy, paste and save the following lines into the `flask_quickstart.wsgi` file.
```python
#!/usr/bin/python3.6
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/flask_quickstart/")

from flask_quickstart import app as application

```

Create a new virtual host file `flask_quickstart.conf` 
```bash
$ sudo vim /etc/apache2/sites-available/flask_quickstart.conf
``` 
 
Paste the content below. Replace the `ServerName` parameter for your own server IP address. If it is not sure, use the IP address of the `inet` by running the `ifconfig` command.  Please note that the `flask_quickstart` directory is under another `flask_quickstart`. This is not an error.  Also make sure that the `flask_quickstart.wsgi` file is under the first `flask_quickstart` directory.
```xml
<VirtualHost *:80>
     ServerName xxx.xxx.xxx.xxx
     ServerAdmin your@email.com
     WSGIScriptAlias / /var/www/flask_quickstart/flask_quickstart.wsgi
     <Directory /var/www/flask_quickstart/flask_quickstart/>
        Order allow,deny
        Allow from all
     </Directory>
     ErrorLog ${APACHE_LOG_DIR}/flask_quickstart-error.log
     LogLevel warn
     CustomLog ${APACHE_LOG_DIR}/flask_quickstart-access.log combined
</VirtualHost>
```

So far, your Apache document `/var/www/flask_quickstart` directory would look like this...

```
/var/www/flask_quickstart
├── flask_quickstart
│   ├── __init__.py
│   └── templates
│       └── index.html
├── flask_quickstart.wsgi
├── README.md
└── requirements.txt
```


Activate the virtual host and restart Apache

```bash
$ sudo a2ensite flask_quickstart.conf
$ sudo service apache2 restart
```