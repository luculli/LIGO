# Dockerfile for LIGO Environment - v0.3
This folder contains a Dockerfile to setup the standard LIGO environment (i.e. LALSuite) following the description reported in https://wiki.ligo.org/Computing/LALSuiteInstall for Debian platform.

In order to setup the LAL Suite in your computer you have to:

* clone this folder
* run "make build-image" in order to build a local docker image

The LAL image can be started in several different ways:

* "make start-image" will create a detached container
* "make run-image" will create a container and it will start python
* "make run-bash" will create a container and it will start a bash shell
* "make stop-image" will stop the actual running LAL container

