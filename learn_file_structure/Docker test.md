# Docker test

### 1. 실패 

- `--no-install-recommends` 적용하면 `--on-check-certificate` 문제 발생 

```
RUN apt-get update && apt-get install -qqy --no-install-recommends \
	  wget \
	  && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb && \ 
	 apt-get install -y ./one-compiler_1.21.0_amd64.deb \
	 && rm -rf /var/lib/apt/lists/*
```



```
--2022-09-16 05:42:53--  https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb
Resolving github.com (github.com)... 20.200.245.247
Connecting to github.com (github.com)|20.200.245.247|:443... connected.
ERROR: cannot verify github.com's certificate, issued by 'CN=DigiCert TLS Hybrid ECC SHA384 2020 CA1,O=DigiCert Inc,C=US':
  Unable to locally verify the issuer's authority.
To connect to github.com insecurely, use `--no-check-certificate'
```

### 2. 실패

- `rm -rf /var/lib/apt/lists/*` 적용하면 python 의존성 문제 발생 

```
RUN apt-get update && apt-get install -qqy \
	  wget \
	  && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb && \ 
	 apt-get install -y ./one-compiler_1.21.0_amd64.deb \
	 && rm -rf /var/lib/apt/lists/*
```



```
The following packages have unmet dependencies:
 one-compiler : Depends: python3-venv but it is not installable
                Depends: python3-pip but it is not installable
                Depends: python3.8 but it is not installable
                Depends: python3.8-venv but it is not installable
E: Unable to correct problems, you have held broken packages.
The command '/bin/sh -c wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb &&    apt-get install -y ./one-compiler_1.21.0_amd64.deb      && rm -rf /var/lib/apt/lists/*' returned a non-zero code: 100
holawan@DESKTOP-KVCQHCD:~/test$ 
```



### 3. 내잘못 실패 

```
RUN apt-get update && apt-get install -qqy \
	  wget \
	  # && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb && \ 
	 apt-get install -y ./one-compiler_1.21.0_amd64.deb \
	 && rm -rf /var/lib/apt/lists/*
```



```
Reading package lists...
E: Unable to locate package RUN
E: Unable to locate package https://github.com/Samsung/ONE/releases/download/1.21.0
E: Couldn't find any package by glob 'https://github.com/Samsung/ONE/releases/download/1.21.0'
E: Couldn't find any package by regex 'https://github.com/Samsung/ONE/releases/download/1.21.0'
The command '/bin/sh -c apt-get update && apt-get install -qqy    wget RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb &&         apt-get install -y ./one-compiler_1.21.0_amd64.deb       && rm -rf /var/lib/apt/lists/*' returned a non-zero code: 100
```



### 4. 

```
RUN apt-get update && apt-get install -qqy \
	  wget \
	  # && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb && \ 
	 apt-get install -y ./one-compiler_1.21.0_amd64.deb \
	#  && rm -rf /var/lib/apt/lists/*
```

```
## 성공
RUN apt-get update && apt-get install -qqy \
	  wget \
	  # && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb && \ 
	 apt-get install -y ./one-compiler_1.21.0_amd64.deb \
	#  && rm -rf /var/lib/apt/lists/*
```



### 5. 성공

```
FROM ubuntu:18.04 

RUN apt update -y && \ 
	 apt install -y \ 
	 wget && \ 
	 apt clean 
RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb && \ 
	 apt-get install -y ./one-compiler_1.21.0_amd64.deb 
```

```
Successfully built 289c357f80d8
Successfully tagged test:2
```



### 6. 

```
FROM ubuntu:18.04 

RUN apt-get update && apt-get install -qqy \
	 wget && \ 
	 apt clean 
RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb && \ 
	 apt-get install -y ./one-compiler_1.21.0_amd64.deb 
```



```
Successfully built 5930a105ccb1
Successfully tagged test:2
```



### 7. 

```
FROM ubuntu:18.04 

RUN apt-get update && apt-get install -qqy \
	 wget && \ 
	 rm -rf /var/lib/apt/lists/*
RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb && \ 
	 apt-get install -y ./one-compiler_1.21.0_amd64.deb 
```

```
The following packages have unmet dependencies:
 one-compiler : Depends: python3-venv but it is not installable
                Depends: python3-pip but it is not installable
                Depends: python3.8 but it is not installable
                Depends: python3.8-venv but it is not installable
E: Unable to correct problems, you have held broken packages.
```



### 8.

```

FROM ubuntu:18.04 

RUN apt-get update && apt-get install -qqy --no-install-recommends \
	  wget
RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb && \ 
	  apt-get install -y ./one-compiler_1.21.0_amd64.deb 
```

```
--2022-09-16 05:55:37--  https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb
Resolving github.com (github.com)... 20.200.245.247
Connecting to github.com (github.com)|20.200.245.247|:443... connected.
ERROR: cannot verify github.com's certificate, issued by 'CN=DigiCert TLS Hybrid ECC SHA384 2020 CA1,O=DigiCert Inc,C=US':
  Unable to locally verify the issuer's authority.
To connect to github.com insecurely, use `--no-check-certificate'.
```



### 9. 

```
FROM ubuntu:18.04 

RUN apt-get update && apt-get install -qqy \
	  wget \ 
	  && apt clean 
RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb \ 
	  && apt-get install -y ./one-compiler_1.21.0_amd64.deb  \
    && rm -rf /var/lib/apt/lists/*
```

```
```

