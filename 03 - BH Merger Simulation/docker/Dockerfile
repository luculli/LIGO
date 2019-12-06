## ----------------------------------------------------------------------
## Dockerfile for BH Merging Simulation
## v. 0.1 - 20191204 G. Luculli
## ----------------------------------------------------------------------

# base image
FROM debian:8
LABEL maintainer="Gabriele LUCULLI"

# install linux packages 
RUN export DEBIAN_FRONTEND=noninteractive; apt-get -y  update \
  && apt-get install -y git-core libxml2-dev gsl-bin libfftw3-dev swig  gsl-bin libhdf5-dev libframe-dev sudo apt-utils \
  python-pip python-dev python-tk wget alien

# install general python packages
COPY  ./requirements.txt .
RUN sudo pip install --upgrade pip
RUN sudo pip install -r requirements.txt

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

# working dir
RUN mkdir -p /home/user/src
RUN mkdir -p /home/user/data
WORKDIR /home/user
ENV DISPLAY :0

# user definition
RUN useradd -s /bin/bash user -p ""
RUN adduser user sudo
RUN chown -R user:user /home/user

USER user

## -- start
CMD ["python3.6"]
