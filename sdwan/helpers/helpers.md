# Helpers

These are some scripts I used to accelerate the deployment of lab environments.

## cat8k_bootstrap_gen.py

This script helps to perform the onboarding of the cat8k to the sdwan fabric, when you use enterprise self signed.
For using it you need to have the following files on the same folder as de script:
 - File named __rootcert.pem__ with your root ca certificate
 - File named __cedge_data.yaml__ with the data of the edges that you want to onboard
 - a folder named __results__

 The structure of the file __cedge_data.yaml__ is the following:

```yaml
---
vbond: 10.10.10.10
organization-name: your-org
devices:
  - ip_address: 10.0.0.1
    mask: 255.255.255.0
    hostname: your-hostname-1
    system-ip: 1.1.1.1
    site-id: 1
    uuid: C8K-your-uuid
    otp: your-otp
  - ip_address: 10.0.0.2
    mask: 255.255.255.0
    hostname: your-hostname-2
    system-ip: 1.1.1.2
    site-id: 1
    uuid: C8K-your-uuid
    otp: your-otp
```
Here I used example values for all the fields. You need to replace this values with the real values.
The script will assume that your interface Gi1 will be connected with mpls color and the IP/subnet you indicate.

The script will generate two files for each device, one to be used when the device is in autonomous mode and the other for to use when the device is in controller mode.