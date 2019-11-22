## ----------------------------------------------------------------------
## Dockerfile for LAL environment (Giulia)
## v. 0.3 - 20191121 G. Luculli
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

# install lal for python
RUN sudo pip install lalsuite

# install cpnest and its dependencies for python
RUN export DEBIAN_FRONTEND=noninteractive; apt-get install -y python-pyrex pyrex-mode
RUN sudo pip install pyrex cpnest

# install python3.6
RUN export DEBIAN_FRONTEND=noninteractive; sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev

RUN cd /tmp; wget https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tgz; \
tar xvf Python-3.6.9.tgz; \
cd Python-3.6.9; \
./configure --enable-shared --with-ensurepip=install; \
make -j8 build_all; \
sudo make install ; sudo ldconfig

# install general python 3.6 packages
RUN sudo pip3.6 install -r requirements.txt
RUN rm ./requirements.txt

# install lal for python3.6
RUN sudo pip3.6 install lalsuite

# install cpnest and its dependencies for python3.6
RUN sudo pip3.6 install cpnest

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
