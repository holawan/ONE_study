FROM ubuntu:18.04 

RUN apt update -y && \ 
	 apt install -y \ 
	 wget && \ 
	 apt clean 
RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb && \ 
	 apt-get install -y ./one-compiler_1.21.0_amd64.deb 
ENTRYPOINT ["onecc"]