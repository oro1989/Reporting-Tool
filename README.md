Log Analysis Project - Reporting Tool
======

### This Project Project is part of Udacity's Full Stack Nanodegree program
### prerequisites:
1. virtual machine (VM) to run an SQL database server and the web app that uses it
  * [Install VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1):
   Currently, the supported version of VirtualBox to install is version 5.1. Newer versions do not work with the current release of Vagrant.
  * [Install Vagrant](https://www.vagrantup.com/downloads.html)
   Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.
2. Download the VM configuration:
  * download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip)
3. Start the virtual machine
  * From your terminal, inside the vagrant subdirectory of the downloaded configuraiton, run the command `vagrant up`
  * When vagrant up is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh`
4. Download the data
  * Next, [download the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.
  * Load the data, `cd` into the vagrant directory and use the command `psql -d news -f newsdata.sql`

### Run newsdata.py
* The program will connect to news database and execute the quries to answer 3 questions required by the project
