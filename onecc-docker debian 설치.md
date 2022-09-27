# onecc-docker debian 설치

### 빌드 및 설치 

```
1. 패키지 빌드
$ dpkg-buildpackage -us -uc -d
2. 생성된 패키지 파일로 onecc-docker 설치
$ sudo apt-get install -y ./onecc-docker_1.0.0_amd64.deb
```



### 재설치

```
sudo apt-get install --reinstall -y ./onecc-docker_1.0.0_amd64.deb
```

