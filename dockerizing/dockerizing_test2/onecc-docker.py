#!/usr/bin/env bash
''''exec "python3" "onecc-docker-recent.py" "$@" #'''

import sys
import subprocess
import json
import os
import re
import requests


def _is_image(version) : 
    cmd = ['docker', 'images', f'onecc:{version}']
    p = subprocess.Popen(cmd,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
    out, err = p.communicate()
    dic = {}

    decoded_out = [i.split() for i in out.decode().split("\n") if len(i)]

    if len(decoded_out) <2 :
        return False

    dic[decoded_out[0][0]] = decoded_out[1][0]
    dic[decoded_out[0][1]] = decoded_out[1][1]

    tag_name = cmd[2].split(':')

    if dic['REPOSITORY'] == tag_name[0] and dic['TAG'] == tag_name[1]  :
        return True 
    else :
        return False

def write_dockerfile(script_path,version) :

    with open(f'{script_path}/Dockerfile', 'w', encoding='utf-8') as dockerfile: 
        dockerfile.write('FROM ubuntu:18.04 \n\n')
        dockerfile.write('RUN apt update -y && \ \n')
        dockerfile.write('\t apt install -y \ \n')
        dockerfile.write('\t wget && \ \n')
        dockerfile.write('\t apt clean \n')
        dockerfile.write(f'RUN wget https://github.com/Samsung/ONE/releases/download/{version}/one-compiler_{version}_amd64.deb && \ \n')
        dockerfile.write(f'\t apt-get install -y ./one-compiler_{version}_amd64.deb \n')
        dockerfile.write('ENTRYPOINT ["onecc"]')


def main():
    onecc_version = subprocess.check_output("command -v onecc > /dev/null && echo $(onecc -v)", shell=True ,encoding='utf-8')
    installed_onecc_version = onecc_version.split(' ')[2]
    script_path = re.sub("\n", "", os.popen('pwd').read())
    versions_str = requests.get("https://api.github.com/repos/Samsung/ONE/tags").content
    versions_json = json.loads(versions_str)
    recent_version = versions_json[1]["name"]
    # recent_version='1.21.0'
    if(recent_version == installed_onecc_version):
        print("onecc is installed in computer")
        onecc_cmd = ["onecc"] + sys.argv[1:]
        subprocess.call(onecc_cmd)
        # 설치된 onecc 버전이 선택한 버전과 같을 때 onecc에 포워딩!
        exit(0)

    image_name = f"onecc:{recent_version}"

    if not _is_image(recent_version):
        write_dockerfile(script_path,recent_version)
        build_cmd = ["docker", "build", "-t", image_name, script_path]
        subprocess.call(build_cmd)

    contianer_name = f"onecc_{recent_version.replace('.','_')}"
    user_cmd = ''.join(sys.argv[1:])
    run_cmd = ["docker", "run", "--rm", "--name", contianer_name, "-v", "/home:/home", "--workdir", script_path, image_name, user_cmd]
    subprocess.run(run_cmd,shell=False)

if __name__ == "__main__":
	main()