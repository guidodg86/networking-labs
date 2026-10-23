#imports
from jinja2 import Environment, FileSystemLoader
import yaml
import os

#Getting current path
path_current_file = __file__
current_path_splitted = path_current_file.split("/")[1:-1]
file_dir = ""
for element in current_path_splitted:
    file_dir = file_dir + "/" + element

#parse yaml and get certificate
with open(f'{file_dir}/context_data.yaml', 'r') as f:
    context_data = yaml.load(f, Loader=yaml.SafeLoader)

#Loading jinja templates for the config
environment = Environment(loader=FileSystemLoader(f"{file_dir}/jinja_templates/"))
template_loopback = environment.get_template("core_loopback.jinja")
template_vrf = environment.get_template("core_vrf.jinja")
template_p2p = environment.get_template("core_p2p.jinja")
template_ospf = environment.get_template("core_ospf.jinja")

# Creating list of vpn
d_list_of_vpn = []
for env in context_data["envs"]:
    d_list_of_vpn.append(env["vpn"])
list_of_vpn = set (d_list_of_vpn)

#Creating the bulk of subnets for each site and the vpn
commands ={}
for site in context_data["sites"]:
    commands[site["site_name"]] = {}
    commands[site["site_name"]]["vrf"] = []
    commands[site["site_name"]]["loopbacks"] = []
    commands[site["site_name"]]["p2p"] = []
    commands[site["site_name"]]["ospf"] = []
    for vpn in list_of_vpn:
        vpn_name = f"vpn_{vpn}"
        vrf_command = template_vrf.render(
            vrf_name = vpn_name)
        commands[site["site_name"]]["vrf"].append(vrf_command)
        ospf_command = template_ospf.render(
            ospf_process = vpn_name,
            vrf_name = vpn_name)
        commands[site["site_name"]]["ospf"].append(ospf_command)
    for i,env in enumerate(context_data["envs"]):
        ip_address = f"10.{site["site_id"]}.{env["octet"]}.1"
        mask = "255.255.255.0"
        vrf_name = f"vpn_{env["vpn"]}"
        loopback_command = template_loopback.render(
            vrf_name = vrf_name,
            loopback_number = i,
            ip_address = ip_address, 
            mask = mask)
        commands[site["site_name"]]["loopbacks"].append(loopback_command) 
    for i,vpn in enumerate(list_of_vpn):
        vrf_name = f"vpn_{vpn}"
        ip_address = f"192.168.{site["site_id"]}.{2*i}"
        mask = "255.255.255.254"
        p2p_commands = template_p2p.render(
            vrf_name = vrf_name,
            vlan = vpn,
            ip_address = ip_address, 
            mask = mask)
        commands[site["site_name"]]["p2p"].append(p2p_commands)


for site in commands:
    with open(f"{file_dir}/results/core_routers/{site}_commands.txt", "w") as f:
        for vrf in commands[site]["vrf"]:
            f.write(vrf)
        for loopback in commands[site]["loopbacks"]:
            f.write(loopback)
        # Putting interface as layer 3
        f.write("int Gi0/0\n  no switchport\n!\n")
        for p2p in commands[site]["p2p"]:
            f.write(p2p)
        for ospf_p in commands[site]["ospf"]:
            f.write(ospf_p)



pass
