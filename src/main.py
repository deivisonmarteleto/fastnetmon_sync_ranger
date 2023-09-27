#IMPORTS
"""
Main module
"""
from dynaconf import settings

from app.database import MongoDB, RedisDB
from app.facade_ipam import IpamFacade
from app.service_subnet import ServiceSubnet


def main() -> None:
    """
    Main method
    """
    cache = RedisDB(8)
    mongo = MongoDB()

    print("Clearing cache tables...")
    cache.flushall_key()

    print("Clearing the subnet table...")
    mongo.drop_collection(coll="subnet")

    ipam = IpamFacade()
    subneting_whitelist = []
    subneting_all_whitelist = []
    
    get_vrf = ipam.get_vrf()
    get_sections = ipam.get_sections()
    for section in get_sections["data"]:
        section_name = section.get("name")
        section_id = section.get("id")
        ipam.get_subnets(sections_id=section_id,sections_name=section_name, vrf_item=get_vrf["data"])

    subneting = cache.keys()
    if subneting:
        for cidr in subneting:
            if cidr.split("_")[0] == "whitelist":
                subneting_whitelist.append(cidr.split("_")[1])

            subneting_all_whitelist.append(cidr.split("_")[1])

        subnet_mask_26 = ServiceSubnet.granerSubneting(subneting=subneting_all_whitelist)
        print("sending list of blocks 26 to be saved in network_list...")
        ServiceSubnet.save_file(subneting=subnet_mask_26, file=settings.FILE_NETWORK)

        if subneting_whitelist:
            subnet_mask_26_whitelist = ServiceSubnet.granerSubneting(subneting=subneting_whitelist)
            print("sending list of blocks 26 to save in network_whitelist...")
            ServiceSubnet.save_file(subneting=subnet_mask_26_whitelist, file=settings.FILE_NETWORK_WHITE)
        else:
            print("The whitelist is empty...")

        print("END! Sync with ipam successfully completed...")

    else:
        print("The is empty.")

if __name__ == '__main__':
    print("Starting the Sync process with IPAM....")
    print("environment: %s" % settings.RANGER_NEXT_HOP)
    main()
