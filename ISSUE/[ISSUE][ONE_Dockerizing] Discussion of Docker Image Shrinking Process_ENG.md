```suggestion
RUN apt-get update && apt-get install -qqy --no-install-recommends \
  wget \
  && rm -rf /var/lib/apt/lists/*
```

from https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#run

_Originally posted by @jyoungyun in https://github.com/Samsung/ONE/pull/9722#discussion_r972576673_

Related Issue : #9721 #9712 
### Why?

Based on your opinion, we tried to include `--no-install-recommends`, `rm-rf/var/lib/apt/lists/*` in the Docker execution process.

### How?

However, there was a problem in this process.
1. Related to `--no-install-recommends`
Adding `--no-install-recommends` does not apply `--no-check-certificate`, which seems to cause https authentication problems. I am attaching my error log.

```
--2022-09-16 05:42:53--  https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb
Resolving github.com (github.com)... 20.200.245.247
Connecting to github.com (github.com)|20.200.245.247|:443... connected.
ERROR: cannot verify github.com's certificate, issued by 'CN=DigiCert TLS Hybrid ECC SHA384 2020 CA1,O=DigiCert Inc,C=US':
  Unable to locally verify the issuer's authority.
To connect to github.com insecurely, use `--no-check-certificate'
```

2. Related to `rm -rf/var/lib/apt/lists/*`
Applying `rm -rf /var/lib/apt/lists/*` before installing the debian package results in dependency issues for python 3.8. I am attaching my error log.

```
The following packages have unmet dependencies:
 one-compiler : Depends: python3-venv but it is not installable
                Depends: python3-pip but it is not installable
                Depends: python3.8 but it is not installable
                Depends: python3.8-venv but it is not installable
E: Unable to correct problems, you have held broken packages.
The command '/bin/sh -c wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb &&    apt-get install -y ./one-compiler_1.21.0_amd64.deb      && rm -rf /var/lib/apt/lists/*' returned a non-zero code: 100
```

3. Attached is an example of the last successful docker file.

After considering these examples, it is not clear yet whether you would like to install additional packages, so we were able to successfully build the image after uninstalling them for both options. Can you give me your opinion on this content?

```
FROM ubuntu:18.04 

RUN apt-get update && apt-get install -qqy \ 
    wget \ 
    && apt clean 
 
RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb \ 
    && apt-get install -y ./one-compiler_1.21.0_amd64.deb \ 
    && rm -rf /var/lib/apt/lists/* 
 
ENTRYPOINT ["onecc"] 
```

After considering these examples, it is not clear yet whether you would like to install additional packages, so we were able to successfully build the image after uninstalling them for both options. Can you give me your opinion on this content?

/cc [@Samsung/ootpg](https://github.com/orgs/Samsung/teams/ootpg)