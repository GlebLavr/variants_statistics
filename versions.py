import os
import json

def find_command_aptget():

    line_found = os.popen('zgrep "Commandline: apt-get install -y" /var/log/apt/history.log').read()
    command_list = line_found.split("\n")[:-1]

    commands = []
    for cnt, command in enumerate(command_list):
        command_list[cnt] = command[32:]
        for el in command_list[cnt].split():
            commands.append(el)
            
    return commands


def find_command_apt():

    line_found = os.popen('zgrep "Commandline: apt install -y" /var/log/apt/history.log').read()
    command_list = line_found.split("\n")[:-1]

    commands = []
    for cnt, command in enumerate(command_list):
        command_list[cnt] = command[28:]
        for el in command_list[cnt].split():
            commands.append(el)

    return commands

aptget_var = find_command_aptget()
apt_var = find_command_apt()


def conc_apts(aptget_var, apt_var):
    names = []
    if aptget_var and apt_var:
        names = aptget_var + apt_var
    if not apt_var[0]:
        names = aptget_var
    if not aptget_var[0]:
        names = apt_var
    return final_list


names = conc_apts(aptget_var, apt_var)

def get_versions(names):
    versions = []
    for name in names:
        
        apt_cache_str = 'apt-cache policy ' + str(name) 
        apt_cache = os.popen(apt_cache_str).read()
        lines = apt_cache.split('\n')
        version = lines[4][5:-4]
        versions.append(version)
   
    return versions
    
    
versions = get_versions(names)

def create_json(names, versions):
    apt_dict = {}
    
    for name, version in zip(names, versions):
        apt_dict[name] = version
        
    return apt_dict

apt_dict = create_json(names, versions)
x = json.dumps(apt_dict, indent=3)
print(x)



