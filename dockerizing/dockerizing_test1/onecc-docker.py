import sys
import subprocess
from distutils.version import StrictVersion
import json

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

def main():
    # python 3에서는 print() 으로 사용합니다.
    installed_onecc_version = sys.argv[1]
    versions_str = subprocess.check_output("curl -s https://api.github.com/repos/Samsung/ONE/tags", shell=True ,encoding='utf-8')
    versions_json = json.loads(versions_str)
    versions = []
    for i in versions_json:
        versions.append(i["name"])
    # print(versions_str)
    # print(type(versions_str))
    # print(versions)
    versions.sort(key=StrictVersion)
    chosen_version = ""
    while 1:
        for i in range(18, len(versions)):
            print(versions[i])
        chosen_version = input("choose version: ")
        flag = False
        for i in range(18, len(versions)):
            if(chosen_version == versions[i]):
                flag = True
                break
        if(flag):
            break
        else:
            print("choose right version")
    if(chosen_version == installed_onecc_version):
        print("onecc is installed in computer")
        onecc_cmd = ["onecc"] + sys.argv[2:]
        subprocess.call(onecc_cmd)
        # 설치된 onecc 버전이 선택한 버전과 같을 때 onecc에 포워딩!
        exit(0)
    # 설치된 onecc 버전이 선택한 버전과 다를 때 dockerfile 작성
    if(not _is_image(chosen_version)):
        print(chosen_version)

if __name__ == "__main__":
	main()