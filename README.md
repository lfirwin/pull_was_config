# Pull WebSphere Application Server (WAS) configuration into a centralized web site for viewing

## Overview
This project is a framework for centralizing WAS configurations into a centralized web site for viewing by a wide audience (developers, deployment managers, operations, etc.).

It is designed to run from a VM that has SSH access to VMs running the WAS Deployment Managers for the environments from which config data is to be gathered from.

This framework is presented as simply that, a framework, and could do with some major revamping and simplifying.

## Components
There are several components to the framework:
* Properties file that holds adhoc variables and an array of environments to process - gather_ree.props.
* A wsadmin Jython script to pull the configuration data and format the output file - gather_ree.py
* A shell script that controls the execution of the components - gather_ree.sh.
* A shell script that executes the wsadmin script on the target environent's deployment manager VM - gather_ree_ssh.sh.

The two shell scripts act in concert, and allow for multiple environments to be processed at once, as long as the deployment manager processes aren't running on the same VM.  
Deployment manager processes running on the same VM will be executed in the order they appear in the environment array.

This reduces the amount of time to gather this data across many environments.  

Output files will not be automatically updated in the home directory, unless there is a material change in the configuration.  The timestamp on the environment configuration web page indicates the last time the file was updated, and can provide a guesstimate as to when an actual change was made to the WAS configuration.  If cron is used to schedule the runs on a fairly frequent basis, this narrows the timeframe even more.

## HTML vs. XML
The wsadmin Jython script outputs both XML and HTML.  An included XSL file can be used to view XML files in a web browser.  (Yes, why both - it's a long story.)
