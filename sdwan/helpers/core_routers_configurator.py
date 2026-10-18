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

# Creating list of vpn
d_list_of_vpn = []
for env in context_data["envs"]:
    d_list_of_vpn.append(env["vpn"])
list_of_vpn = set (d_list_of_vpn)

#Creating the bulk of subnets for each site and the vpn
for site in context_data["sites"]:
    for vpn in list_of_vpn:
        vpn_name = f"vpn_{vpn}"
        # Here need to render vrf/vpn template
    for i,env in enumerate(context_data["envs"]):
        ip_address = f"10.{site["site_id"]}.{env["octet"]}.1"
        mask = "255.255.255.0"
        vrf_name = f"vpn_ {env["vpn"]}"
        # Here need to render the interface loopback command

        pass



pass
