# Sync Ranger DDoS

This scrip syncs with the [PHPipam][https://phpipam.net/api/api_documentation/] app, collecting subnet information to help [Fastnetmon Community Edition][https://github.com/pavel-odintsov/fastnetmon] scirpt perform smarter operations.



# What do we do?
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
For everything to work, PHPIpam must be structured as follows:

1. In Administration > custom-fields, under Custom Subnets fields. You must create the fields:
   - __forced_mitigation__  type boolean: The field provides information on whether the subnet is under forced mitigation.
   - __community_ddos__  type integer: The field provides information about the community that the subnet should be announced to.
   - __networks_whitelist__  type boolean: The field provides information about the subnet that should be configured in the network_whitelist file.

2. In Administration > custom-fields, under Custom VRF fields. You must create the fields:
   - __NEXT_HOP__  type varchar: The field provides information on which next hop the subnet announcement should be made.  You can create next_hop fields to accommodate your architecture.
   _It is mandatory to have a VRF created with an ip address in the registered next_hop. e.g.: 10.0.0.1_

3.  In Administration , under API:
   - __Create API__: You must create and configure access to the API.

4.  In Administration > Section , under Section management:
   - Sections must be configured with the ASN (e.g. 65006)

5.  In Administration > Subnets , under Available subnets in section xxx:
   - Subnets must be entered with the mask /24 in the section created.

6. configure src/settings.toml and src/.secrets.toml

The script is designed for a transit operator or ISP.  It does not sync private blocks (10.0.0.0/8) or CGNAT blocks (100.64.0.0/10).
The sync is configured to register valid blocks and asn.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# dependency:

Mongo v4.4
Redis v7.0.7
PHPIpam v1.5.1

# how to install?

- git clone project
- cd sync_ranger
- python3 -m venv .venv
- pip3 install -r requirements.txt
- python3 src.main.py



enjoy!