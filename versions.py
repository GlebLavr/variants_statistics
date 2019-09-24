import os
import json

def pkgs_and_version():

    lines = os.popen('dpkg -l | grep "^ii"').read().split('\n')[5:-1]
    i = 0
    while len([l for l in lines[i].split('  ') if l]) != 4:
        i += 1
    offsets = [lines[i].index(l) for l in lines[i].split('  ') if len(l)]
    pkgs = {}
    for line in lines:
        parsed = []
        for i in range(len(offsets)):
            if len(offsets) == i + 1:
                parsed.append(line[offsets[i]:].strip())
            else:
                parsed.append(line[offsets[i]:offsets[i + 1]].strip())

        name = parsed[1].split()[0]
        version = parsed[1].split()[1]
        pkgs.update({name:{'version':version}})
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

aptget_dict = find_command_aptget(pkgs)

apt_dict = find_command_apt(pkgs)
command_dict = {**apt_dict, **aptget_dict}
x = json.dumps(command_dict, indent=3)
print(x) 
