import os
import json

def pkgs_and_version():
    os.system('dpkg -l | grep "^ii" | cat > versions.txt')
    fh = open('versions.txt')
    lines = []
    pkgs = {}
    while True:
        line = fh.readline()
        if not line:
            break
        name = line.split()[1]
        version = line.split()[2]
        pkgs[name] = version
    fh.close()
    return pkgs
    return pkgs

pkgs = pkgs_and_version()

def find_command_aptget(pkgs):

    line_found = os.popen('zgrep "Commandline: apt-get install -y" /var/log/apt/history.log').read()
    command_list = line_found.split("\n")[:-1]

    commands = []
    for cnt, command in enumerate(command_list):
        command_list[cnt] = command[32:]
        for el in command_list[cnt].split():
            commands.append(el)
            
    command_dict = {}
    for command in commands:
        command_dict[command] = pkgs[command]
            
    return command_dict


def find_command_apt(pkgs):

    line_found = os.popen('zgrep "Commandline: apt install -y" /var/log/apt/history.log').read()
    command_list = line_found.split("\n")[:-1]

    commands = []
    for cnt, command in enumerate(command_list):
        command_list[cnt] = command[28:]
        for el in command_list[cnt].split():
            commands.append(el)
            
    command_dict = {}
    for command in commands:
        command_dict[command] = pkgs[command]
            
    return command_dict

aptget = os.popen('zgrep "Commandline: apt-get install -y" /var/log/apt/history.log').read()
if aptget:
    aptget_dict = find_command_aptget(pkgs)

apt = os.popen('zgrep "Commandline: apt install -y" /var/log/apt/history.log').read()
if apt:    
    apt_dict = find_command_apt(pkgs)
command_dict = {**apt_dict, **aptget_dict}
x = json.dumps(command_dict, indent=3)
print(x) 
