# SDWAN LAB 1
## Data plane diagram
![diagram](sdwan-lab-1.png "Data plane diagram")

## General description
This lab is simulating two set of sites in two different countries, Argentina with Buenos Aires, Cordoba and Mendoza. On the other side you have Poland with Warszawa, Bielsko, Wrocław, Kraków and Katowice.

## Control plane
For this use case we are using one validator, one controller and one manager.

## Design constraints
- Traffic between countries will be able to flow via Metro Ethernet or Internet. Metro should be preferable option.
- Argentina should be HUB and SPOKE topology, where HUB is Buenos Aires (BUE)
- Each site will contain one ubuntu machine for performing tests with ping, telnet, http requests and IPERF
- Despite of BUE and WAW site being reachable via MPLS this transport must not be used
- Poland sites will form a full mesh topology
- Poland edge devices are cEdge, and Argentina are vEdge
- Each site has a core router with /24 subnets as loopback and one more subnet with the ubuntu machine
- We will have one subnet for each environment on each site. The Environments will be DEV, UAT, PROD, USERS and SERVICES.
- Argentina sites will do OSPF with the SDWAN edges. Poland will do BGP.

## Subnetting and vpn scheme
Each internal site aggregate subnet will be a /16 from 10.0.0.0/8 where second octet is site id:

| Site    | Aggregate |
| :--------| :-------: |
| BUE | 10.1.0.0/16    |
| COR | 10.11.0.0/16     |
| MDZ | 10.21.0.0/16   |
| WAW | 10.31.0.0/16    |
| KRK | 10.41.0.0/16    |
| WRO | 10.51.0.0/16    |
| BIE | 10.61.0.0/16    |
| KTW | 10.71.0.0/16    |

For each one of the subnets, the third octet will correspond with the vpn number, following the table

| Environment    | VPN ID |
| :--------| :-------: |
| DEV | 10    |
| UAT | 20     |
| PROD | 30   |
| USERS | 40    |
| SERVICES | 50    |

This number will be used also when creating the proper subnets for each site as a third octet. We can show as example of full design of BUE site:

| Site    | ENV    | VPN ID | Subnet |
| :--------| :--------| :-------: | :---: |
| BUE    | DEV    | 10 | 10.1.10.0/24 |
| BUE    | UAT    | 20 | 10.1.20.0/24 |
| BUE    | PROD    | 30 | 10.1.30.0/24 |
| BUE    | USERS    | 40 | 10.1.40.0/24 |
| BUE    | SERVICES    | 50 | 10.1.50.0/24 |

For point to point connectivity internally to the site we will use /31 subnets within the range of 192.168.0.0/16. 

For the MPLS cloud we will use the subnet 172.16.0.0/24. The router interface will have as last octet the SITE ID. The control plane IP are assigned arbitrarily as follows:

| Site    | MPLS interface    |
| :--------| :--------:| 
| BUE    | 172.16.0.1/24    |
| COR    | 172.16.0.11/24    |
| MDZ    | 172.16.0.21/24    |
| WAW    | 172.16.0.31/24    |
| KRK    | 172.16.0.41/24    |
| WRO    | 172.16.0.51/24    |
| KTW    | 172.16.0.61/24    |
| controller    | 172.16.0.100/24    |
| validator    | 172.16.0.101/24    |
| manager    | 172.16.0.102/24    |
| ubuntu root cert    | 172.16.0.103/24    |

For the Metro ethernet we will use the subnet 172.16.1.0/24 and each site will have the interface same as site ID, as follows:

| Site    | Metro Ethernet interface    |
| :--------| :--------:| 
| BUE    | 172.16.1.1/24    |
| WAW    | 172.16.1.31/24    |

For the internet cloud we will use the range 100.64.0.0/24 with the last octet same as site ID. The control plane ips are assigned arbitrarily as follows:

| Site    | Internet interface    |
| :--------| :--------:| 
| BUE    | 100.64.0.1/24    |
| COR    | 100.64.0.11/24    |
| MDZ    | 100.64.0.21/24    |
| WAW    | 100.64.0.31/24    |
| KRK    | 100.64.0.41/24    |
| WRO    | 100.64.0.51/24    |
| KTW    | 100.64.0.61/24    |
| controller    | 100.64.0.100/24    |
| validator    | 100.64.0.101/24    |
| manager    | 100.64.0.102/24    |

For the system IPs we will use the following and the org-id will be `guido-velez`

| Site    | system IP    | site ID    |
| :--------| :--------:|  :--------:| 
| BUE    | 1.1.1.4   | 1 |
| COR    | 1.1.1.11    | 11 |
| MDZ    | 1.1.1.21    | 21 |
| WAW    | 1.1.1.31    | 31 |
| KRK    | 1.1.1.41    | 41 |
| WRO    | 1.1.1.51    | 51 |
| KTW    | 1.1.1.61    | 61 |
| controller    | 1.1.1.2    | 1 |
| validator    | 1.1.1.3   | 1 |
| manager    | 1.1.1.1    | 1 |