import subprocess
import sys 

#이미지가 있는지 없는지 

def _is_image(version) : 
    cmd = ['docker', 'images', version]
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

print(_is_image('onecc:1.21.0'))
