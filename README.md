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

\$ docker pull elasticsearch:7.14.1
\$ docker network create esearch
\$ docker run --publish 127.0.0.1:9200:9200 --name esearch \
  --net esearch -e "discovery.type=single-node" \
  elasticsearch:7.14.1

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


### Optional: run Kibana

Elasticsearch has a nice web frontend called kibana. You can 
run it with the following commands:

\$ docker pull kibana:7.14.1
\$ docker run --publish 127.0.0.1:5601:5601 --name kibana \
  --net esearch kibana:7.14.1

and then access kibana on 

  http://localhost:5601/
  
This is an optional step as most users will not need kibana.


## Getting started with data

To load some data into Elasticsearch, we provide a script in 
the "importers/" subdirectory named "segger-xml.py". Provided 
your Elasticsearch instance is listening at localhost:9200, 
you can run "segger-xml.py" with the segger xml file as first 
argument: 

  ./segger-xml.py jlink_dev_list.xml

The script will read the XML file and import its data into 
your local Elasticsearch instance. After that, you can try 
running some basic searches in the web frontend using the 
Elasticsearch described in this document:

https://www.elastic.co/guide/en/elasticsearch/reference/7.14/query-dsl-query-string-query.html#query-string-syntax

For example, you can search for 'Zilog' to find the first 
ten devices by this vendor, or try 'Zilog "Cortex-M0"' to 
find Zilog devices with this score. You can search within 
certain fields prepending your search string with its name 
and a colon (':'): 'vendor:Zilog AND core:"Cortex-M0"'. 

All searches and field names are case-insensitive, you can 
group parts of the query with parentheses and combine them 
logically with "AND" and "OR", while "OR" is the default. 

Please notice that the output is still very raw and by far 
not in a presentable shape, so please remember that we are 
still in an very early stage of development. Enjoy! ;-)


## Getting started with docker-compose

To run this software with docker-compose, you need to have 
-- surprise! -- docker and docker-compose installed. Then, 
you do the following steps from the root directory in this 
repository: 

$ (cd docker && docker build --tag chipselect .)

This will take some time to build your local docker image; 
please note that we run these commands in a subshell, thus
you will find yourself in the root directory after that is 
done. (You could also "cd docker; docker build...; cd .." 
instead, if you wish.) 

Then, we start our services with docker-compose from this 
root directory: 

$ docker-compose up

and you'll see a short message from our web service, then 
-- after a while -- followed by the looong output of the 
typical Java application that Elasticsearch is. When you 
run this the first time, the Elasticsearch docker image 
will have to be pulled from elastic.co's Docker Registry 
which will take some time. 

After a while, an empty Elasticsearch docker instance and 
our web fronend will run, so you can import data with the 
appropriate import scripts. There are two scripts in our 
"importers/" subdirectory, so run the following with the 
virtualenv (see above) activated -- please note that we 
have intentionally kept the data files out of this repo: 

$ cd importers
$ ./segger-xml.py <jlink_dev_list.xml>
$ ./microcontroller_and_processors-2020-08-14.py \
  <microcontroller_and_processors-2020-08-14.xlsx> 
  
Please note that Elasticsearch and its driver output a 
warning on an insecure installation. For us, this is 
completely pointless, as all network interfaces are 
strictly bound to our local network device... ;-) 

When everything is done, point your web browser to 

"http://localhost:5001/" 

and try some searches like "cortex AND DDR2"... 

Have fun! 

