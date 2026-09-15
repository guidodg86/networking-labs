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
with open(f'{file_dir}/cedge_data.yaml', 'r') as f:
    cedge_data = yaml.load(f, Loader=yaml.SafeLoader)
with open(f'{file_dir}/rootcert.pem', 'r') as f:
    certificate = f.read()

environment = Environment(loader=FileSystemLoader(f"{file_dir}/jinja_templates/"))
template_pre = environment.get_template("8k_commands_autono_mode.jinja")
template_post = environment.get_template("8k_commands_controller_mode.jinja")
for device in cedge_data["devices"]:
    pre_commands = template_pre.render(
            certificate=certificate,
            uuid=device["uuid"],
            otp=device["otp"],
            organization_name= cedge_data["organization-name"],
            vbond= cedge_data["vbond"]
        )   
    post_commands = template_post.render(
            hostname=device["hostname"],
            ip_address=device["ip_address"],
            organization_name= cedge_data["organization-name"],
            vbond= cedge_data["vbond"],
            mask=device["mask"],
            system_ip=device["system-ip"],
            site_id=device["site-id"]
        )       
    with open(f"{file_dir}/results/{device["hostname"]}_pre.txt", "w") as f:
        f.write(pre_commands)
    with open(f"{file_dir}/results/{device["hostname"]}_post.txt", "w") as f:
        f.write(post_commands)

pass
