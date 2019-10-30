## ----------------------------------------------------------------------
## Dockerfile for LAL environment (Giulia)
## v. 0.1 - 20191029 G. Luculli
## ----------------------------------------------------------------------

# base image
FROM debian:8
LABEL maintainer="Gabriele LUCULLI"

# install linux packages 
RUN export DEBIAN_FRONTEND=noninteractive; apt-get -y  update \
  && apt-get install -y git-core libxml2-dev gsl-bin libfftw3-dev swig  gsl-bin libhdf5-dev libframe-dev sudo apt-utils \
  python-pip python-dev python-tk wget alien

# install LAL
RUN export DEBIAN_FRONTEND=noninteractive; apt-get install -y software-properties-common

RUN (gpg --batch --no-tty --keyserver pgp.mit.edu --recv-keys CE050D236DB6FA3F \
     ||  gpg --batch --no-tty --keyserver ha.pool.sks-keyservers.net --recv-keys CE050D236DB6FA3F                 \
     ||  gpg --batch --no-tty --keyserver keyserver.pgp.com --recv-keys CE050D236DB6FA3F )

RUN gpg -a --export CE050D236DB6FA3F | sudo apt-key add -
RUN export DEBIAN_FRONTEND=noninteractive; sudo add-apt-repository -y 'deb [trusted=yes] http://software.ligo.org/lscsoft/debian jessie contrib'
RUN export DEBIAN_FRONTEND=noninteractive; sudo apt-get update -y; sudo apt-get install -y lscsoft-archive-keyring; 
RUN export DEBIAN_FRONTEND=noninteractive; sudo apt-get install -y lal lal-python lal-octave

# get additional packages
RUN mkdir -p /home/user/packages
COPY ./packages/* /home/user/packages/

# install metaio
RUN tar -xvf /home/user/packages/metaio-8.4.0.tar.gz
RUN cd metaio-8.4.0; ./configure; make; make install

# install general python packages
COPY  ./requirements.txt .
RUN sudo pip install --upgrade pip
RUN sudo pip install -r requirements.txt
RUN rm ./requirements.txt

# install lal for python
RUN sudo pip install lalsuite

# working dir, env and user
RUN mkdir -p /home/user/src
RUN mkdir -p /home/user/data
WORKDIR /home/user
ENV DISPLAY :0

RUN useradd -s /bin/bash user -p ""
RUN adduser user sudo
RUN chown -R user:user /home/user

USER user

## -- start
CMD ["python"]
