def write_dockerfile(version,argument) :
    with open('Dockerfile', 'w', encoding='utf-8') as f: 
        f.write('FROM ubuntu:18.04 \n')
        f.write('RUN apt-get update \n')
        f.write('RUN apt-get install -y wget \n')
        f.write(f'RUN wget https://github.com/Samsung/ONE/releases/download/{version}/one-compiler_{version}_amd64.deb \n')
        f.write(f'RUN apt install -y ./one-compiler_{version}_amd64.deb \n')
        f.write('WORKDIR /home/ \n')
        f.write('RUN mkdir test \n')
        f.write('WORKDIR /home/test \n')
        f.write(f'CMD {argument}')


write_dockerfile('1.21.0',["onecc", "-C", "onecc.template.cfg"])