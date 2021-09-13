# Chipselect
library of microcontrollers

## Install the development server

ATTENTION! This option is just for development purposes and shall
NEVER EVER be used in a production environment! 

Required: 
  - Python 3
  - virtualenv
  - Elasticsearch

First, install Python3 (version 3.8.10 used for development, but 
most other versions should work, too) and virtualenv. For mostly 
all Linux distributions based on Debian GNU/Linux, you can find 
virtualenv in the package "python3-virtualenv". Users of other 
operating systems please make sure that you install a version of
virtualenv that was built for your Python version. Please note 
that the installation of virtualenv depends on a lot of packages 
in order to build binaries from source and thus will install a 
complete compiler toolchain on your system. 

Then, with these both installed, take the following steps in the 
root directory of this code (the directory this file is in):

\$ virtualenv v3
\$ source v3/bin/activate
\$ pip install -r requirements.txt

These commands will create a virtualenv (virtual environment) for 
Python and install a copy of your Python interpreter and several 
needed tools into the directory "v3/", which will stay completely 
separate from your system's installation. Thus, anything you will 
install in this directory will not affect your system, but only 
this one directory. After you activate the virtualenv, you will 
probably notice that your command prompt has been prepended with 
the directory name of your virtualenv. You can always leave your 
virtualenv using the command "deactivate" and re-enter it using 
the "source" command shown above. In the third command, the pip
command will download and install all required Python packages, 
and then you are ready to go. 

After these steps, head over into "docker/files/web" and start 
the development server: 

\$ cd docker/files/web/
\$ flask run --debugger --reload --extra-files app/templates:app/static

This will run the development server on your localhost port 5000, 
if needed you can change this with the "--port" command line option
to "flask run". So, start your web browser and point it to the URL 
"http://localhost:5000/" and enjoy! 

In order to do something useful with the application, an install 
of Elasticsearch is necessary. We will ease the process for the 
moment and install Elasticsearch as a Docker image. First, we'll 
download the image, and then run it as follows: 

\$ docker pull docker.elastic.co/elasticsearch/elasticsearch:7.14.1
\$ docker run --publish 127.0.0.1:9200:9200 --name esearch \
  -e "discovery.type=single-node" \
  docker.elastic.co/elasticsearch/elasticsearch:7.14.1

(The last command has been split at the backslashes ("\") to fit.)

ATTENTION! For performance reasons, Elasticsearch assumes to run 
on a dedicated server and preallocate little more than 50% of the
machine's overall memory. This should not be necessary for this 
application, thus you should restrict the available memory for at 
least 2 GiB in your "docker run" or "docker create" commands. But 
although 2 GiB should work fine, with more allocated memory (such
as 4 or better 8 GiB) you might experience a better performance. 
So, if you'd wish to limit Elasticsearchs memory usage, please 
use the "--memory" command line option for your "docker run" and
"docker create" commands. 

To make sure Elasticsearch is running and locally reachable, try 
the following command: 

\$ curl -XGET 'http://localhost:9200/'

The output should look something like: 

--snip-----
{
  "name" : "6049f5cd496e",
  "cluster\_name" : "docker-cluster",
  "cluster\_uuid" : "gSCkvVK4SlSLL\_erRwo9EA",
  "version" : {
    "number" : "7.14.1",
    "build\_flavor" : "default",
    "build\_type" : "docker",
    "build\_hash" : "66b55ebfa59c92c15db3f69a335d500018b3331e",
    "build\_date" : "2021-08-26T09:01:05.390870785Z",
    "build\_snapshot" : false,
    "lucene_version" : "8.9.0",
    "minimum\_wire\_compatibility\_version" : "6.8.0",
    "minimum\_index\_compatibility\_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
--snap-----

If you see this output, everything should work fine. Have fun!

