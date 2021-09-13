# Chipselect
library of microcontrollers

## Install with development server

ATTENTION! This option is just for development purposes and shall
NEVER EVER be used in a production environment! 

Required: 
  - Python 3
  - virtualenv

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

$ virtualenv v3
$ source v3/bin/activate
$ pip install -r requirements.txt

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

$ cd docker/files/web/
$ flask run --debugger --reload --extra-files app/templates:app/static

This will run the development server on your localhost port 5000, 
if needed you can change this with the "--port" command line option
to "flask run". So, start your web browser and point it to the URL 
"http://localhost:5000/" and enjoy! 

