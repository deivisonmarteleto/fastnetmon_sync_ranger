"""
Service object by Collections.
"""
from dynaconf import settings

from .auth import IpamSession
from .database import MongoDB, RedisDB
from .service_ipam import IpamService


class IpamFacade:
    """
    class Facade Ipam
    """

    def __init__(self):
        self._cache = RedisDB(8)
        self._session = IpamSession.session()
        self._mongo = MongoDB()

    def get_vrf(self):
        """
        Realiza busca por todas as VRFs cadastradas no IPAM. A VRF é responsavel pelo NEXT_HOP para cada subnet.

        :param: None
        :return: Dict = { vrf_id:
                            { next_hop: str, vrf_name: str, vrf_id: str, sections_list: list }
                        }
        """
        print("Iniciando busca por vrf...")

        vrf_data: dict = {}

        get_vrf = IpamService.get(
            controller="vrf",token= self._session
        )

        for vrf in get_vrf["data"]:
            next_hop = vrf.get(settings.RANGER_NEXT_HOP)
            vrf_name = vrf.get("name")
            vrf_id = vrf.get("vrfId")
            sections_list = list(vrf.get("sections").split(";"))

            vrf_data[vrf_id] = {
                "next_hop":next_hop,
                "vrf_name":vrf_name,
                "vrf_id":vrf_id,
                "sections_list":sections_list
            }

        print("VRF`s encontradas com sucesso: %s" % vrf_data)
        return {"status":"success", "message":"vrf sucesso", "data":vrf_data}

    def get_sections(self):
        """
        Realiza busca por todas as sections cadastradas no IPAM. A section é responsavel por agrupar as subnets.
        :return: Dict = { sections_list: list }
        :param: None
        """
        print("Iniciando busca de sections ipam...")

        sections_data = []
        get_sections = IpamService.get(controller="sections",token=self._session)

        for section in get_sections["data"]:
            section_name = section.get("name")
            section_id = section.get("id")
            if section_name in ["ASN-INVALIDOS", "ASN-CGNAT"]:
                continue

            sections_data.append({
                "name": section_name,
                "id":section_id
            })

        print("Sections encontradas com sucesso: %s" % sections_data)
        return {"status":"success", "message":"sections sucesso", "data":sections_data}

    def get_subnets(self,sections_id: str, sections_name: str, vrf_item: dict):
        """
        Realiza busca por todas as subnets cadastradas no IPAM. A subnet é responsavel por agrupar as redes.
        :return: Dict = { subnet_list: list }
        :param: sections_id: str ex.: 1
        :param: sections_name: str ex.: 265066
        :param: vrf_item: dict ex.: { next_hop: str, vrf_name: str, vrf_id: str, sections_list: list }
        """
        print("Iniciando busca subneting no ipam...")

        subnet_data = []
        params = {
                "filter_match": "full",
                "filter_by": "mask",
                "filter_value": "24"
        }

        get_subnet = IpamService.get_filter_object(
            controller=f"sections/{sections_id}/subnets/",token=self._session, params=params
        )

        for subnet in get_subnet["data"]:
            subnet_id = subnet.get("id")
            subnet_community_ddos = subnet.get("custom_community_ddos")
            subnet_vrf = subnet.get("vrfId")
            subnet_networks = subnet.get("subnet")
            whitelist = subnet.get("custom_networks_whitelist")
            if whitelist == "1":
                self._cache.save(key=f"whitelist_{subnet_networks}", obj=subnet_networks, ex_token=89000)

            if not vrf_item.get(subnet_vrf):
                next_hop = "0.0.0.0"
                print(
                    f"*****>>>>> Subnet sem VRF <<<<<******* - net: {subnet_networks} - asn: {sections_name}"
                )
            else:
                next_hop = vrf_item[subnet_vrf]["next_hop"]


            subnet_dict = {
                "_id" : subnet_id,
                "id" :  subnet_id,
                "net" : subnet_networks,
                "asn" : sections_name,
                "hop" : next_hop,
                "whitelist" : whitelist,
                "community_ddos": int(subnet_community_ddos),
                "guard" : "0"
            }
            self._cache.save(key=f"network_{subnet_networks}", obj=subnet_networks, ex_token=89000)
            self._mongo.find_and_update_by_options(coll="subnet", value_id={"_id" : subnet_id}, value_update=subnet_dict)
            subnet_data.append(subnet_dict)
        return {"status":"success", "message":"subneting sucesso", "data":subnet_data}
