FROM ubuntu:18.04
LABEL maintainer="asdf134652@gmail.com"
LABEL version="1.0.0"
LABEL description="A test Docker image to understanding"

WORKDIR /home/


RUN apt-get update

RUN apt-get install -y sudo 

RUN apt-get install -y wget

RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb

RUN sudo apt install -y ./one-compiler_1.21.0_amd64.deb

RUN mkdir test

WORKDIR /home/test 

CMD ["onecc", "-C", "onecc.template.cfg"]